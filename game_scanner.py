import os

def scan_for_games(root_dir):
    unity_games = []
    godot_games = []

    print(f"🔎 Scanning directory: {root_dir}...\n")

    # Walk through every folder and subfolder
    for current_folder, dirs, files in os.walk(root_dir):
        
        is_unity = False
        is_godot = False
        
        # --- 1. DETECT GODOT ---
        # Godot web builds almost always have a .pck file
        for file in files:
            if file.endswith('.pck'):
                is_godot = True
                break

        # --- 2. DETECT UNITY ---
        # Unity WebGL usually has a 'Build' folder and a 'TemplateData' folder
        # Or files ending in .unityweb
        if not is_godot:
            if "Build" in dirs:
                # Check inside the Build folder to be sure
                try:
                    build_path = os.path.join(current_folder, "Build")
                    build_files = os.listdir(build_path)
                    for bf in build_files:
                        if bf.endswith(".loader.js") or bf.endswith(".framework.js") or bf.endswith(".data"):
                            is_unity = True
                            break
                except Exception:
                    pass
            
            # Check for older Unity versions in the root file list
            for file in files:
                if file.endswith(".unityweb") or "UnityLoader.js" in file:
                    is_unity = True
                    break

        # --- 3. STORE RESULTS ---
        # We store the relative path to make it easier to read
        rel_path = os.path.relpath(current_folder, root_dir)
        
        if is_unity:
            unity_games.append(rel_path)
        elif is_godot:
            godot_games.append(rel_path)

    return unity_games, godot_games

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Default to current directory if user just hits enter
    target_dir = input("Paste the path to your 'games' folder (or press Enter for current folder): ").strip()
    
    # Remove quotes if Windows added them
    target_dir = target_dir.replace('"', '')
    
    if not target_dir:
        target_dir = "."

    if os.path.exists(target_dir):
        unity, godot = scan_for_games(target_dir)

        print("-" * 40)
        print(f"🎮 FOUND {len(unity)} UNITY WEBGL GAMES:")
        print("-" * 40)
        for game in unity:
            print(f" [Unity] {game}")

        print("\n" + "-" * 40)
        print(f"🤖 FOUND {len(godot)} GODOT GAMES:")
        print("-" * 40)
        for game in godot:
            print(f" [Godot] {game}")
            
        print("\n✅ Scan Complete.")
    else:
        print("❌ Error: Directory not found.")

    input("\nPress Enter to exit...")
