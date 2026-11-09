#!/usr/bin/env python3
"""Check external URLs referenced by the archive's JSON content files.

Run from the project root:
    python check_archive_links.py

The script only reads JSON files and writes two reports. It does not modify
state_pages.json, food_stories.json, or any project source/assets.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path.cwd()
INPUT_FILES = ("state_pages.json", "food_stories.json")
CSV_REPORT = ROOT / "archive_link_check_report.csv"
SUMMARY_REPORT = ROOT / "archive_link_check_summary.txt"
TIMEOUT_SECONDS = 15
MAX_WORKERS = 6
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def find_urls(value: Any, location: str, found: list[dict[str, str]]) -> None:
    """Recursively collect HTTP(S) URL strings and their JSON paths."""
    if isinstance(value, dict):
        for key, child in value.items():
            find_urls(child, f"{location}.{key}" if location else str(key), found)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            find_urls(child, f"{location}[{index}]", found)
    elif isinstance(value, str) and value.strip().lower().startswith(("http://", "https://")):
        found.append({"location": location, "url": value.strip()})


def request_once(url: str, method: str) -> tuple[int | None, str, str]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "Range": "bytes=0-4095",
        "Connection": "close",
    }
    request = Request(url, headers=headers, method=method)
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            # A small read for GET confirms that the server sends a response;
            # Range requests avoid downloading complete PDFs or large pages.
            if method == "GET":
                response.read(4096)
            return response.status, response.geturl(), response.headers.get("Content-Type", "")
    except HTTPError as error:
        return error.code, error.geturl(), error.headers.get("Content-Type", "") if error.headers else ""
    except URLError as error:
        reason = getattr(error, "reason", error)
        return None, "", f"connection error: {reason}"
    except TimeoutError:
        return None, "", "timeout"
    except Exception as error:  # DNS, TLS, malformed URL, socket errors, etc.
        return None, "", f"{type(error).__name__}: {error}"


def check_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {
            "status": "INVALID_URL", "http_status": "", "method": "NONE",
            "final_url": "", "content_type": "", "note": "URL is malformed or not HTTP(S).",
        }

    # HEAD is cheap. Many publishers reject HEAD, so retry with a small GET.
    head_status, head_final, head_info = request_once(url, "HEAD")
    if head_status is not None and 200 <= head_status < 400:
        return {
            "status": "WORKING", "http_status": str(head_status), "method": "HEAD",
            "final_url": head_final or url, "content_type": head_info,
            "note": "Server returned a successful response (redirects followed).",
        }

    # GET fallback also handles sites that block HEAD or return method-specific errors.
    get_status, get_final, get_info = request_once(url, "GET")
    if get_status is not None and 200 <= get_status < 400:
        return {
            "status": "WORKING", "http_status": str(get_status), "method": "GET fallback",
            "final_url": get_final or url, "content_type": get_info,
            "note": "GET succeeded after HEAD was unavailable or unsuccessful.",
        }

    status_code = get_status if get_status is not None else head_status
    info = get_info if get_status is not None else head_info
    final = get_final or head_final or ""

    if status_code in {404, 410}:
        label, note = "BROKEN", "The server says this resource was not found or is gone."
    elif status_code in {401, 403, 451}:
        label, note = "BLOCKED / RESTRICTED", "The site denied automated access; verify in a normal browser before replacing."
    elif status_code == 429:
        label, note = "RATE LIMITED", "The site is rate-limiting automated requests; retry later or verify manually."
    elif status_code is not None and 500 <= status_code <= 599:
        label, note = "SERVER ERROR", "The publisher returned a server-side error; retry later."
    elif status_code is not None:
        label, note = "CHECK MANUALLY", f"Non-success HTTP response: {status_code}."
    else:
        label = "CONNECTION ERROR"
        note = info or "Could not establish a connection."

    return {
        "status": label, "http_status": str(status_code or ""), "method": "HEAD + GET",
        "final_url": final, "content_type": "", "note": note,
    }


def main() -> int:
    occurrences: list[dict[str, str]] = []
    missing_files: list[str] = []

    for filename in INPUT_FILES:
        path = ROOT / filename
        if not path.is_file():
            missing_files.append(filename)
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"ERROR: Could not read {filename}: {error}")
            return 2
        found: list[dict[str, str]] = []
        find_urls(payload, filename, found)
        for item in found:
            occurrences.append({"file": filename, **item})

    if missing_files:
        print("Missing input file(s): " + ", ".join(missing_files))
        print("Place this script beside state_pages.json and food_stories.json.")
        return 2

    if not occurrences:
        print("No HTTP(S) URLs found in the two JSON files.")
        return 0

    paths_by_url: dict[str, list[str]] = defaultdict(list)
    for item in occurrences:
        paths_by_url[item["url"]].append(f'{item["file"]}: {item["location"]}')

    unique_urls = list(paths_by_url)
    print(f"Found {len(occurrences)} URL occurrence(s), {len(unique_urls)} unique URL(s).")
    print(f"Checking with {MAX_WORKERS} workers; reports will be saved in {ROOT}.\n")

    results: dict[str, dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_url, url): url for url in unique_urls}
        completed = 0
        for future in as_completed(futures):
            url = futures[future]
            try:
                results[url] = future.result()
            except Exception as error:
                results[url] = {
                    "status": "CHECK ERROR", "http_status": "", "method": "NONE",
                    "final_url": "", "content_type": "", "note": str(error),
                }
            completed += 1
            result = results[url]
            print(f"[{completed:>3}/{len(unique_urls)}] {result['status']:<20} {url}")

    fields = ["status", "http_status", "method", "file", "location", "url", "final_url", "content_type", "note"]
    with CSV_REPORT.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in occurrences:
            result = results[item["url"]]
            writer.writerow({
                **result,
                "file": item["file"],
                "location": item["location"],
                "url": item["url"],
            })

    unique_counts = Counter(result["status"] for result in results.values())
    occurrence_counts = Counter(results[item["url"]]["status"] for item in occurrences)
    lines = [
        "INDIA'S CULINARY MEMORY ARCHIVE — LINK CHECK SUMMARY",
        "=" * 58,
        f"URL occurrences in JSON: {len(occurrences)}",
        f"Unique URLs checked: {len(unique_urls)}",
        "",
        "Unique URL results:",
    ]
    for status, count in sorted(unique_counts.items()):
        lines.append(f"  {status}: {count}")
    lines.extend(["", "Occurrences by result:"])
    for status, count in sorted(occurrence_counts.items()):
        lines.append(f"  {status}: {count}")
    lines.extend([
        "",
        "Interpretation:",
        "  WORKING = server responded successfully; this does not prove the page supports the cited claim.",
        "  BROKEN = 404/410; replace or correct the URL after confirming the source.",
        "  BLOCKED / RESTRICTED = publisher denied automated access; open it manually before calling it broken.",
        "  RATE LIMITED / SERVER ERROR / CONNECTION ERROR = retry later before taking action.",
        "",
        f"Detailed report: {CSV_REPORT.name}",
    ])
    SUMMARY_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n" + "\n".join(lines))
    print(f"\nSaved: {CSV_REPORT.name}")
    print(f"Saved: {SUMMARY_REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
