from pathlib import Path
import tkinter as tk
from tkinter import filedialog

TARGET_SNIPPET = """
<script>
(function() {
    const UNITY_DB_PATH = '/idbfs'; 
    const CHECK_INTERVAL_MS = 5000; 

    // 1. SAVE: Periodically check for file changes
    setInterval(async () => {
        if (typeof FS === 'undefined') return; 
        try {
            const filePath = `${UNITY_DB_PATH}/PlayerPrefs`;
            const stream = FS.open(filePath, 'r');
            if (stream) {
                const stat = FS.stat(filePath);
                const buf = new Uint8Array(stat.size);
                FS.read(stream, buf, 0, stat.size, 0);
                FS.close(stream);
                
                const base64Data = btoa(String.fromCharCode.apply(null, buf));
                window.parent.postMessage({
                    type: "GAME_SAVE",
                    key: "unity_save_file_v1", 
                    value: base64Data,
                    gameId: window.location.pathname
                }, "*"); 
            }
        } catch (e) {}
    }, CHECK_INTERVAL_MS); 

    // 2. LOAD: Write data back to FS
    window.addEventListener("message", (event) => {
        if (event.data.type === "LOAD_SAVE") {
            const base64Data = event.data.payload["unity_save_file_v1"];
            if (base64Data && typeof FS !== 'undefined') {
                try {
                    const binaryString = atob(base64Data);
                    const bytes = new Uint8Array(binaryString.length);
                    for (let i = 0; i < binaryString.length; i++) {
                        bytes[i] = binaryString.charCodeAt(i);
                    }
                    const filePath = `${UNITY_DB_PATH}/PlayerPrefs`;
                    const stream = FS.open(filePath, 'w+');
                    FS.write(stream, bytes, 0, bytes.length, 0);
                    FS.close(stream);
                    FS.syncfs(false, () => console.log("[Bridge] Save Restored to Engine"));
                } catch(e) { console.error(e); }
            }
        }
    });
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
    print(f"[UNITY] Removed Base64 bridge from {index}")
    removed += 1

print(f"\n✅ Done — removed from {removed} index.html files")
input("Press Enter to close...")
