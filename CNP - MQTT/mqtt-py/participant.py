import paho.mqtt.client as mqtt #import the client1
import json
from random import randint
############
def on_message(client, userdata, message):
    if(message.topic == "cnp/cfp"):
        print('Call for proposal received.')
        m_decode = str(message.payload.decode("utf-8"))
        print("CFP = ", m_decode)
        # price = 1;
        price = randint(2, 20);
        cfp_msg = json.loads(m_decode)
        id = cfp_msg["Id"]
        proposal_msg = json.dumps({"Type": "proposal", "Id": f"{id}", "Name": "python", "Price": f"{price}"});
        print(f'\nMy proposal = {proposal_msg}')
        client.publish("cnp/proposals", proposal_msg)

    elif(message.topic == "cnp/result"):
        print("\nresult = ", str(message.payload.decode("utf-8")))
        m_decode = str(message.payload.decode("utf-8"))
        result_msg = json.loads(m_decode)
        if(result_msg["Name"] == "python"):
            print(f'\nI won the CNP (Id = {result_msg["Id"]})')
        else:
            print(f'\nI lost the CNP (Id = {result_msg["Id"]})')


broker_address="test.mosquitto.org"
print("creating new instance")
client = mqtt.Client("python") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address, port=1883) #connect to broker
print("Registering my credentials to CNP...")
register_msg = json.dumps({"Type": "participant", "Name": "python", "Service": "beer"});
client.publish("cnp/participants", register_msg)
client.subscribe("cnp/cfp")
client.subscribe("cnp/result")
# client.subscribe("CNP-proposals")
client.loop_forever();
