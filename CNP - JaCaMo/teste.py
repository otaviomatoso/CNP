from requests import post, get
import os, json, time
from random import randint, uniform
############

def sendCmd(agent, cmd):
    endpoint = f'agents/{agent}/cmd'
    url = url_base + endpoint
    payload = {'c': f'{cmd}'}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    post(url, headers=headers, data=payload)

print('Starting...\n')
url_base = 'http://192.168.1.106:8080/'
cmd = '.print("COMER CU DE CURIOSO")'
sendCmd('p1', cmd)
# url_base = 'http://150.162.12.79:8080/' # url computer LTIC
