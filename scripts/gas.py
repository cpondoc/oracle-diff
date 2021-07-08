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
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1cc3d60f38f64e469c4ea250ddeb0c54'))
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

"""
Function: get_corresponding_indices()
Gets the corresponding indices of gas prices to time differences
"""
def get_corresponding_prices(timestamps, gas_times, gas_prices):
    indices = []
    corresponding_prices = []
    for timestamp in timestamps:
        difference = int(10000000)
        index = int(0)
        for other_timestamp in gas_times:
            other_diff = int(abs(other_timestamp - int(datetime.timestamp(timestamp))))
            if (other_diff < difference):
                difference = other_diff
                index = int(gas_times.index(other_timestamp))
            indices.append(index)
    for i in range(0, len(gas_prices)):
        corresponding_prices.append(gas_prices[i])
    return corresponding_prices