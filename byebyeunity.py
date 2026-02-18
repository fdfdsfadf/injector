from pathlib import Path

OLD_SCRIPT = """<script>
(function () {
  const GAME_ID = location.pathname;
  const SAVE_KEY = "engine_save_v1";

  async function loadSave() {
    if (!window.parent?.cloudLoad) return;
    const save = await window.parent.cloudLoad(GAME_ID);
    if (!save) return;

    if (typeof FS !== "undefined") {
      FS.syncfs(true, () =>
        console.log("[CloudSave] Engine save restored")
      );
    }
  }

  window.addEventListener("beforeunload", () => {
    if (!window.parent?.cloudSave) return;
    window.parent.cloudSave(GAME_ID, { [SAVE_KEY]: true });
  });

  loadSave();
})();
</script>"""

removed = 0

for index in Path(".").rglob("index.html"):
    text = index.read_text(encoding="utf-8", errors="ignore")

    if OLD_SCRIPT in text:
        text = text.replace(OLD_SCRIPT, "")
        index.write_text(text, encoding="utf-8")
        print("Removed Unity/Godot bridge from:", index)
        removed += 1

print("Done. Removed from", removed, "files.")
