# import threading
# import paho.mqtt.client as mqtt

# MQTT_BROKER = "broker.emqx.io"
# MQTT_PORT = 1883
# MQTT_KEEPALIVE = 60

# _last_mqtt_result = None
# _lock = threading.Lock()

# client = mqtt.Client()

# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT broker with result code " + str(rc))
#     client.subscribe("waste/raw")

# def on_message(client, userdata, msg):
#     global _last_mqtt_result
#     payload = msg.payload.decode('utf-8')
#     print(f"MQTT received message: {payload}")
#     with _lock:
#         _last_mqtt_result = payload

# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
# client.loop_start()

# def mqtt_publish(topic: str, message: str):
#     client.publish(topic, message)

# def get_last_mqtt_result():
#     with _lock:
#         return _last_mqtt_result

# def reset_last_mqtt_result():
#     global _last_mqtt_result
#     with _lock:
#         _last_mqtt_result = None
