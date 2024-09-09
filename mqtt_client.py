import paho.mqtt.client as mqtt

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to multiple topics
    topics = [("subscribe/ilyasmali", 0), ("subscribe/topic1", 0), ("subscribe/topic2", 0)]
    for topic, qos in topics:
        client.subscribe(topic, qos)
        print(f"Subscribed to topic: {topic}")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

# Initialize the client instance with TLS/SSL
client = mqtt.Client()

# TLS settings - bypassing certificate verification (use only for testing)
client.tls_insecure_set(False)

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the broker with MQTTS port
broker_address = "broker.emqx.io"  # Replace with your broker address if different
client.connect(broker_address, 8883, 60)

# Start the loop
client.loop_start()

# Publish test messages to multiple topics
publish_topics = ["publish/ilyasmali", "publish/topic1", "publish/topic2"]
for topic in publish_topics:
    client.publish(topic, f"Hello MQTT from {topic}")

# Wait for user to quit
input("Press Enter to quit...")

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()
