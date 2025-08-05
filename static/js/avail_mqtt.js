function initializeGlobalAvailabilityMQTT() {
    console.log("Initializing Global MQTT for Availability...");

    if (window.availMqttClient && window.availMqttClient.isConnected()) {
        console.log("Global MQTT Connection already established.");
        return;
    }

    waitForPaho(() => {
        console.log("Paho library ready for MQTT.");

        const client = new window.Paho.Client(
            "broker.emqx.io", 8084, "/mqtt",
            "avail_client_" + Math.random().toString(16).substr(2, 8)
        );
        window.availMqttClient = client;

        const topicMap = {
            "waste/sensor1": "count1",
            "waste/sensor2": "count2",
            "waste/sensor3": "count3",
            "waste/sensor4": "count4"
        };

        client.onMessageArrived = function (message) {
            const topic = message.destinationName;
            const value = parseInt(message.payloadString, 10);
            const elementId = topicMap[topic];

            if (!elementId || isNaN(value)) return;

            console.log(`[MQTT] ${topic} -> ${value}`);

            localStorage.setItem(`avail_${elementId}`, value);

            if (document.querySelector(".avail-page-content") && window.updateAvailabilityUI) {
                window.updateAvailabilityUI(elementId, value);
            }
        };

        client.connect({
            useSSL: true,
            onSuccess: () => {
                console.log("Global MQTT Connection Successful for Availability!");
                for (const topic in topicMap) {
                    client.subscribe(topic, { qos: 0 });
                }
            },
            onFailure: (err) => console.error("MQTT Connection Failed:", err)
        });
    });
}

function waitForPaho(callback) {
    if (window.Paho && window.Paho.Client) {
        callback();
    } else {
        setTimeout(() => waitForPaho(callback), 100);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initializeGlobalAvailabilityMQTT();
});
