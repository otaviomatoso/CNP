import paho.mqtt.client as mqtt #import the client1
import time
from random import randint
############
def on_message(client, userdata, message):
    if(message.topic == "CNP-cfp"):
        print('Call for proposal received.')
        print("CFP = ", str(message.payload.decode("utf-8")))

    elif(message.topic == "CNP-proposals"):
        print('PROPOSALS')


        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
    # print("CFP received by MAS")
    # print("Sending a proposal...")
    # price = randint(2, 20);
    # print(f"My proposal = proposal(python,beer,{price})")
    # client.publish("CNP-proposals",f"proposal(python,beer,{price})")


    # print("Publishing message to topic","register")
    # client.publish("register","introduction(beer,python)")
########################################
broker_address="test.mosquitto.org"
print("creating new instance")
client = mqtt.Client("python") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address, port=1883) #connect to broker
print("Registering my credentials to CNP...")
client.publish("CNP-participants","participant(python,beer)")
client.subscribe("CNP-cfp")
client.subscribe("CNP-proposals")
client.loop_forever();
print("after loop forever...")



# client.loop_start() #start the loop
# print("Subscribing to topic","cnp")
# client.subscribe("cnp")
# print("Publishing message to topic","register")
# client.publish("register","introduction(cooker,python)")
# time.sleep(4) # wait
# client.loop_stop() #stop the loop
