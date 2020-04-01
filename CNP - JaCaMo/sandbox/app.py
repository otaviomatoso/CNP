from flask import Flask, request
from requests import post
import json
from random import randint, uniform

app = Flask(__name__)

def process_content(content):
    d = dict();
    d['functor'] = content[0:content.find('(')]
    d['args'] = content[len(d['functor'])+1:len(content)-1]
    return d

def process_msg(literal, sender):
    if (literal['functor'] == 'cfp'):
        global task, offer, id
        cnpId = literal["args"].split(',')[0]
        task = literal["args"].split(',')[1]
        offer = uniform(100, 110)
        content = f'propose({cnpId},{offer})'
        msg = create_msg(my_name,sender,'tell',content,id)
        send_msg(msg, sender)
        id += 1
    elif (literal['functor'] == 'accept_proposal'):
        cnpId = literal["args"]
        print(f'My proposal {offer} won CNP {cnpId} for {task}!')
    elif (literal['functor'] == 'reject_proposal'):
        cnpId = literal["args"]
        print(f'I lost CNP {cnpId}.')

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

def getDf():
    endpoint = 'services'
    url = url_base + endpoint
    req = get(url)
    return req.text

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
# wp_register(my_name, my_address)
# Copy plans from a participant agent to python agent
plans = getPlans(part_name)
postPlans(my_name,plans)
# Add an offer in the BB of python agent (by sending a message)
price = uniform(100, 110)
content = f'price(Task,{price})'
msg = createMsg(my_name,my_name,'tell',content,randint(10, 100))
sendMsg(msg,my_name)
print(f'\nMy offer = {price}\n')
# Ask python agent to register in the DF (by sending a message)
msg2 = createMsg(my_name,my_name,'achieve','register',randint(10, 100))
sendMsg(msg2,my_name)


# --- MAIN ---
# print('\nRegistering myself at WP...')
# wp_register(my_name, my_address)
# print('\nRegistering myself at DF...')
# service = "participant"
# df_register(service, my_name)

# Mailbox to receive messages from agents
# PS.: When agent acts as client, the path '/mb'
#      is added at the end of the endpoint
@app.route('/mb', methods=['POST'])
def mailBox():
    msg = json.loads(request.data)
    sender = msg['sender']
    content = msg['content']
    literal = process_content(content)
    process_msg(literal, sender)
    return ''
