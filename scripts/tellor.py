"""
File: tellor.py
Get the data from the function
"""

""" Necessary Libraries """
import json
from web3 import Web3

# Looking at pulling
# Opening JSON file
f = open('contracts/tellorLens.json',)
abi = json.load(f)
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
address = '0xb2b6c6232d38fae21656703cac5a74e5314741d4'
contract = web3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
print(contract.functions.getCurrentValue(1).call())
f.close()