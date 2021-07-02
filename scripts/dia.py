"""
File: dia.py
Get important data for the DIA Oracle
Note: Only takes in Bitcoin, Litecoin, and Ethereum through their ABI
"""

""" Necessary Libraries """
from scripts.tellor import set_up_contract
import requests
from web3 import Web3
import json
from datetime import datetime

"""
Function: get_contract
Get the smart contract info using web3.py
"""
def get_contract():
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/50b206f08a5745818266c90ac93c86b2'))
    f = open('contracts/dia.json', 'r')
    abi = json.load(f)
    contract = web3.eth.contract(address="0xD47FDf51D61c100C447E2D4747c7126F19fa23Ef", abi=abi)
    return contract

""" 
Function: get_value
Get the value of the coin given the response from the DIA API Endpoint
"""
def get_value(coin):
    r = requests.get("https://api.diadata.org/v1/quotation/" + coin)
    return r.json()

""" 
Function: print_info
Print information relevant to each coin
"""
def print_info(name, price, comparison, time):
    print("DIA Oracle data on " + name + "/" + comparison)
    print("Conversation Rate: " + str(price))
    print("Time Updated: " + str(time))
    print("\n")

""" 
Function: return_price
Returns price from the .json response!
"""
def return_price(coin):
    coin_json = get_value(coin)
    return coin_json['Price']

"""
Function: grab_gas_estimate
Gets the estimate of gas from pulling info from one data point from the oracle
"""
def grab_gas_estimate(coin_name):
    contract = get_contract()
    return contract.functions.getCoinInfo((coin_name)).estimateGas()

""" 
Function: main
Runs all of the entirety of the helper functions
"""
if __name__ == "__main__":
    contract = get_contract()
    print(contract.functions.getCoinInfo("Bitcoin").call())