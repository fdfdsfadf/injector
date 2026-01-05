import os
import shutil

# --- CONFIGURATION (Hardcoded paths as requested) ---
SOURCE_DIR = r"C:\Users\qkly1\OneDrive\Documents\GitHub\justgames\games"
DEST_UNITY = r"C:\Users\qkly1\OneDrive\Documents\GitHub\New-layout\games\unity"
DEST_GODOT = r"C:\Users\qkly1\OneDrive\Documents\GitHub\New-layout\games\godot"

def identify_game_engine(game_folder_path):
    """
    Scans a single game folder to guess if it is Unity or Godot.
    Returns: 'unity', 'godot', or None
    """
    for root, dirs, files in os.walk(game_folder_path):
        # 1. Check for Godot (.pck file)
        for file in files:
            if file.endswith('.pck'):
                return 'godot'

        # 2. Check for Unity (Build folder or .unityweb files)
        if "Build" in dirs:
            # Look inside the Build folder for verification
            try:
                build_path = os.path.join(root, "Build")
                build_files = os.listdir(build_path)
                for bf in build_files:
                    if bf.endswith(".loader.js") or bf.endswith(".framework.js") or bf.endswith(".data"):
                        return 'unity'
            except:
                pass
        
        # Check for older Unity signatures in file list
        for file in files:
            if file.endswith(".unityweb") or "UnityLoader.js" in file:
                return 'unity'

    return None

def copy_game(game_name, source_path, destination_root):
    """
    Copies the folder from source to destination using copytree.
    """
    # Create the full destination path (e.g., .../games/unity/bitplanes)
    final_dest = os.path.join(destination_root, game_name)

    if os.path.exists(final_dest):
        print(f"⚠️ SKIPPING: {game_name} (Already exists in destination)")
        return

    print(f"🚀 COPYING: {game_name} -> {destination_root}...")
    try:
        # copytree copies the folder and all subfolders/files
        shutil.copytree(source_path, final_dest)
        print(f"✅ SUCCESS: {game_name}")
    except Exception as e:
        print(f"❌ ERROR copying {game_name}: {e}")

def main():
    # 1. Ensure destination folders exist
    if not os.path.exists(DEST_UNITY):
        os.makedirs(DEST_UNITY)
    if not os.path.exists(DEST_GODOT):
        os.makedirs(DEST_GODOT)

    print(f"📂 Scanning Source: {SOURCE_DIR}\n")

    # 2. Iterate through every folder in the source directory
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ CRITICAL ERROR: Source directory not found: {SOURCE_DIR}")
        return

    games_found = 0
    unity_count = 0
    godot_count = 0

    for item in os.listdir(SOURCE_DIR):
        full_path = os.path.join(SOURCE_DIR, item)

        # We only care about directories (folders), not random files
        if os.path.isdir(full_path):
            engine = identify_game_engine(full_path)

            if engine == 'unity':
                copy_game(item, full_path, DEST_UNITY)
                unity_count += 1
            elif engine == 'godot':
                copy_game(item, full_path, DEST_GODOT)
                godot_count += 1
            else:
                print(f"⚪ IGNORING: {item} (Unknown Engine or HTML5)")
            
            games_found += 1

    print("-" * 50)
    print(f"🎉 OPERATION COMPLETE")
    print(f"Total Folders Scanned: {games_found}")
    print(f"Unity Games Copied:    {unity_count}")
    print(f"Godot Games Copied:    {godot_count}")
    print("-" * 50)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
