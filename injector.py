import os

# --- CONFIGURATION ---
# This is the code we want to inject.
# I added a comment at the top so the script knows not to add it twice.
INJECTION_CODE = """
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
"""

def inject_code_into_directory(root_dir):
    print(f"Scanning directory: {root_dir}")
    count = 0
    
    # os.walk goes through every folder and subfolder automatically
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(subdir, file)
                process_file(filepath)
                count += 1
                
    print(f"Done! Processed {count} files.")

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check if we already added the script to avoid duplicates
        if "BRIDGE SCRIPT START" in content:
            print(f"Skipping (Already exists): {filepath}")
            return

        # 2. Find the closing body tag
        if "</body>" in content:
            # Replace </body> with our Code + </body>
            new_content = content.replace("</body>", INJECTION_CODE + "\n</body>")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Success: {filepath}")
        else:
            print(f"Warning: No </body> tag found in {filepath}")

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Ask the user for the folder path
    target_folder = input("Paste the full path to your 'games' folder: ").strip()
    
    # Remove quotes if Windows added them
    target_folder = target_folder.replace('"', '')

    if os.path.exists(target_folder):
        inject_code_into_directory(target_folder)
    else:
        print("Error: That folder does not exist.")
    
    input("Press Enter to exit...")
