from requests import post, get
import os, json, time
from random import randint, uniform
############

def createAgent(agent):
    print(f'Creating agent {agent}')
    endpoint = f'agents/{agent}'
    url = url_base + endpoint
    req = post(url)
    print(req.text)

def createMsg(sender,receiver,performative,content,msgId):
    msg = json.dumps({"sender": f"{sender}", "receiver": f"{receiver}", "performative": f"{performative}", "content": f"{content}", "msgId": f"{msgId}"})
    return msg

def sendMsg(message, agent):
    endpoint = f'agents/{agent}/mb'
    url = url_base + endpoint
    headers = {'Content-Type':'application/json'}
    post(url, headers=headers, data=message)

def getPlans(agent):
    endpoint = f'agents/{agent}/plans'
    url = url_base + endpoint
    req = get(url)
    return req.text

def postPlans(agent, plans):
    print(f'\nSending plans to agent {agent}...')
    endpoint = f'agents/{agent}/plans'
    url = url_base + endpoint
    currentDir = os.getcwd()
    filePath = currentDir + '\plan'
    files = {'file': open(filePath)} # Why is it necessary?
    payload = {'plans': plans}
    req = post(url, files=files, data=payload)
    print(req.text)

def getBeliefs(agent):
    endpoint = f'agents/{agent}/mind/bb'
    url = url_base + endpoint
    req = get(url)
    return req.text

print('Starting...\n')
url_base = 'http://192.168.1.106:8080/'
# url_base = 'http://150.162.12.79:8080/' # url computer LTIC

# Create 'python' agent
myName = 'python'
createAgent(myName)

# Copy plans from a participant agent to python agent
partAgent = 'p1' # participant agent
plans = getPlans(partAgent)
postPlans(myName,plans)

# Add an offer in the BB of python agent (by sending a message)
price = uniform(100, 110)
content = f'price(Task,{price})'
msg = createMsg(myName,myName,'tell',content,randint(10, 100))
sendMsg(msg,myName)
print(f'\nMy offer = {price}\n')

# Ask python agent to register in the DF (by sending a message)
msg2 = createMsg(myName,myName,'achieve','register',randint(10, 100))
sendMsg(msg2,myName)

# Polling to check if CNP is finished.
result = ''
while (result == ''):
    beliefs = getBeliefs(myName)
    # If an agent receives 'accept_proposal' or 'reject_proposal',...
    # ...it means that the CNP is over
    if ('accept_proposal' in beliefs) or ('reject_proposal' in beliefs):
        bbjson = json.loads(beliefs)
        for b in bbjson:
            if ('accept_proposal' in b):
                cnpId = b[b.find("(")+1:b.find(")")] # Get CNPId
                print(f'\nMy proposal \'{price}\' won CNP {cnpId}\n')
                result = b
                break
            elif ('reject_proposal' in b):
                cnpId = b[b.find("(")+1:b.find(")")] # Get CNPId
                print(f'\nI lost CNP {cnpId}\n')
                result = b
                break
    else:
        print('Waiting for the result of CNP.')
        time.sleep(4)
