import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

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

REMOVE_PATTERNS = [
    r"UNITY_DB_PATH",
    r"PlayerPrefs",
    r"FS\.open\(",
    r"btoa\(",
    r"atob\(",
    r"postMessage\([\s\S]*?\);",
    r"window\.addEventListener\([\s\S]*?LOAD_SAVE[\s\S]*?\);",
]

# ---------- Folder Picker ----------
root = tk.Tk()
root.withdraw()
repo_path = filedialog.askdirectory(title="Select your repo folder")
if not repo_path:
    input("No folder selected. Press Enter to exit...")
    exit()

repo = Path(repo_path)

updated = 0

for html in repo.rglob("*.html"):
    text = html.read_text(encoding="utf-8", errors="ignore")

    if "Engine save restored" in text:
        continue

    original = text

    for pattern in REMOVE_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)

    if "</body>" in text:
        text = text.replace("</body>", UNITY_BRIDGE + "\n</body>")

    if text != original:
        html.write_text(text, encoding="utf-8")
        print(f"[UNITY] Updated {html}")
        updated += 1

print(f"\n✅ Unity/Godot migration complete — {updated} files updated")
input("Press Enter to close...")
