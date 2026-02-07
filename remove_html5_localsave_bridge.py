from pathlib import Path
import tkinter as tk
from tkinter import filedialog

TARGET_SNIPPET = """
<script>
(function() {
    const PARENT_DOMAIN = "https://main1.macbooksuck.xyz"; 

    window.addEventListener("message", (event) => {
        if (event.origin !== PARENT_DOMAIN) return;
        if (event.data.type === "LOAD_SAVE") {
            const data = event.data.payload;
            Object.keys(data).forEach(key => localStorage.setItem(key, data[key]));
            console.log("[Bridge] Save Loaded");
        }
    });

    const originalSetItem = localStorage.setItem;
    localStorage.setItem = function(key, value) {
        originalSetItem.apply(this, arguments);
        const uniqueGameId = window.location.hostname + window.location.pathname;
        window.parent.postMessage({
            type: "GAME_SAVE",
            key: key,
            value: value,
            gameId: uniqueGameId 
        }, PARENT_DOMAIN);
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
removed = 0

for folder in repo.iterdir():
    index = folder / "index.html"
    if not index.is_file():
        continue

    text = index.read_text(encoding="utf-8", errors="ignore")
    if TARGET_SNIPPET not in text:
        continue

    index.write_text(text.replace(TARGET_SNIPPET, ""), encoding="utf-8")
    print(f"[HTML5] Removed localStorage bridge from {index}")
    removed += 1

print(f"\n✅ Done — removed from {removed} index.html files")
input("Press Enter to close...")
