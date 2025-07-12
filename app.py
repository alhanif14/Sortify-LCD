from fasthtml.common import *
from routes.landing import landing_section, landing_routes
from routes.start import start_routes
from routes.how import how_routes
from routes.avail import avail_routes
from routes.success import success_routes
from routes.barcode import barcode_routes
from routes.preload import preload_routes
from routes.mqtt_client import set_last_mqtt_result  # ✅ Tambahkan ini
import uvicorn, threading, os
from dotenv import load_dotenv
load_dotenv()

# --------------------------
# FASTHTML APP
# --------------------------
app, rt = fast_app(live=True, pico=False)
landing_routes(rt)
start_routes(rt)
how_routes(rt)
avail_routes(rt)
success_routes(rt)
barcode_routes(rt)
preload_routes(rt)

def main_content():
    return Div(
        landing_section(),
        cls="main pt-4",
        id="mainContent",
    )

@rt("/")
def landing():
    return Html(
        Head(
            Title("Sortify"),
            Link(href="/static/css/style.css", rel="stylesheet"),
            Link(href="/static/css/landing.css", rel="stylesheet"),
            Link(href="/static/css/avail.css", rel="stylesheet"),
            Link(href="/static/css/how.css", rel="stylesheet"),
            Link(href="/static/css/start.css", rel="stylesheet"),
            Link(href="/static/css/success.css", rel="stylesheet"),
            Link(href="/static/css/barcode.css", rel="stylesheet"),
            Link(href="/static/css/preload.css", rel="stylesheet"),
            Link(href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@300;600&display=swap", rel="stylesheet"),
            Link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"),
            Link(href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded", rel="stylesheet"),
            Script(type="module", src="/static/js/countUp.min.js"),
            Script(type="module", src="/static/js/initCountUp.js"),
            Script(src="/static/js/paho-mqtt.js", defer=True),
            Script(src="/static/js/mqtt.js", defer=True),
            Script("""if (!window.Paho || !window.Paho.MQTT) { console.error("Paho MQTT belum dimuat"); } else { console.log("Paho MQTT sudah dimuat"); }"""),
            Script(type="module", src="/static/js/script.js"),
            Script(src="https://unpkg.com/htmx.org@1.9.12", defer=True),
        ),
        Body(main_content()),
    )

# --------------------------
# MQTT SCRIPT (INLINE)
# --------------------------
def run_mqtt_script():
    import paho.mqtt.client as mqtt
    import psycopg2
    from datetime import datetime
    import qrcode
    import json

    waste_point_map = {"plastic": 40, "paper": 40, "organic": 30, "other": 10}
    detecting = False
    detected = []

    output_folder = os.path.abspath("static/qr-code")
    os.makedirs(output_folder, exist_ok=True)

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    def generate_qr(waste_id, timestamp, waste_list, total_point):
        filename = f"waste_{waste_id}.png"
        qr_data = {
            "id": waste_id,
            "timestamp": str(timestamp),
            "waste_type": waste_list,
            "point": total_point
        }
        qr = qrcode.make(json.dumps(qr_data, indent=2))
        path = os.path.join(output_folder, filename)
        qr.save(path)
        return filename

    def on_connect(client, userdata, flags, rc):
        print("✅ Connected to MQTT Broker!")
        client.subscribe("waste/raw")

    def on_message(client, userdata, msg):
        nonlocal detecting, detected
        payload = msg.payload.decode().strip().lower()

        if payload == "start":
            detecting = True
            detected = []
            print("🚀 Deteksi dimulai.")
        elif payload == "stop":
            if detecting:
                detecting = False
                if detected:
                    timestamp = datetime.now()
                    waste_str = ", ".join(detected)
                    total_point = sum(waste_point_map.get(w, 0) for w in detected)

                    cur.execute(
                        "INSERT INTO waste_detection_log (timestamp, waste_type, point) VALUES (%s, %s, %s) RETURNING id",
                        (timestamp, waste_str, total_point)
                    )
                    waste_id = cur.fetchone()[0]

                    qr_filename = generate_qr(waste_id, timestamp, detected, total_point)

                    cur.execute(
                        "UPDATE waste_detection_log SET qr_code = %s WHERE id = %s",
                        (qr_filename, waste_id)
                    )
                    conn.commit()

                    print(f"✅ Data disimpan | Sampah: {waste_str} | Point: {total_point} | QR: {qr_filename}")
                else:
                    print("⚠️ Tidak ada jenis sampah yang terdeteksi.")
        else:
            if detecting:
                if payload in waste_point_map:
                    detected.append(payload)
                    set_last_mqtt_result(payload)  # ✅ Set result ke global
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

# Jalankan MQTT script di thread terpisah
threading.Thread(target=run_mqtt_script, daemon=True).start()

# Jalankan app FastHTML
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
