import json
import base64
import os
from urllib.parse import urlparse

HAR_FILE = "game.har"   # rename your HAR file to this
OUTPUT_DIR = "output"

with open(HAR_FILE, "r", encoding="utf8") as f:
    har = json.load(f)

for entry in har["log"]["entries"]:
    req = entry.get("request", {})
    res = entry.get("response", {})
    content = res.get("content", {})

    url = req.get("url")
    if not url:
        continue

    body = content.get("text")
    if not body:
        continue

    # Determine file path from URL
    path = urlparse(url).path.lstrip("/")
    if not path or path.endswith("/"):
        continue

    # Decode content
    if content.get("encoding") == "base64":
        data = base64.b64decode(body)
    else:
        data = body.encode("utf8")

    # Create folders
    full_path = os.path.join(OUTPUT_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Write file
    with open(full_path, "wb") as f:
        f.write(data)

print("Done! Extracted files are in the 'output' folder.")
