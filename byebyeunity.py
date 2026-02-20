from pathlib import Path
import tkinter as tk
from tkinter import filedialog

OLD_SCRIPT = """<script>
(function () {
  const GAME_ID = location.pathname;
  const SAVE_KEY = "engine_save_v1";

  async function loadSave() {
    if (!window.parent?.cloudLoad) return;
    const save = await window.parent.cloudLoad(GAME_ID);
    if (!save) return;

    if (typeof FS !== "undefined") {
      FS.syncfs(true, () =>
        console.log("[CloudSave] Engine save restored")
      );
    }
  }

  window.addEventListener("beforeunload", () => {
    if (!window.parent?.cloudSave) return;
    window.parent.cloudSave(GAME_ID, { [SAVE_KEY]: true });
  });

  loadSave();
})();
</script>"""

# --- Pick Folder ---
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Select Repo Root Folder")

if not folder_path:
    print("No folder selected.")
    input("Press Enter to exit...")
    exit()

removed = 0

for index in Path(folder_path).rglob("index.html"):
    text = index.read_text(encoding="utf-8", errors="ignore")

    # normalize line endings
    normalized_text = text.replace("\r\n", "\n")
    normalized_old = OLD_SCRIPT.replace("\r\n", "\n")

    if normalized_old in normalized_text:
        normalized_text = normalized_text.replace(normalized_old, "")
        index.write_text(normalized_text, encoding="utf-8")
        print("Removed Unity script from:", index)
        removed += 1

print("\nDone. Removed from", removed, "files.")
input("Press Enter to exit...")
