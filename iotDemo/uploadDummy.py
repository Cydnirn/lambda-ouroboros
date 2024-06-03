import ssl
import random
import json
import os
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# Configuration
broker_url = "a1138tbftbjhbs-ats.iot.ap-southeast-2.amazonaws.com"
broker_port = 8883
topic = "/esp32/temp"
client_id = "mqtt_client_id"

# Paths to certificate files
auth_folder = "auth"
ca_cert = os.path.join(auth_folder, "ca.pem")         
cert_file = os.path.join(auth_folder, "certificate.crt")
key_file = os.path.join(auth_folder, "private.key")

# Generate data


def generate_data():
    data = {
        "location": "Jakarta",
        "temp": random.randint(30, 45),
        "time": datetime.now().isoformat()
    }
    return data

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, props):
    print(f"Connected with result code {rc}")
    if rc == 0:
        data = generate_data()
        client.publish(topic, json.dumps(data), qos=1)
        print(f"Published: {data}")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_publish(client, userdata, mid, rc, props):
    print("Message Published")

# Create MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id, None, None, mqtt.MQTTv311)
client.on_connect = on_connect
client.on_publish = on_publish

# Configure TLS Set
client.tls_set(ca_certs=ca_cert, certfile=cert_file, keyfile=key_file, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.tls_insecure_set(False)

# Connect to Broker and Publish
client.connect(broker_url, broker_port, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_start()
try:
    while True:
        data = generate_data()
        client.publish(topic, json.dumps(data), qos=1)
        print(f"Published: {data}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
    exit(0)

