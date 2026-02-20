RESPONDER_SNIPPET = """<script>
(function () {

  const PARENT_ORIGIN_MATCH = "macbooksuck.xyz";

  function allowedParent(origin) {
    return origin && origin.includes(PARENT_ORIGIN_MATCH);
  }

  function sendToParent(message) {
    parent.postMessage(message, "*");
  }

  async function exportSave() {

    if (typeof FS !== "undefined") {
      try {
        const filePath = "/idbfs/PlayerPrefs";
        const stat = FS.stat(filePath);
        const stream = FS.open(filePath, "r");
        const buffer = new Uint8Array(stat.size);

        FS.read(stream, buffer, 0, stat.size, 0);
        FS.close(stream);

        const base64 = btoa(
          String.fromCharCode.apply(null, Array.from(buffer))
        );

        sendToParent({
          type: "EXPORT_SAVE",
          gameId: location.pathname,
          payload: {
            type: "unity",
            unity_save_file_v1: base64
          }
        });

        console.log("[Game] Unity/Godot save exported");
        return;
      } catch (e) {
        console.warn("[Game] Unity export failed:", e);
      }
    }

    try {
      const data = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        data[key] = localStorage.getItem(key);
      }

      sendToParent({
        type: "EXPORT_SAVE",
        gameId: location.pathname,
        payload: {
          type: "html5",
          storage: data
        }
      });

      console.log("[Game] HTML5 localStorage exported");
      return;

    } catch (e) {
      console.error("[Game] HTML5 export failed:", e);
    }

    sendToParent({
      type: "EXPORT_SAVE",
      gameId: location.pathname,
      payload: { type: "none" }
    });
  }

  async function importSave(payload) {

    if (!payload) return;

    if (payload.type === "unity" && payload.unity_save_file_v1 && typeof FS !== "undefined") {
      try {
        const binary = atob(payload.unity_save_file_v1);
        const bytes = new Uint8Array(binary.length);

        for (let i = 0; i < binary.length; i++) {
          bytes[i] = binary.charCodeAt(i);
        }

        const filePath = "/idbfs/PlayerPrefs";
        const stream = FS.open(filePath, "w+");

        FS.write(stream, bytes, 0, bytes.length, 0);
        FS.close(stream);

        FS.syncfs(false, function () {
          console.log("[Game] Unity/Godot save restored");
          alert("Cloud save restored. Reload the game.");
        });

        return;
      } catch (e) {
        console.error("[Game] Unity import failed:", e);
      }
    }

    if (payload.type === "html5" && payload.storage) {
      try {
        Object.entries(payload.storage).forEach(([k, v]) => {
          localStorage.setItem(k, v);
        });

        console.log("[Game] HTML5 save restored");
        alert("Cloud save restored. Reload the game.");
        return;

      } catch (e) {
        console.error("[Game] HTML5 import failed:", e);
      }
    }
  }

  window.addEventListener("message", function (event) {

    if (!allowedParent(event.origin)) return;

    const data = event.data || {};

    if (data.type === "REQUEST_EXPORT_SAVE") {
      exportSave();
    }

    if (data.type === "IMPORT_SAVE") {
      importSave(data.payload);
    }

  });

  console.log("[Game] Cloud save responder installed");

})();
</script>"""
