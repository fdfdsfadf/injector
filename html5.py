from pathlib import Path
import tkinter as tk
from tkinter import filedialog

OLD_SCRIPT = """<script>
(function () {
  const gameId = location.hostname + location.pathname;

  // LOAD from cloud
  window.addEventListener("message", (event) => {
    if (event.data?.type !== "LOAD_SAVE") return;
    const save = event.data.payload;
    if (!save) return;

    Object.entries(save).forEach(([k, v]) => {
      localStorage.setItem(k, v);
    });

    console.log("[CloudSave] HTML5 save restored");
  });

  // SAVE to cloud
  const originalSet = localStorage.setItem;
  localStorage.setItem = function (key, value) {
    originalSet.apply(this, arguments);
    if (window.parent?.cloudSave) {
      window.parent.cloudSave(gameId, { [key]: value });
    }
  };
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

    normalized_text = text.replace("\r\n", "\n")
    normalized_old = OLD_SCRIPT.replace("\r\n", "\n")

    if normalized_old in normalized_text:
        normalized_text = normalized_text.replace(normalized_old, "")
        index.write_text(normalized_text, encoding="utf-8")
        print("Removed HTML5 script from:", index)
        removed += 1

print("\nDone. Removed from", removed, "files.")
input("Press Enter to exit...")
