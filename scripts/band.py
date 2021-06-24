"""
File: band.py
Getting data from the Band Protocol network
"""

""" Libraries """
from web3 import Web3
import json

""" Constants """
granularity = 10 ** 18 # For helping parse through data from the blockchain

""" 
Function: get_contract()
Accesses the Band Protocol ABI, connects to the Band Protocol contract, and returns to use
"""
def get_contract():
   f = open('contracts/bandchain.json', 'r')
   abi = json.load(f)
   web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
   address = '0xDA7a001b254CD22e46d3eAB04d937489c93174C3'
   f.close()
   return web3.eth.contract(address=(address), abi=abi)

""" 
Function: main
Runs all helper functions by setting up contract, grabbing values, and printing.
"""
if __name__ == "__main__":
    contract = get_contract()
    [value, block, quote] = contract.functions.getReferenceData('BTC', 'USD').call()
    print(value / granularity)