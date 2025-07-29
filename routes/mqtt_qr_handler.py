import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
import qrcode
import os
import json
import threading
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("Error: DATABASE_URL environment variable is not set.")

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883

output_folder = os.path.join(os.path.dirname(__file__), "../static/qr-code")
output_folder = os.path.abspath(output_folder)
os.makedirs(output_folder, exist_ok=True)

detecting = False
detected_waste_types = []
lock = threading.Lock()

waste_point_map = {
    "plastic": 40,
    "paper": 40,
    "organic": 30,
    "other": 10
}

client = mqtt.Client(client_id=f"db_handler_{os.getpid()}")

def mqtt_publish(topic: str, message: str):
    client.publish(topic, message)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

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
    print("Database Handler: Connected to MQTT Broker!")
    client.subscribe("waste/raw")

def on_message(client, userdata, msg):
    global detecting, detected_waste_types

    payload = msg.payload.decode().strip().lower()
    print(f"Database Handler: Message received '{payload}'")

    with lock:
        if payload == "start":
            detecting = True
            detected_waste_types = []
            print("Database Handler: Detection started.")

        elif payload == "stop":
            if detecting:
                detecting = False
                if detected_waste_types:
                    timestamp = datetime.now()
                    waste_str = ", ".join(detected_waste_types)
                    total_point = sum(waste_point_map.get(w, 0) for w in detected_waste_types)
                    
                    conn = get_db_connection()
                    cur = conn.cursor()

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
                    cur.close()
                    conn.close()

                    print(f"Database Handler: Data saved | waste: {waste_str} | Point: {total_point} | QR: {qr_filename}")
                else:
                    print("Database Handler: 'stop' received but no waste was detected.")
        
        elif payload in waste_point_map:
            if detecting:
                detected_waste_types.append(payload)
                print(f"Database Handler: Waste type detected: {payload}")

def start_database_mqtt_listener():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    print("Database MQTT listener has started in the background.")