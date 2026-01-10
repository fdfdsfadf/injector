import re
import os

# CONFIGURATION
INPUT_FILE = "testing.html"
OUTPUT_FILE = "testing_fixed.html"

def process_html():
    print(f"📂 Reading {INPUT_FILE}...")
    
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex Explanation:
        # 1. We look for an <a tag.
        # 2. It must have an href="..." (Group 1).
        # 3. It must have a class that contains "game-card" (Group 2) - this handles 'game-card new-card' etc.
        # 4. We capture everything inside the tag >...</a> (Group 3).
        
        pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"(?:[^>]*?\s+)?class="([^"]*game-card[^"]*)"(?:[^>]*?)>(.*?)</a>'
        
        def replacement(match):
            url = match.group(1)
            class_name = match.group(2)
            inner_html = match.group(3)

            # --- LOGIC: Which links do we convert? ---
            
            clean_path = None

            # Case 1: Standard games repo links
            # Ex: https://games.macbooksuck.xyz/games/bit-planes/
            if "games.macbooksuck.xyz/games/" in url:
                clean_path = url.split("games.macbooksuck.xyz/")[1] # gets "games/bit-planes/"

            # Case 2: Local links (already relative)
            # Ex: /games/proxy/
            elif url.startswith("/games/") or "macbooksuck.xyz/games/" in url:
                if "macbooksuck.xyz" in url:
                    clean_path = url.split("macbooksuck.xyz/")[1]
                else:
                    clean_path = url.lstrip("/")

            # Clean up the path (remove index.html, trailing slashes)
            if clean_path:
                clean_path = clean_path.replace("index.html", "").rstrip("/")
                
                # RETURN THE NEW DIV
                # We keep the original classes (like 'game-card hot') so styling stays perfect
                return f'<div class="{class_name}" onclick="openGame(\'{clean_path}\')" style="cursor: pointer;">{inner_html}</div>'

            else:
                # Case 3: External links (Discord, Forms, Movie Hub, Emulators on subdomains)
                # We do NOT change these, so they still open in new tabs/windows normally.
                return match.group(0)

        # Run the replacement
        # re.DOTALL is crucial so the regex matches across multiple lines
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

        # Write the result
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("-" * 40)
        print(f"✅ Success! Generated '{OUTPUT_FILE}'")
        print(f"🔗 Game cards have been converted to <div> tags with openGame().")
        print(f"🌍 External links (Discord, Movies) were left as <a> tags.")
        print("-" * 40)
        print("NEXT STEPS:")
        print("1. Open 'testing_fixed.html' in your browser to verify.")
        print("2. Rename it to 'index.html' when ready.")

    except FileNotFoundError:
        print(f"❌ Error: Could not find '{INPUT_FILE}' in this folder.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    process_html()
