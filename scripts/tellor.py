'''
File: tellor.py
Grabs data from Tellor and get all results
'''

''' Necessary Libraries '''
import json
from datetime import datetime, timedelta
import math
import helpers.contract

''' Constants '''
ABI_PATH = 'contracts/tellorLens.json' # Relative path to ABI
ADDRESS = '0xb2b6c6232d38fae21656703cac5a74e5314741d4' # Address of smart contract on mainnet
FEEDS_PATH = 'feeds/tellor.json' # Path to get feeds data from feeds
GRANULAITY = 1000000 # Defined granularity for all of the data feeds
NUM_DAYS = 8 # Number of days to look back for historical data
NUM_VALS = 100 # Number of past values to grab for looking at history
TIME_CHANGE = 20 # Number of time changes to look at

''' Setting up Smart Contract '''
tellor_contract = helpers.contract.get_contract(ABI_PATH, ADDRESS)

def grab_feeds():
    '''
    Get the correct data feed IDs from Tellor and get their value
    '''
    prices = []
    with open(FEEDS_PATH) as f:
        data = json.load(f)
    for elem in data:
        id_num = int(data[elem]['id'])
        tellor_data = (tellor_contract.functions.getCurrentValue(id_num).call())
        prices.append(tellor_data[1]/GRANULAITY)
    return prices

def grab_price_change(id_name):
    '''
    Older function -- used to get change in price over a certain amount of time
    '''
    all_prices = []
    with open(FEEDS_PATH) as f:
        data = json.load(f)
    id_num = int(data[id_name]['id'])
    [worked, value, timestamp] = (tellor_contract.functions.getCurrentValue(id_num).call())
    all_prices.append(value/GRANULAITY)
    for i in range(0, NUM_VALS):
        [worked, value, timestamp] = (tellor_contract.functions.getDataBefore(id_num, timestamp).call())
        all_prices.append(value/GRANULAITY)
    return all_prices[::-1]

def get_better_price(id_name, number_values):
    '''
    Updated function get price over time
    '''
    # Define initial variables
    all_prices = []
    all_timestamps = []
    with open(FEEDS_PATH) as f:
        data = json.load(f)
    id_num = int(data[id_name]['id'])

    # Get initial data and old date
    old_date = datetime.timestamp(datetime.now() - timedelta(days=NUM_DAYS))
    initial_data = tellor_contract.functions.getCurrentValue(id_num).call()
    all_prices.append(initial_data[1] / GRANULAITY)
    all_timestamps.append(datetime.fromtimestamp(int(initial_data[2])))

    # Loop through old data and append all prices and time stamps
    while (old_date < initial_data[2]):
        initial_data = tellor_contract.functions.getDataBefore(id_num, initial_data[2]).call()
        all_prices.append(initial_data[1] / GRANULAITY)
        all_timestamps.append(datetime.fromtimestamp(int(initial_data[2])))
    round_factor = math.floor(len(all_prices) / number_values)

    # Trim down number of elements to fit into needed values
    if len(all_prices) < number_values:
        round_factor = number_values
    all_prices = all_prices[::round_factor]
    all_timestamps = all_timestamps[::round_factor]
    last_offset = abs(len(all_prices) - number_values)
    all_prices = all_prices[last_offset:]
    all_timestamps = all_timestamps[last_offset:]
    return all_prices, all_timestamps

def grab_time_change(id_name):
    '''
    Get the change in update time over a certain amount of requests!
    '''
    # Define initial variables
    all_diffs = []
    all_timestamps = []
    old_timestamp = datetime.now()
    new_timestamp = datetime.now()
    with open(FEEDS_PATH) as f:
        data = json.load(f)
    id_num = int(data[str(id_name)]['id'])

    # Grab initial timestamp
    [worked, value, timestamp] = (tellor_contract.functions.getCurrentValue(id_num).call())
    all_timestamps.append(datetime.utcfromtimestamp(timestamp))
    new_timestamp = datetime.utcfromtimestamp(timestamp)

    # Loop through time change to get to old values
    for i in range(0, TIME_CHANGE):
        [worked, value, timestamp] = (tellor_contract.functions.getDataBefore(id_num, timestamp).call())
        old_timestamp = datetime.utcfromtimestamp(timestamp)
        time_diff = new_timestamp - old_timestamp
        all_diffs.append(time_diff.seconds)
        all_timestamps.append(datetime.utcfromtimestamp(timestamp))
        new_timestamp = old_timestamp
    return all_diffs[::-1], all_timestamps[:20]

def grab_gas_estimate(id_name):
    '''
    Estimate gas for retrieving data from the chain.
    '''
    with open('feeds/tellor.json') as f:
        data = json.load(f)
    id_num = int(data[str(id_name)]['id'])
    return (tellor_contract.functions.getCurrentValue(id_num).estimateGas())

def print_data(elem, value, timestamp):
    '''
    Older function -- print all data concerning oracle
    '''
    print("Tellor Data for " + str(elem))
    print("Exchange Rate: " + str(value/GRANULAITY))
    print("Timestamp: " + str(timestamp))
    print("\n")

if __name__ == "__main__":
    grab_feeds()