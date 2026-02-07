from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import re

MARKERS = [
    "UNITY_DB_PATH",
    "PlayerPrefs",
    "btoa(",
    "atob(",
    "FS.open("
]

SCRIPT_BLOCK_RE = re.compile(
    r"<script[\s\S]*?>[\s\S]*?</script>",
    re.IGNORECASE
)

root = tk.Tk()
root.withdraw()
repo_path = filedialog.askdirectory(title="Select your repo folder")
if not repo_path:
    input("No folder selected. Press Enter to exit...")
    exit()

repo = Path(repo_path)
removed = 0

for folder in repo.iterdir():
    index = folder / "index.html"
    if not index.is_file():
        continue

    text = index.read_text(encoding="utf-8", errors="ignore")
    original = text

    def strip_if_unity_base64(match):
        block = match.group(0)
        return "" if all(m in block for m in MARKERS) else block

    new_text = SCRIPT_BLOCK_RE.sub(strip_if_unity_base64, text)

    if new_text != original:
        index.write_text(new_text, encoding="utf-8")
        print(f"[UNITY] Removed Base64 bridge from {index}")
        removed += 1

print(f"\n✅ Done — removed Unity Base64 bridge from {removed} index.html files")
input("Press Enter to close...")
