import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import ssl

class MQTTApp:
    def __init__(self, root):
       # definir la fenetre principale
        self.root = root
        # nom de la fenetre
        self.root.title("MQTTS Client")
        

        # initialisation du client 
        self.client = None

        # liste pour stocker les topics
        self.subscribe_topics = []
        self.publish_topics = []

        # appeler la methode pour creer les composants de l'interface
        self.create_widgets()

    def create_widgets(self):
        # creer bouton de connexion 
        self.connect_button = ttk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.pack(pady=10)
        
     # creer une Label et Entrée pour entrer le topic auquel s'abonner
        self.subscribe_label = ttk.Label(self.root, text="Topic to Subscribe:")
        self.subscribe_label.pack()
        self.subscribe_entry = ttk.Entry(self.root)
        self.subscribe_entry.pack()
   # creer bouton subscribe
        self.subscribe_button = ttk.Button(self.root, text="Subscribe", command=self.subscribe)
        self.subscribe_button.pack(pady=10)
   #creer une Label et Entrée pour entrer le message à publier
        self.publish_label = ttk.Label(self.root, text="Topic to Publish:")
        self.publish_label.pack()
        self.publish_entry = ttk.Entry(self.root)
        self.publish_entry.pack()

        self.publish_message_label = ttk.Label(self.root, text="Message to Publish:")
        self.publish_message_label.pack()
        self.publish_message_entry = ttk.Entry(self.root)
        self.publish_message_entry.pack()
  # creer un bouton pour publier 
        self.publish_button = ttk.Button(self.root, text="Publish", command=self.publish)
        self.publish_button.pack(pady=10)
 # creer un bouton pour se déconnecter 
        self.disconnect_button = ttk.Button(self.root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(pady=10)
 # creer une zone de texte 
        self.log = tk.Text(self.root, height=15, width=60)
        self.log.pack(pady=10)
# methode connect 
    def connect(self):
        if self.client is not None:
            self.disconnect()

        # création du client et configuration du callbacks
        self.client = mqtt.Client(protocol=mqtt.MQTTv311) 
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
      
        broker_address = "broker.emqx.io"  
        port = 8883  # MQTTS port

        try:
            self.client.tls_set(
                ca_certs=None,  # Use system default CA certs
                tls_version=ssl.PROTOCOL_TLS,
                cert_reqs=ssl.CERT_REQUIRED
            )
            # configuration du paramètre TLS pour vérifier les certif  
            self.client.tls_insecure_set(True)  
            # se connecter au broker 
            self.client.connect(broker_address, port, 60) 
            # commencer une boucle d'écoute 
            self.client.loop_start()
            self.log.insert(tk.END, "Connecting to broker...\n")
        except Exception as e:
            self.log.insert(tk.END, f"Connection failed: {str(e)}\n")
            # appeler on_connect quand le client se connecte
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.log.insert(tk.END, "Connected successfully\n")
            for topic in self.subscribe_topics:
                self.client.subscribe(topic)
                self.log.insert(tk.END, f"Subscribed to topic: {topic}\n")
        else:
            self.log.insert(tk.END, f"Connection failed with code {rc}\n")
#Récupère le topic de souscription de l'interface, ajoute le topic à la liste, puis demande au client MQTT de s'y abonner
    def subscribe(self):
        topic = self.subscribe_entry.get()
        if topic:
            self.subscribe_topics.append(topic)
            if self.client is not None:
                self.client.subscribe(topic)
                self.log.insert(tk.END, f"Subscribed to topic: {topic}\n")
            else:
                self.log.insert(tk.END, "Not connected. Please connect first.\n")
# Affiche les messages reçus dans la zone de log
    def on_message(self, client, userdata, msg):
        self.log.insert(tk.END, f"Message received: {msg.topic}: {msg.payload.decode()}\n")
# Publie le message entré sur le topic sélectionné

    def publish(self):
        topic = self.publish_entry.get()
        message = self.publish_message_entry.get()
        if not self.client:
            self.log.insert(tk.END, "Not connected. Please connect first.\n")
            return
        if topic and message:
            self.client.publish(topic, message)
            self.log.insert(tk.END, f"Message published to {topic}: {message}\n")
#Arrête la boucle d'écoute et déconnecte le client MQTT
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
 #Code d'éxecution 
if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTApp(root)
    root.mainloop()
