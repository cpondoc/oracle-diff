'''
File: band.py
Getting data from the Band Protocol network
'''

''' Libraries '''
from web3 import Web3
import json
import scripts.helpers.contract

''' Constants '''
granularity = 10 ** 18 # For helping parse through data from the blockchain
bases = ['BTC', 'ETH'] # For base of conversion
converts = ['USD', 'ETH'] # For what is going to be converted into

''' Setting up Smart Contract '''
band_contract = scripts.helpers.contract.get_contract('contracts/bandchain.json', '0xDA7a001b254CD22e46d3eAB04d937489c93174C3')

"""
Function: get_values()
Get the corresponding values, given the contract
"""
def find_values():
   '''
   Get the corresponding values, given the contract
   '''
   for base in bases:
      for convert in converts:
         print("Convert " + base + " to " + convert)
         band_data = band_contract.functions.getReferenceData(base, convert).call()
         print("Exchange Rate: " + str(band_data[0]/granularity))
         print('\n')

def return_prices(coin):
   '''
   Returns price for a given coin
   '''
   return band_contract.functions.getReferenceData(str(coin), 'USD').call()[0] / granularity

def grab_gas_estimate(coin_name):
   '''
   Gets the estimate of gas from pulling info from one data 
   point from the oracle.
   '''
   return band_contract.functions.getReferenceData(str(coin_name), 'USD').estimateGas()

if __name__ == "__main__":
   '''
   Runs all helper functions by setting up contract, 
   grabbing values, and printing.
   '''
   print("Run")