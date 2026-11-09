"""Dev-only: extract inline <script> blocks and the app.py extension script, then
node --check each. Not part of the application."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = Path(__file__).resolve().parent

targets = []

qa = (SCRATCH / "qa-index.html").read_text(encoding="utf-8")
for i, block in enumerate(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", qa, re.S)):
    targets.append((f"qa-index.html script #{i + 1}", block))

app_src = (ROOT / "app.py").read_text(encoding="utf-8")
m = re.search(r'STATE_PAGE_EXTENSION = r"""(.*?)"""', app_src, re.S)
if m:
    inner = m.group(1)
    for i, block in enumerate(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", inner, re.S)):
        targets.append((f"app.py STATE_PAGE_EXTENSION script #{i + 1}", block))

failures = 0
for name, code in targets:
    if not code.strip():
        continue
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
        fh.write(code)
        tmp = fh.name
    result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    status = "OK" if result.returncode == 0 else "FAIL"
    if result.returncode != 0:
        failures += 1
        print(f"[{status}] {name}\n{result.stderr.strip()}")
    else:
        print(f"[{status}] {name}")
    Path(tmp).unlink(missing_ok=True)

print(f"checked {len(targets)} script blocks, {failures} failure(s)")
sys.exit(1 if failures else 0)
