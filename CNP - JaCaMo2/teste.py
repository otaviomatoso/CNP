from requests import post, get
import os, json, time
from random import randint, uniform
############

def process_content(sender, content):
    d = dict();
    d['sender'] = sender
    d['functor'] = content[0:content.find('(')]
    d['args'] = content[len(d['functor'])+1:len(content)-1]
    return d

propose(CNPId,Offer)

def process_msg(literal):
    if (literal['functor'] == 'cfp'):
        cnpId = literal["args"].split(',')[0]
        task = literal["args"].split(',')[1]
        price = uniform(100, 110)
        content = f'propose({cnpId},{price})'


sender = 'corona'
msg = 'cfp(1,fix(computer))'
msg1 = 'accept_proposal(2)'
msg2 = 'reject_proposal(3)'
literal = process_content(sender,msg)
print(literal)
# print(f'\nFUNCTOR = {literal["functor"]}')
# print(f'\nARGS = {literal["args"]}')
#
# cnpId = literal["args"].split(',')[0]
# task = literal["args"].split(',')[1]
# print(f'\nCNPId = {cnpId}')
# print(f'\nTask = {task}')
