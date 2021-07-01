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
granularity = 1000000 # Defined granularity for all of the data feeds
num_vals = 100 # Number of past values to grab for looking at history

"""
Function: set_up_contract()
Accesses the Tellor ABI, connects to the Tellor contract, and returns to use
"""
def set_up_contract():
    f = open('contracts/tellorLens.json', 'r')
    abi = json.load(f)
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
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
        prices.append(value/granularity)
        #for i in range(0, 50):
            #[worked, value, timestamp] = (contract.functions.getDataBefore(id_num, timestamp).call())
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
    all_prices.append(value/granularity)
    for i in range(0, num_vals):
        [worked, value, timestamp] = (contract.functions.getDataBefore(id_num, timestamp).call())
        all_prices.append(value/granularity)
    return all_prices[::-1]

"""
Function: grab_price_change()
Get the change in price over a certain amount of time!
"""
def get_better_price(id_name, number_values):
    contract = set_up_contract()
    all_prices = []
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[id_name]['id'])
    old_date = datetime.timestamp(datetime.now() - timedelta(days=5))
    initial_data = contract.functions.getCurrentValue(id_num).call()
    all_prices.append(initial_data[1] / granularity)
    while (old_date < initial_data[2]):
        initial_data = contract.functions.getDataBefore(id_num, initial_data[2]).call()
        all_prices.append(initial_data[1] / granularity)
    round_factor = math.floor(len(all_prices) / number_values)
    if len(all_prices) < number_values:
        round_factor = number_values
    all_prices = all_prices[::round_factor]
    last_offset = abs(len(all_prices) - number_values)
    all_prices = all_prices[last_offset:]
    return all_prices

"""
Function: grab_time_change()
Get the change in update time over a certain amount of requests!
"""
def grab_time_change(id_name):
    contract = set_up_contract()
    all_diffs = []
    old_timestamp = datetime.now()
    new_timestamp = datetime.now()
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[str(id_name)]['id'])
    [worked, value, timestamp] = (contract.functions.getCurrentValue(id_num).call())
    new_timestamp = datetime.utcfromtimestamp(timestamp)
    for i in range(0, 50):
        [worked, value, timestamp] = (contract.functions.getDataBefore(id_num, timestamp).call())
        old_timestamp = datetime.utcfromtimestamp(timestamp)
        time_diff = new_timestamp - old_timestamp
        all_diffs.append(time_diff.seconds)
        new_timestamp = old_timestamp
    return all_diffs[::-1]

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
    print("Exchange Rate: " + str(value/granularity))
    print("Timestamp: " + str(timestamp))
    print("\n")

""" 
Function: main
Runs all of the entirety of the helper functions
"""
if __name__ == "__main__":
    contract = set_up_contract()
    #print(get_better_price(contract, "BTC/USD"))
    #grab_gas_estimate(contract, "BTC/USD")
    #grab_feeds(contract)
    #grab_price_change(contract, "BTC/USD")
    #grab_time_change(contract, "BTC/USD")