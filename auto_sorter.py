import os

# --- CONFIGURATION ---
# This points to your specific local repository path
TARGET_ROOT = r"C:\Users\qkly1\OneDrive\Documents\GitHub\New-layout\games"

# The Bridge Script to Inject
BRIDGE_SCRIPT = """
<script>
(function() {
    const UNITY_DB_PATH = '/idbfs'; 
    const CHECK_INTERVAL_MS = 5000; 

    // 1. SAVE: Periodically check for file changes
    setInterval(async () => {
        if (typeof FS === 'undefined') return; 
        try {
            // This path covers Unity PlayerPrefs; Godot uses a similar FS structure
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
"""

def inject_code_recursively(root_dir):
    print(f"📂 Scanning Directory: {root_dir}")
    print("-" * 50)
    
    injected_count = 0
    skipped_count = 0
    error_count = 0

    if not os.path.exists(root_dir):
        print(f"❌ Error: Target directory does not exist: {root_dir}")
        return

    for subdir, dirs, files in os.walk(root_dir):
        if "index.html" in files:
            file_path = os.path.join(subdir, "index.html")
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check if already injected (prevents duplicates)
                if "UNITY/GODOT SAVE BRIDGE" in content:
                    print(f"⏭  Skipping (Already Exists): {subdir}")
                    skipped_count += 1
                    continue

                # Inject before </body>
                if "</body>" in content:
                    new_content = content.replace("</body>", BRIDGE_SCRIPT + "\n</body>")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    print(f"✅ Injected: {subdir}")
                    injected_count += 1
                else:
                    print(f"⚠️ Warning: No </body> tag found in {subdir}")
                    error_count += 1

            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                error_count += 1

    print("-" * 50)
    print(f"🎉 Done!")
    print(f"Injected: {injected_count}")
    print(f"Skipped:  {skipped_count}")
    print(f"Errors:   {error_count}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    inject_code_recursively(TARGET_ROOT)
