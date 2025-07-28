function waitForPaho(callback, interval = 100, timeout = 5000) {
  const start = Date.now();
  (function check() {
    console.log("Check Paho MQTT...", window.Paho);
    if (window.Paho && window.Paho.Client && window.Paho.Message) {
      callback();
    } else if (Date.now() - start > timeout) {
      console.error("Timeout: Paho MQTT not loaded after 5 seconds.");
    } else {
      setTimeout(check, interval);
    }
  })();
}

waitForPaho(() => {
  const client = new window.Paho.Client(
    "broker.emqx.io",
    8083,
    "clientId" + Math.random()
  );

  client.onMessageArrived = function (message) {
    const data = message.payloadString.toLowerCase();
    console.log("MQTT message received:", data);

    if (["paper", "plastic", "organic", "other"].includes(data)) {
      console.log("Valid data detected, navigating to /success...");
      const target = document.getElementById("mainContent");
      if (target) {
        htmx.ajax("GET", "/success", {
          target: "#mainContent",
          swap: "innerHTML",
        });
      } else {
        window.location.href = "/success";
      }
    }
  };

  client.connect({
    onSuccess: () => {
      console.log("MQTT connected");
      client.subscribe("waste/raw");
    },
    onFailure: (err) => {
      console.error("Gagal connect MQTT:", err);
    },
  });

  document.body.addEventListener("go-success", () => {
    console.log("go-success event received");
    const pollDiv = document.getElementById("mqtt-poll");
    if (pollDiv) {
      pollDiv.removeAttribute("hx-trigger");
    }
    htmx.ajax("GET", "/success", { target: "#mainContent", swap: "innerHTML" });
  });
});