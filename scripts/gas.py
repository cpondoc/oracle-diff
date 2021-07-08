from web3 import Web3
import json
from datetime import datetime

""" Constants """
TIME_CHANGE = 20 

"""
Function: get_contract()
Get the contract for a specific exchange for Chainlink
"""
def get_contract(address):
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
    f = open('contracts/chainlink_gas.json', 'r')
    abi = json.load(f)
    return web3.eth.contract(address=address, abi=abi)

"""
Function: get_timestamps()
Get the values and the timestamps for each value
"""
def get_timestamps():
    timestamps = []
    gas_prices = []
    contract = get_contract('0x169E633A2D1E6c10dD91238Ba11c4A708dfEF37C')
    data = (contract.functions.latestRoundData().call())
    update_id = data[0]
    for i in range(0, TIME_CHANGE):
        data = contract.functions.getRoundData(update_id).call()
        timestamps.append(data[3])
        gas_prices.append(data[1])
        update_id -= 1
    return gas_prices, timestamps