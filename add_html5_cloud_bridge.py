from pathlib import Path
import tkinter as tk
from tkinter import filedialog

HTML5_CLOUD_BRIDGE = """
<script>
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

    if "HTML5 save restored" in text:
        continue  # already added

    if "</body>" not in text:
        continue  # don't touch weird files

    index.write_text(
        text.replace("</body>", HTML5_CLOUD_BRIDGE + "\n</body>"),
        encoding="utf-8"
    )

    print(f"[HTML5] Added cloud bridge to {index}")
    added += 1

print(f"\n✅ Done — added HTML5 cloud bridge to {added} games")
input("Press Enter to close...")
