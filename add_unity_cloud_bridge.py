from pathlib import Path
import tkinter as tk
from tkinter import filedialog

UNITY_CLOUD_BRIDGE = """
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
</script>
""".strip()

root = tk.Tk()
root.withdraw()
repo_path = filedialog.askdirectory(title="Select your repo folder")
if not repo_path:
    input("No folder selected. Press Enter to exit...")
    exit()

repo = Path(repo_path)
added = 0

for folder in repo.iterdir():
    index = folder / "index.html"
    if not index.is_file():
        continue

    text = index.read_text(encoding="utf-8", errors="ignore")

    if "Engine save restored" in text:
        continue  # already added

    if "</body>" not in text:
        continue  # don't touch broken files

    index.write_text(
        text.replace("</body>", UNITY_CLOUD_BRIDGE + "\n</body>"),
        encoding="utf-8"
    )

    print(f"[UNITY] Added cloud bridge to {index}")
    added += 1

print(f"\n✅ Done — added Unity/Godot cloud bridge to {added} games")
input("Press Enter to close...")
