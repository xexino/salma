import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import ssl

class MQTTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTTS Client")

        # Initialize MQTT Client
        self.client = None

        # Store topics for subscribing and publishing
        self.subscribe_topics = []
        self.publish_topics = []

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        self.connect_button = ttk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.pack(pady=10)

        self.subscribe_label = ttk.Label(self.root, text="Topic to Subscribe:")
        self.subscribe_label.pack()
        self.subscribe_entry = ttk.Entry(self.root)
        self.subscribe_entry.pack()

        self.subscribe_button = ttk.Button(self.root, text="Subscribe", command=self.subscribe)
        self.subscribe_button.pack(pady=10)

        self.publish_label = ttk.Label(self.root, text="Topic to Publish:")
        self.publish_label.pack()
        self.publish_entry = ttk.Entry(self.root)
        self.publish_entry.pack()

        self.publish_message_label = ttk.Label(self.root, text="Message to Publish:")
        self.publish_message_label.pack()
        self.publish_message_entry = ttk.Entry(self.root)
        self.publish_message_entry.pack()

        self.publish_button = ttk.Button(self.root, text="Publish", command=self.publish)
        self.publish_button.pack(pady=10)

        self.disconnect_button = ttk.Button(self.root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(pady=10)

        self.log = tk.Text(self.root, height=15, width=60)
        self.log.pack(pady=10)

    def connect(self):
        if self.client is not None:
            self.disconnect()

        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        
        # Set MQTT Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        broker_address = "broker.emqx.io"  # Replace with your broker address
        port = 8883  # MQTTS port

        try:
            self.client.tls_set(
                ca_certs=None,  # Use system default CA certs
                tls_version=ssl.PROTOCOL_TLS,
                cert_reqs=ssl.CERT_REQUIRED
            )
            self.client.tls_insecure_set(True)  # Bypass certificate verification for testing

            self.client.connect(broker_address, port, 60)
            self.client.loop_start()
            self.log.insert(tk.END, "Connecting to broker...\n")
        except Exception as e:
            self.log.insert(tk.END, f"Connection failed: {str(e)}\n")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.log.insert(tk.END, "Connected successfully\n")
            for topic in self.subscribe_topics:
                self.client.subscribe(topic)
                self.log.insert(tk.END, f"Subscribed to topic: {topic}\n")
        else:
            self.log.insert(tk.END, f"Connection failed with code {rc}\n")

    def subscribe(self):
        topic = self.subscribe_entry.get()
        if topic:
            self.subscribe_topics.append(topic)
            if self.client is not None:
                self.client.subscribe(topic)
                self.log.insert(tk.END, f"Subscribed to topic: {topic}\n")
            else:
                self.log.insert(tk.END, "Not connected. Please connect first.\n")

    def on_message(self, client, userdata, msg):
        self.log.insert(tk.END, f"Message received: {msg.topic}: {msg.payload.decode()}\n")

    def publish(self):
        topic = self.publish_entry.get()
        message = self.publish_message_entry.get()
        if not self.client:
            self.log.insert(tk.END, "Not connected. Please connect first.\n")
            return
        if topic and message:
            self.client.publish(topic, message)
            self.log.insert(tk.END, f"Message published to {topic}: {message}\n")

    def disconnect(self):
        if self.client is None:
            return
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.log.insert(tk.END, "Disconnected\n")
        except Exception as e:
            self.log.insert(tk.END, f"Disconnect failed: {str(e)}\n")
        finally:
            self.client = None

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.log.insert(tk.END, f"Unexpected disconnection. Code: {rc}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTApp(root)
    root.mainloop()
