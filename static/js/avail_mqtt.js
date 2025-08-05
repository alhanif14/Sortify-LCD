function initializeAvailabilityMQTT() {
    console.log("Initializing MQTT for Availability page...");

    if (window.mqttClient && window.mqttClient.isConnected()) {
        console.log("MQTT Connection already established.");
        return;
    }

    waitForPaho(() => {
        console.log("Paho library ready for MQTT.");
        const client = new window.Paho.Client(
            "broker.emqx.io", 8084, "/mqtt",
            "avail_client_" + Math.random().toString(16).substr(2, 8)
        );
        window.mqttClient = client;

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
            console.log(`MQTT message received: ${topic} -> ${value}`);

            if (elementId && !isNaN(value) && window.updateAvailabilityUI) {
                localStorage.setItem(`avail_${elementId}`, value);
                window.updateAvailabilityUI(elementId, value);
            }
        };

        client.connect({
            useSSL: true,
            onSuccess: () => {
                console.log("MQTT Connection Successful for Availability!");
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

document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.querySelector(".avail-page-content")) {
        console.log("Event htmx:afterSwap detected for Avail page.");
        initializeAvailabilityMQTT();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector(".avail-page-content")) {
        console.log("Event DOMContentLoaded detected for Avail page.");
        initializeAvailabilityMQTT();
    }
});
