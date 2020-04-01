import paho.mqtt.client as mqtt #import the client1
import time
from random import randint
############
broker_address="test.mosquitto.org"
client = mqtt.Client("python") #create new instance
client.connect(broker_address, port=1883) #connect to broker
print("CFP received by MAS")
print("Sending a proposal...")
price = randint(1, 9);
client.publish("proposals",f"proposal(python,beer,{price})")



# client.loop_start() #start the loop
# print("Subscribing to topic","cnp")
# client.subscribe("cnp")
# print("Publishing message to topic","register")
# client.publish("register","introduction(cooker,python)")
# time.sleep(4) # wait
# client.loop_stop() #stop the loop
