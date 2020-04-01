import paho.mqtt.client as mqtt #import the client1
import json
from random import randint
############
# message = '{"Type": "participant", "Name": "Python", "Service": "beer"}'
# msg = json.dumps(message)
MQTT_MSG=json.dumps({"Type": "participant", "Name": "Python", "Service": "beer"});
broker_address="test.mosquitto.org"
client = mqtt.Client("python") #create new instance
print("connecting to broker")
client.connect(broker_address, port=1883) #connect to broker
client.publish("CNP-global", MQTT_MSG)



# client.loop_start() #start the loop
# print("Subscribing to topic","cnp")
# client.subscribe("cnp")
# print("Publishing message to topic","register")
# client.publish("register","introduction(cooker,python)")
# time.sleep(4) # wait
# client.loop_stop() #stop the loop
