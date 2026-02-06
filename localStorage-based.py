from pathlib import Path
import re

HTML5_BRIDGE = """
<script>
(function () {
  const ALLOWED_PARENTS = ["https://main1.macbooksuck.xyz"];
  const gameId = location.hostname + location.pathname;

  window.addEventListener("message", (event) => {
    if (!ALLOWED_PARENTS.includes(event.origin)) return;
    if (event.data?.type !== "LOAD_SAVE") return;

    const save = event.data.payload;
    if (!save) return;

    Object.entries(save).forEach(([k, v]) => {
      localStorage.setItem(k, v);
    });

    console.log("[Bridge] HTML5 save restored");
  });

  const originalSet = localStorage.setItem;
  localStorage.setItem = function (key, value) {
    originalSet.apply(this, arguments);
    if (window.parent?.cloudSave) {
      window.parent.cloudSave(gameId, { [key]: value });
    }
  };
})();
</script>
"""

REMOVE_PATTERNS = [
    r"window\.addEventListener\([\s\S]*?\);",
    r"localStorage\.setItem\s*=\s*function[\s\S]*?\};",
    r"postMessage\([\s\S]*?\);",
    r"GAME_SAVE",
    r"LOAD_SAVE",
]

root = Path("games")

for html in root.rglob("*.html"):
    text = html.read_text(encoding="utf-8", errors="ignore")

    if "HTML5 save restored" in text:
        continue  # already migrated

    original = text

    for pattern in REMOVE_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)

    if "</body>" in text:
        text = text.replace("</body>", HTML5_BRIDGE + "\n</body>")

    if text != original:
        html.write_text(text, encoding="utf-8")
        print(f"[HTML5] Updated {html}")

print("✅ HTML5 migration complete")
