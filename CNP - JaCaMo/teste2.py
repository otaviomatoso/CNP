from requests import post, get
import os, json, time
from random import randint, uniform
############

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

def wp_register(name, address):
    body = json.dumps({"agentid": f"{name}", "uri": f"{address}"})
    endpoint = 'wp'
    url = url_base + endpoint
    headers = {'Content-Type':'application/json'}
    post(url, headers=headers, data=body)

print('Starting...\n')
url_base = 'http://192.168.1.106:8080/'
my_name = 'p341'
my_address = 'sdfmandetta'
# pname = getParticipant()
# print(f'NAME = {pname}')
wp_register(my_name, my_address)
# Create 'python' agent
