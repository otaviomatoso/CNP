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
url_base = 'http://192.168.1.106:8080/' # jacamo-rest address
p_name = 'p' # p.asl is the participant source code in Jason
reply = create_agent(p_name)
# Regex is used to get the name of the created agent.
# The name is in the API response, in single quotes.
# If more than one agent is created using the same name,
# the given names are as follows: name, name_1, name_2, name_3,...
myName = re.findall(r"'([^']*)'", reply)[0] # The result is a list, so the name is at index 0.
print (f'My name = {myName}')

# Polling to check if CNP has finished.
result = ''
while (result == ''):
    beliefs = get_beliefs(myName)
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
