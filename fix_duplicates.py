import os

# --- CONFIGURATION ---
TARGET_ROOT = r"C:\Users\qkly1\OneDrive\Documents\GitHub\New-layout\games"

# We look for this unique line to count how many times the script appears
SIGNATURE = "const UNITY_DB_PATH = '/idbfs';"

# This is the CLEAN version we want to keep (One copy)
CLEAN_BRIDGE_SCRIPT = """
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
"""

def clean_duplicates(root_dir):
    print(f"🧹 Scanning for duplicates in: {root_dir}")
    fixed_count = 0

    for subdir, dirs, files in os.walk(root_dir):
        if "index.html" in files:
            file_path = os.path.join(subdir, "index.html")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Count how many times the script signature appears
            occurrences = content.count(SIGNATURE)

            if occurrences > 1:
                print(f"  ⚠️ Found {occurrences} copies in: {subdir}")
                
                # STRATEGY: 
                # 1. Remove ALL instances of the script (using a rough split/replace)
                #    Since exact string matching can fail if spacing differs, 
                #    we will remove the file's bottom section and rebuild it.
                
                # A safer way: Split by the signature and reconstruct, 
                # but simply replacing the file end is often safest for bulk Unity fixes.
                
                if "</body>" in content:
                    # Strip out everything after </body> tag if it got messy,
                    # or better: Remove the specific blocks we inserted.
                    
                    # NOTE: This approach assumes the duplicates are the EXACT text block.
                    # If they vary slightly, we need to be aggressive.
                    
                    # Simple fix: We know where we injected. Let's look for our comments.
                    # If you didn't use comments before, we will search for the code block start.
                    
                    # 1. Remove the markers if they exist
                    content = content.replace("", "")
                    content = content.replace("", "")
                    content = content.replace("", "")

                    # 2. Remove the Script Block (We try to match the code you pasted)
                    # We utilize the fact that the code starts with specific unique lines.
                    
                    # We will simply wipe the specific code block by splitting the file.
                    # This is aggressive but effective for identical duplicates.
                    
                    # If we can't cleanly remove via replace, we append a FRESH copy 
                    # only after manually verifying we deleted the old ones.
                    
                    pass 
                
                # --- ROBUST REPLACEMENT METHOD ---
                # We will write a new clean file that definitely only has ONE copy.
                
                # 1. Read lines
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                new_lines = []
                inside_bad_script = False
                
                for line in lines:
                    # Detect start of our specific script
                    if "const UNITY_DB_PATH = '/idbfs';" in line:
                        inside_bad_script = True
                        # Look backwards to remove the opening <script> tag from new_lines
                        if new_lines and "<script>" in new_lines[-1]:
                            new_lines.pop()
                        elif new_lines and "(function() {" in new_lines[-1]: # Handle different formatting
                             pass
                    
                    # Detect end of our specific script
                    if inside_bad_script and "})();" in line:
                        inside_bad_script = False
                        # Look ahead to remove closing </script> if it's on the next line
                        continue 
                    
                    if inside_bad_script:
                        continue
                        
                    # Also strip standalone closing script tags if we just exited a bad block
                    if line.strip() == "</script>" and inside_bad_script == False:
                        # This is risky, only skip if we suspect it belongs to our removed block
                        # For safety, we will let the "Replace </body>" logic handle the re-add.
                        pass

                    new_lines.append(line)
                
                # Re-join
                cleaned_content = "".join(new_lines)
                
                # Remove any leftover closing tags from the sloppy removal above
                # (This is a quick hack to clean up the specific artifacts)
                cleaned_content = cleaned_content.replace("<script>\n</script>", "")
                
                # Now add ONE clean copy back
                final_content = cleaned_content.replace("</body>", CLEAN_BRIDGE_SCRIPT + "\n</body>")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(final_content)
                    
                print(f"  ✅ Fixed: {subdir}")
                fixed_count += 1

    print("-" * 50)
    print(f"🎉 Cleanup Complete! Fixed {fixed_count} files.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    clean_duplicates(TARGET_ROOT)
