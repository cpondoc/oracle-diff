"""
File: tellor.py
Grabs data from Tellor and get all results
"""

""" Necessary Libraries """
import json
from web3 import Web3
from datetime import datetime, timedelta
import math

""" Constants """
GRANULAITY = 1000000 # Defined granularity for all of the data feeds
NUM_VALS = 100 # Number of past values to grab for looking at history
TIME_CHANGE = 20 # Number of time changes to look at


"""
Function: set_up_contract()
Accesses the Tellor ABI, connects to the Tellor contract, and returns to use
"""
def set_up_contract():
    f = open('contracts/tellorLens.json', 'r')
    abi = json.load(f)
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1cc3d60f38f64e469c4ea250ddeb0c54'))
    address = '0xb2b6c6232d38fae21656703cac5a74e5314741d4'
    f.close()
    return web3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)

""" 
Function: grab_feeds()
Get the correct data feed IDs from Tellor and get their value
"""
def grab_feeds():
    contract = set_up_contract()
    prices = []
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    for elem in data:
        id_num = int(data[elem]['id'])
        [worked, value, timestamp] = (contract.functions.getCurrentValue(id_num).call())
        prices.append(value/GRANULAITY)
    return prices

"""
Function: grab_price_change()
Get the change in price over a certain amount of time!
"""
def grab_price_change(contractz, id_name):
    contract = set_up_contract()
    all_prices = []
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[id_name]['id'])
    [worked, value, timestamp] = (contract.functions.getCurrentValue(id_num).call())
    all_prices.append(value/GRANULAITY)
    for i in range(0, NUM_VALS):
        [worked, value, timestamp] = (contract.functions.getDataBefore(id_num, timestamp).call())
        all_prices.append(value/GRANULAITY)
    return all_prices[::-1]

"""
Function: get_better_price()
Get the change in price over a certain amount of time!
"""
def get_better_price(id_name, number_values):
    contract = set_up_contract()
    all_prices = []
    all_timestamps = []
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[id_name]['id'])
    old_date = datetime.timestamp(datetime.now() - timedelta(days=8))
    initial_data = contract.functions.getCurrentValue(id_num).call()
    all_prices.append(initial_data[1] / GRANULAITY)
    all_timestamps.append(datetime.fromtimestamp(int(initial_data[2])))
    while (old_date < initial_data[2]):
        initial_data = contract.functions.getDataBefore(id_num, initial_data[2]).call()
        all_prices.append(initial_data[1] / GRANULAITY)
        all_timestamps.append(datetime.fromtimestamp(int(initial_data[2])))
    round_factor = math.floor(len(all_prices) / number_values)
    if len(all_prices) < number_values:
        round_factor = number_values
    all_prices = all_prices[::round_factor]
    all_timestamps = all_timestamps[::round_factor]
    last_offset = abs(len(all_prices) - number_values)
    all_prices = all_prices[last_offset:]
    all_timestamps = all_timestamps[last_offset:]
    return all_prices, all_timestamps

"""
Function: grab_time_change()
Get the change in update time over a certain amount of requests!
"""
def grab_time_change(id_name):
    contract = set_up_contract()
    all_diffs = []
    all_timestamps = []
    old_timestamp = datetime.now()
    new_timestamp = datetime.now()
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[str(id_name)]['id'])
    [worked, value, timestamp] = (contract.functions.getCurrentValue(id_num).call())
    all_timestamps.append(datetime.utcfromtimestamp(timestamp))
    new_timestamp = datetime.utcfromtimestamp(timestamp)
    for i in range(0, TIME_CHANGE):
        [worked, value, timestamp] = (contract.functions.getDataBefore(id_num, timestamp).call())
        old_timestamp = datetime.utcfromtimestamp(timestamp)
        time_diff = new_timestamp - old_timestamp
        all_diffs.append(time_diff.seconds)
        all_timestamps.append(datetime.utcfromtimestamp(timestamp))
        new_timestamp = old_timestamp
    return all_diffs[::-1], all_timestamps[:20]

"""
Function: grab_gas_estimate()
Estimate gas for retrieving data from the chain.
"""
def grab_gas_estimate(id_name):
    contract = set_up_contract()
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[str(id_name)]['id'])
    return (contract.functions.getCurrentValue(id_num).estimateGas())


"""
Function: print_data()
Print all of the data!
"""
def print_data(elem, value, timestamp):
    print("Tellor Data for " + str(elem))
    print("Exchange Rate: " + str(value/GRANULAITY))
    print("Timestamp: " + str(timestamp))
    print("\n")

""" 
Function: main
Runs all of the entirety of the helper functions
"""
if __name__ == "__main__":
    contract = set_up_contract()
    print(get_better_price("BTC/USD", 80))
    #grab_gas_estimate(contract, "BTC/USD")
    #grab_feeds(contract)
    #grab_price_change(contract, "BTC/USD")
    #grab_time_change(contract, "BTC/USD")