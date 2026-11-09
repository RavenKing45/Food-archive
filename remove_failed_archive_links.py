#!/usr/bin/env python3
"""Remove source entries whose URLs failed archive_link_check_report.csv.

Place this script, archive_link_check_report.csv, state_pages.json, and
food_stories.json in the project root, then run:
    python remove_failed_archive_links.py

Only source references listed with a non-WORKING status are removed. Existing
JSON files are backed up before replacement. Narrative/content fields remain.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "archive_link_check_report.csv"
JSON_FILES = ("state_pages.json", "food_stories.json")


def parse_location(location: str, filename: str) -> list[str | int]:
    prefix = filename
    if not location.startswith(prefix):
        raise ValueError(f"Location does not start with {filename!r}: {location}")
    remainder = location[len(prefix):]
    tokens: list[str | int] = []
    for match in re.finditer(r"\.([A-Za-z0-9_-]+)|\[(\d+)\]", remainder):
        key, index = match.groups()
        tokens.append(key if key is not None else int(index))
    return tokens


def resolve_parent(root: Any, tokens: list[str | int]) -> tuple[Any, str | int]:
    if not tokens:
        raise ValueError("Empty JSON path")
    current = root
    for token in tokens[:-1]:
        current = current[token]
    return current, tokens[-1]


def read_report() -> list[dict[str, str]]:
    if not REPORT.exists():
        raise FileNotFoundError(
            f"Missing {REPORT.name}. Put the link-check CSV beside this script."
        )
    with REPORT.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"status", "file", "location", "url"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("CSV is empty or is missing required columns: status, file, location, url")
    return [row for row in rows if row["status"].strip().upper() != "WORKING"]


def make_plan(filename: str, data: Any, failed_rows: list[dict[str, str]]):
    # Array deletions are grouped and applied from the largest index downward,
    # so repeated removals from the same list cannot shift later targets.
    list_deletions: dict[tuple[str | int, ...], list[tuple[int, str, str]]] = defaultdict(list)
    field_deletions: list[tuple[tuple[str | int, ...], str, str]] = []

    for row in failed_rows:
        location, expected_url = row["location"], row["url"]
        tokens = parse_location(location, filename)
        if not tokens:
            raise ValueError(f"No JSON path in {location}")

        # A failed URL inside a sources[n] object means remove that source
        # object. For standalone fields such as oralNarrative.sourceUrl,
        # remove only the URL field and retain the narrative itself.
        if (
            len(tokens) >= 3
            and tokens[-1] == "url"
            and isinstance(tokens[-2], int)
            and tokens[-3] == "sources"
        ):
            list_path = tuple(tokens[:-2])
            index = tokens[-2]
            source_list = data
            for part in list_path:
                source_list = source_list[part]
            if not isinstance(source_list, list) or index >= len(source_list):
                raise ValueError(f"Source-list index no longer exists: {location}")
            source = source_list[index]
            if not isinstance(source, dict) or source.get("url") != expected_url:
                raise ValueError(f"URL/path mismatch; refusing to remove: {location}")
            list_deletions[list_path].append((index, expected_url, location))
        else:
            parent, key = resolve_parent(data, tokens)
            if not isinstance(parent, dict) or key not in parent or parent[key] != expected_url:
                raise ValueError(f"URL/path mismatch; refusing to remove: {location}")
            field_deletions.append((tuple(tokens[:-1]), str(key), location))

    return list_deletions, field_deletions


def apply_plan(data: Any, plan) -> tuple[Any, int]:
    list_deletions, field_deletions = plan
    removed = 0

    for list_path, entries in list_deletions.items():
        source_list = data
        for part in list_path:
            source_list = source_list[part]
        for index, _url, _location in sorted(entries, key=lambda item: item[0], reverse=True):
            del source_list[index]
            removed += 1

    for parent_path, key, _location in field_deletions:
        parent = data
        for part in parent_path:
            parent = parent[part]
        del parent[key]
        removed += 1

    return data, removed


def backup_path(path: Path) -> Path:
    candidate = path.with_name(path.name + ".before_link_cleanup.bak")
    number = 2
    while candidate.exists():
        candidate = path.with_name(path.name + f".before_link_cleanup.{number}.bak")
        number += 1
    return candidate


def atomic_write_json(path: Path, data: Any) -> None:
    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="\n", dir=path.parent,
        prefix=path.name + ".", suffix=".tmp", delete=False
    ) as tmp:
        tmp.write(content)
        temporary = Path(tmp.name)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show planned removals without changing JSON files")
    args = parser.parse_args()

    failed_rows = read_report()
    if not failed_rows:
        print("No non-WORKING links found. Nothing to change.")
        return 0

    # Load and validate every target before writing either JSON file.
    loaded: dict[str, Any] = {}
    plans = {}
    for filename in JSON_FILES:
        path = ROOT / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing {filename}; put this script in the project root.")
        with path.open("r", encoding="utf-8") as handle:
            loaded[filename] = json.load(handle)
        rows_for_file = [row for row in failed_rows if row["file"] == filename]
        plans[filename] = make_plan(filename, loaded[filename], rows_for_file)

    if any(row["file"] not in JSON_FILES for row in failed_rows):
        unexpected = sorted({row["file"] for row in failed_rows if row["file"] not in JSON_FILES})
        raise ValueError(f"Unexpected file names in report: {unexpected}")

    print(f"Failed URL occurrences selected: {len(failed_rows)}")
    print(f"Unique failed URLs: {len({row['url'] for row in failed_rows})}")
    print("Statuses selected for removal:")
    for status, count in Counter(row["status"] for row in failed_rows).items():
        print(f"  {status}: {count}")

    transformed = {}
    total_removed = 0
    for filename in JSON_FILES:
        data, removed = apply_plan(loaded[filename], plans[filename])
        transformed[filename] = data
        total_removed += removed
        print(f"  {filename}: {removed} reference(s) removed")

    if args.dry_run:
        print("Dry run only — no files changed.")
        return 0

    for filename in JSON_FILES:
        path = ROOT / filename
        backup = backup_path(path)
        shutil.copy2(path, backup)
        atomic_write_json(path, transformed[filename])
        print(f"Updated {filename}; backup: {backup.name}")

    print(f"\nDone. Removed {total_removed} failed source reference(s).")
    print("Dish descriptions, historical text, oral narratives, images, and working links were retained.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
