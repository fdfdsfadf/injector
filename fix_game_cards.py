import re

# FILE CONFIGURATION
INPUT_FILE = "testing.html"
OUTPUT_FILE = "testing_fixed.html"

def process_html():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex explanation:
        # We look for <a href="..." class="game-card"> ... </a>
        # We capture the URL inside href
        # We capture the inner HTML (title, subtitles, badges)
        
        # Pattern looks for: <a href="(URL)" ... class="game-card" ...>(INNER_CONTENT)</a>
        # Note: This is a simple regex for your specific file structure. 
        pattern = r'<a\s+href="([^"]+)"\s+class="game-card"(?:[^>]*)>(.*?)</a>'
        
        def replacement(match):
            url = match.group(1)
            inner_html = match.group(2)
            
            # LOGIC: Extract the 'game path' from the URL
            # Example: https://games.macbooksuck.xyz/games/bit-planes/ -> games/bit-planes
            
            if "games.macbooksuck.xyz" in url:
                # Remove the domain prefix
                clean_path = url.replace("https://games.macbooksuck.xyz/", "")
                # Remove trailing slash and index.html if present
                clean_path = clean_path.replace("/index.html", "").rstrip("/")
                
                # Create the new DIV tag with onclick
                return f'<div class="game-card" onclick="openGame(\'{clean_path}\')" style="cursor: pointer;">{inner_html}</div>'
            
            elif "macbooksuck.xyz" in url and "/games/" in url:
                 # Handle main domain links if they follow the same structure
                clean_path = url.split("macbooksuck.xyz/")[1].rstrip("/")
                return f'<div class="game-card" onclick="openGame(\'{clean_path}\')" style="cursor: pointer;">{inner_html}</div>'
            
            else:
                # If it's an external link (like Discord or Movie Hub), leave it as an <a> tag
                return match.group(0)

        # Apply the replacement
        # flags=re.DOTALL allows the dot (.) to match newlines (since your cards span multiple lines)
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Success! Created '{OUTPUT_FILE}' with updated game cards.")
        print("You can now rename 'testing_fixed.html' to 'index.html'.")

    except FileNotFoundError:
        print(f"❌ Error: Could not find '{INPUT_FILE}'. Make sure it's in the same folder.")

if __name__ == "__main__":
    process_html()
