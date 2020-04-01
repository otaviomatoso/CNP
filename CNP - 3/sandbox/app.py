from flask import Flask, request
from requests import post
import json
from random import randint, uniform

app = Flask(__name__)

# Global variables
url_base = 'http://192.168.1.106:8080/' # jacamo-rest address
my_name = 'python'
my_address = 'http://127.0.0.1:5000'
id = 1 # id used to send msg to SMA
task = ''
offer = 0

# --- FUNCTIONS ---

def wp_register(name, address):
    body = json.dumps({"agentid": f"{name}", "uri": f"{address}"})
    endpoint = 'wp'
    url = url_base + endpoint
    headers = {'Content-Type':'application/json'}
    post(url, headers=headers, data=body)

def df_register(service, agent):
    body = json.dumps({"service": f"{service}"})
    endpoint = f'services/{agent}'
    url = url_base + endpoint
    print(f'URL = {url}')
    headers = {'Content-Type':'application/json'}
    post(url, headers=headers, data=body)

def create_msg(sender,receiver,performative,content,msgId):
    msg = json.dumps({"sender": f"{sender}", "receiver": f"{receiver}", "performative": f"{performative}", "content": f"{content}", "msgId": f"{msgId}"})
    return msg

def send_msg(message, agent):
    endpoint = f'agents/{agent}/mb'
    url = url_base + endpoint
    headers = {'Content-Type':'application/json'}
    post(url, headers=headers, data=message)

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

# --- MAIN ---
print('\nRegistering myself at WP...')
wp_register(my_name, my_address)
print('\nRegistering myself at DF...')
service = "participant"
df_register(service, my_name)

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
