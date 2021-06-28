"""
File: band.py
Getting data from the Band Protocol network
"""

""" Libraries """
from web3 import Web3
import json

""" Constants """
granularity = 10 ** 18 # For helping parse through data from the blockchain
bases = ['BTC', 'ETH'] # For base of conversion
converts = ['USD', 'ETH'] # For what is going to be converted into

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
Function: get_values()
Get the corresponding values, given the contract
"""
def find_values(contract):
   for base in bases:
      for convert in converts:
         print("Convert " + base + " to " + convert)
         band_data = contract.functions.getReferenceData(base, convert).call()
         print("Exchange Rate: " + str(band_data[0]/granularity))
         print('\n')

"""
Function: return_prices
This function returns prices for given coins
"""
def return_prices(contract, coin):
   return contract.functions.getReferenceData(coin, 'USD').call()[0] / granularity

""" 
Function: main
Runs all helper functions by setting up contract, grabbing values, and printing.
"""
if __name__ == "__main__":
    contract = get_contract()
    find_values(contract)