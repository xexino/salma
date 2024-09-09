import paho.mqtt.client as mqtt

# définir fonction qui est appelé automatiquement quand le client se connecte au broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
#Créer une liste de topics à souscrire avec niveau de QoS 0  
    topics = [("subscribe/ilyasmali", 0), ("subscribe/topic1", 0), ("subscribe/topic2", 0)]
    for topic, qos in topics:
        client.subscribe(topic, qos)
        print(f"Subscribed to topic: {topic}")
# fonction appelé quand le client reçoit un message d'un topic auquel il est abonné.
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
# fonction  appelé lorsque le client se déconnecte du broker
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

# créer une instance client  avec  TLS/SSL
client = mqtt.Client()

# Activée la vérification des cerif SSL
client.tls_insecure_set(False)

# Associé les fonctions à l'instance client 
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Se connecter au broker MQTT s le port 8883
broker_address = "broker.emqx.io"  # Replace with your broker address if different
client.connect(broker_address, 8883, 60)

# Démarre la boucle d'écoute du client
client.loop_start()

# Crée une liste de topics pour publier des messages de test
publish_topics = ["publish/ilyasmali", "publish/topic1", "publish/topic2"]
for topic in publish_topics:
    client.publish(topic, f"Hello MQTT from {topic}")

# Attend que l'utilisateur appuie sur "Enter" pour arrêter le programme
input("Press Enter to quit...")

# Arrête la boucle d'écoute du client et se déconnecter
client.loop_stop()
client.disconnect()
