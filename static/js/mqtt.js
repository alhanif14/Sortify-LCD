function startMqtt() {
    console.log("Paho sudah siap. Memulai koneksi MQTT...");

    // Konfigurasi koneksi
    const brokerHost = "broker.emqx.io";
    const brokerPort = 8083;
    const clientId = "sortify-client-" + Math.random().toString(16).substr(2, 8);

    // Langsung gunakan window.Paho karena dijamin sudah ada
  const client = new window.Paho.MQTT.Client(brokerHost, brokerPort, clientId);

    // Pemetaan dari topik MQTT ke ID elemen di HTML
    const topicToIdMap = {
        "waste/sensor1": "count1",
        "waste/sensor2": "count2",
        "waste/sensor3": "count3",
        "waste/sensor4": "count4"
    };

    // Fungsi callback saat ada pesan masuk
    client.onMessageArrived = function (message) {
        const topic = message.destinationName;
        const payload = message.payloadString;
        console.log(`Pesan MQTT Diterima: Topik=${topic}, Data=${payload}`);

        const elementId = topicToIdMap[topic];
        if (elementId) {
            const value = parseInt(payload);
            if (!isNaN(value)) {
                // Panggil fungsi global dari initCountUp.js untuk update UI
                window.updateAvailability(elementId, value);
            } else {
                console.error(`Data tidak valid diterima dari MQTT: ${payload}`);
            }
        }
    };

    // Fungsi callback saat koneksi terputus
    client.onConnectionLost = function (responseObject) {
        if (responseObject.errorCode !== 0) {
            console.error("Koneksi MQTT terputus:", responseObject.errorMessage);
        }
    };

    // Mulai proses koneksi
    client.connect({
        onSuccess: () => {
            console.log("Berhasil terhubung ke Broker MQTT!");
            for (const topic in topicToIdMap) {
                console.log(`Berlangganan ke topik: ${topic}`);
                client.subscribe(topic, { qos: 0 });
            }
        },
        onFailure: (err) => {
            console.error("Gagal terhubung ke MQTT:", err.errorMessage);
        },
        useSSL: true
    });
}