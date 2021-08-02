'''
File: contract.py
Helper function to create a contract.py 
'''

''' Necessary helper functions '''
from web3 import Web3
import json

def get_contract(abi_path, address):
   '''
   Connect to smart contracts!
   '''
   f = open(abi_path, 'r')
   abi = json.load(f)
   web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
   f.close()
   return web3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)

def reference_data(file_path):
   '''
   Get reference data (addresses, price IDs) for each oracle
   '''
   with open(file_path) as f:
        return json.load(f)