from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import re

UNITY_BRIDGE = """
<script>
(function () {
  const GAME_ID = location.pathname;
  const SAVE_KEY = "engine_save_v1";

  async function loadSave() {
    if (!window.parent?.cloudLoad) return;
    const save = await window.parent.cloudLoad(GAME_ID);
    if (!save) return;

    if (typeof FS !== "undefined") {
      FS.syncfs(true, () =>
        console.log("[Bridge] Engine save restored")
      );
    }
  }

  window.addEventListener("beforeunload", () => {
    if (!window.parent?.cloudSave) return;
    window.parent.cloudSave(GAME_ID, { [SAVE_KEY]: true });
  });

  loadSave();
})();
</script>
"""

# Any script block containing these is nuked entirely
BAD_MARKERS = [
    "localStorage.setItem",
    "UNITY_DB_PATH",
    "PlayerPrefs",
    "GAME_SAVE",
    "LOAD_SAVE",
    "postMessage",
    "btoa(",
    "atob(",
    "FS.open(",
]

root = tk.Tk()
root.withdraw()
repo_path = filedialog.askdirectory(title="Select your repo folder")
if not repo_path:
    input("No folder selected. Press Enter to exit...")
    exit()

repo = Path(repo_path)
updated = 0

SCRIPT_BLOCK = re.compile(r"<script[\s\S]*?>[\s\S]*?</script>", re.IGNORECASE)

for html in repo.rglob("*.html"):
    text = html.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Remove bad script blocks entirely
    def strip_bad(match):
        block = match.group(0)
        return "" if any(m in block for m in BAD_MARKERS) else block

    text = SCRIPT_BLOCK.sub(strip_bad, text)

    # Ensure exactly one Unity bridge
    if "Engine save restored" not in text and "</body>" in text:
        text = text.replace("</body>", UNITY_BRIDGE + "\n</body>")

    if text != original:
        html.write_text(text, encoding="utf-8")
        print(f"[FIXED] {html}")
        updated += 1

print(f"\n✅ Unity cleanup complete — {updated} files fixed")
input("Press Enter to close...")
