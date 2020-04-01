from requests import post, get
import json, time
import re
############

def create_agent(agent):
    print(f'Creating agent {agent}')
    endpoint = f'agents/{agent}'
    url = url_base + endpoint
    req = post(url)
    # print(req.text)
    return req.text

def get_beliefs(agent):
    endpoint = f'agents/{agent}/mind/bb'
    url = url_base + endpoint
    req = get(url)
    return req.text

print('Starting...\n')
url_base = 'http://192.168.1.106:8080/'
p_name = 'p' # p.asl is the participant source code in Jason
reply = create_agent(p_name)
myName = re.search(r"'([^']*)'", reply).group()
# myName = myName[0]  # The result is a list, so the name is at index 0.
print (f'My name = {myName}')
