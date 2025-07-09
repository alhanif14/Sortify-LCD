import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
import qrcode
import os
import json

# Path simpan QR code (relatif ke file ini)
output_folder = os.path.join(os.path.dirname(__file__), "../static/qr-code")
output_folder = os.path.abspath(output_folder)
os.makedirs(output_folder, exist_ok=True)

# Koneksi ke PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="sortify_db",
    user="postgres",
    password="H140604:)"
)
cur = conn.cursor()

detecting = False
detected_waste_types = []

waste_point_map = {
    "plastic": 40,
    "paper": 40,
    "organic": 30,
    "other": 10
}

def generate_qr(waste_id, timestamp, waste_list, total_point):
    filename = f"waste_{waste_id}.png"
    qr_data = {
        "id": waste_id,
        "timestamp": str(timestamp),
        "waste_type": waste_list,
        "point": total_point
    }
    qr_json = json.dumps(qr_data, indent=2)
    qr = qrcode.make(qr_json)
    qr_path = os.path.join(output_folder, filename)
    qr.save(qr_path)
    return filename

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT Broker!")
    client.subscribe("waste/raw")

def on_message(client, userdata, msg):
    global detecting, detected_waste_types

    payload = msg.payload.decode().strip().lower()

    if payload == "start":
        detecting = True
        detected_waste_types = []
        print("🚀 Deteksi dimulai.")

    elif payload == "stop":
        if detecting:
            detecting = False
            if detected_waste_types:
                timestamp = datetime.now()
                waste_str = ", ".join(detected_waste_types)
                total_point = sum(waste_point_map.get(w, 0) for w in detected_waste_types)

                # Simpan ke DB
                cur.execute(
                    "INSERT INTO waste_detection_log (timestamp, waste_type, point) VALUES (%s, %s, %s) RETURNING id",
                    (timestamp, waste_str, total_point)
                )
                waste_id = cur.fetchone()[0]

                qr_filename = generate_qr(waste_id, timestamp, detected_waste_types, total_point)

                cur.execute(
                    "UPDATE waste_detection_log SET qr_code = %s WHERE id = %s",
                    (qr_filename, waste_id)
                )
                conn.commit()

                print(f"✅ Data disimpan | Sampah: {waste_str} | Point: {total_point} | QR: {qr_filename}")
            else:
                print("⚠️ Tidak ada jenis sampah yang terdeteksi.")
        else:
            print("❌ Stop diterima tapi deteksi belum dimulai.")

    else:
        if detecting:
            if payload in waste_point_map:
                detected_waste_types.append(payload)
                print(f"🟢 Jenis sampah terdeteksi: {payload}")
            else:
                print(f"⚪ Diabaikan: {payload}")
        else:
            print(f"🔸 Pesan diterima di luar status deteksi: {payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)
client.loop_forever()
