import re
import os
import sys

# CONFIGURATION
INPUT_FILE = "testing.html"
OUTPUT_FILE = "testing_fixed.html"

def process_html():
    # Ensure we are looking in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, INPUT_FILE)
    output_path = os.path.join(script_dir, OUTPUT_FILE)

    print(f"📂 Looking for file at: {input_path}")
    
    try:
        if not os.path.exists(input_path):
            print(f"❌ ERROR: Could not find '{INPUT_FILE}'.")
            print("   Make sure this python script is in the SAME folder as testing.html!")
            input("\nPress Enter to exit...")
            return

        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex Pattern to find game cards
        pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"(?:[^>]*?\s+)?class="([^"]*game-card[^"]*)"(?:[^>]*?)>(.*?)</a>'
        
        def replacement(match):
            url = match.group(1)
            class_name = match.group(2)
            inner_html = match.group(3)

            clean_path = None

            # Case 1: Standard games repo links
            if "games.macbooksuck.xyz/games/" in url:
                clean_path = url.split("games.macbooksuck.xyz/")[1]

            # Case 2: Local links (already relative)
            elif url.startswith("/games/") or "macbooksuck.xyz/games/" in url:
                if "macbooksuck.xyz" in url:
                    clean_path = url.split("macbooksuck.xyz/")[1]
                else:
                    clean_path = url.lstrip("/")

            # Clean up the path
            if clean_path:
                clean_path = clean_path.replace("index.html", "").rstrip("/")
                return f'<div class="{class_name}" onclick="openGame(\'{clean_path}\')" style="cursor: pointer;">{inner_html}</div>'
            else:
                return match.group(0)

        # Run the replacement
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("-" * 40)
        print(f"✅ Success! Created '{OUTPUT_FILE}'")
        print("-" * 40)

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    process_html()
    # This line keeps the window open!
    input("\nPress Enter to close this window...")
