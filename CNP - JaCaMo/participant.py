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

def sendCmd(agent, cmd):
    endpoint = f'agents/{agent}/cmd'
    url = url_base + endpoint
    payload = {'c': f'{cmd}'}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    post(url, headers=headers, data=payload)

def getDf():
    endpoint = 'services'
    url = url_base + endpoint
    req = get(url)
    return req.text

def dfRegister(service, agent):
    body = json.dumps({"service": f"{service}"})
    endpoint = f'services/{agent}'
    url = url_base + endpoint
    print(f'URL = {url}')
    headers = {'Content-Type':'application/json'}
    post(url, headers=headers, data=body)

def getParticipant():
    df = getDf()
    df = json.loads(df)
    for ag in df:
        if ('participant' in df[ag]['services']):
            return ag

print('Starting...\n')
url_base = 'http://192.168.1.106:8080/'
my_name = 'python'
part_name = getParticipant() # participant agent name

createAgent(my_name)
# Copy plans from a participant agent to python agent
plans = getPlans(part_name)
postPlans(my_name,plans)

service = "participant"
dfRegister(service, my_name)
sendCmd(my_name, '.df_subscribe("initiator")')

#  *** USE EITHER ABOVE OR BELOW BLOCK ***

# # Ask python agent to register in the DF (by sending a message)
# msg2 = createMsg(my_name,my_name,'achieve','register',randint(10, 100))
# sendMsg(msg2,my_name)

# Add an offer in the BB of python agent (by sending a message)
price = uniform(100, 110)
content = f'price(Task,{price})'
msg = createMsg(my_name,my_name,'tell',content,randint(10, 100))
sendMsg(msg,my_name)
print(f'\nMy offer = {price}\n')

# Polling to check if CNP is finished.
result = ''
while (result == ''):
    beliefs = getBeliefs(my_name)
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
