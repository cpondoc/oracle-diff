""" 
File: chainlink.py
Retrieves necessary data and prices from Chainlink!
"""

""" Libraries necessary for development """
from web3 import Web3
import json
from datetime import datetime, timedelta
import math

""" Constants """
num_vals = 100 # Number of past values to grab for looking at history

""" 
Function: calculate_price()
Used to help calculate the actual conversion rate from the raw number
on the blockchain
"""
def calculate_price(price, decimals):
    return float(price) / (10 ** decimals)

"""
Function: get_contract()
Get the contract for a specific exchange for Chainlink
"""
def get_contract(address):
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
    f = open('contracts/chainlink.json', 'r')
    abi = json.load(f)
    return web3.eth.contract(address=address, abi=abi)

""" 
Function: get_chainlink_data()
This function gets the value of all Chainlink Data necessary for running stuff
"""
def get_chainlink_data(name, address):
    contract = get_contract(address)
    num_decimals = contract.functions.decimals().call()
    latestData = contract.functions.latestRoundData().call()
    latestData.append(num_decimals)
    return latestData

""" 
Function: grab_feeds()
This function grabs all of the existing data feeds, and then parses the JSON
to get all of the addresses
"""
def grab_feeds():
    prices = []
    with open('feeds/chainlink.json') as f:
        data = json.load(f)
    for elem in data:
        [roundId, answer, startedAt, updatedAt, answeredInRound, decimals] = get_chainlink_data(elem, data[elem]['address'])
        prices.append(calculate_price(answer, decimals))
    return prices

"""
Function: grab_round()
Get data from a specific round
"""
def grab_round(elem, address, roundId):
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f5470eb326af43adadbb81276c2e4675'))
    f = open('contracts/chainlink.json', 'r')
    abi = json.load(f)
    contract = web3.eth.contract(address=address, abi=abi)
    latestData = contract.functions.getRoundData(roundId).call()
    return latestData

""" 
Function: grab_price_change()
Grab last 50 rounds of chainlink data for a specific exchange
 """
def grab_price_change(exchange):
    all_prices = []
    with open('feeds/chainlink.json') as f:
        data = json.load(f)
    [roundId, answer, startedAt, updatedAt, answeredInRound, decimals] = get_chainlink_data(exchange, data[exchange]['address'])
    all_prices.append(calculate_price(answer, decimals))
    for i in range(0, num_vals - 1):
            [roundId, answer, startedAt, updatedAt, answeredInRound] = grab_round(exchange, data[exchange]['address'], roundId - 1)
            all_prices.append(calculate_price(answer, decimals))
    return all_prices[::-1]

"""
Function: get_better_price()
Get the change in price over a certain amount of time!
"""
def get_better_price(exchange, number_values):
    all_prices = []
    with open('feeds/chainlink.json') as f:
        data = json.load(f)
    old_date = datetime.timestamp(datetime.now() - timedelta(days=5))
    [roundId, answer, startedAt, updatedAt, answeredInRound, decimals] = get_chainlink_data(exchange, data[exchange]['address'])
    all_prices.append(calculate_price(answer, decimals))
    while (old_date < startedAt):
        [roundId, answer, startedAt, updatedAt, answeredInRound] = grab_round(exchange, data[exchange]['address'], roundId - 1)
        all_prices.append(calculate_price(answer, decimals))
    round_factor = math.floor(len(all_prices) / number_values)
    if len(all_prices) < number_values:
        round_factor = number_values
    all_prices = all_prices[::round_factor]
    last_offset = abs(len(all_prices) - number_values)
    all_prices = all_prices[last_offset:]
    return all_prices
  
"""
Function: grab_time_change()
Grab the time in between each request for last 50 rounds of chainlink data for an exchange
"""
def grab_time_change(exchange):
    all_diffs = []
    old_timestamp = datetime.now()
    new_timestamp = datetime.now()
    with open('feeds/chainlink.json') as f:
        data = json.load(f)
    [roundId, answer, startedAt, updatedAt, answeredInRound, decimals] = get_chainlink_data(str(exchange), data[str(exchange)]['address'])
    new_timestamp = datetime.utcfromtimestamp(updatedAt)
    for i in range(0, 50):
            [roundId, answer, startedAt, updatedAt, answeredInRound] = grab_round(str(exchange), data[str(exchange)]['address'], roundId - 1)
            old_timestamp = datetime.utcfromtimestamp(updatedAt)
            time_diff = new_timestamp - old_timestamp
            all_diffs.append(time_diff.seconds)
            new_timestamp = old_timestamp
    return all_diffs[::-1]

"""
Function: grab_gas_estimate()
Grabs the gas estimate for getting the latest value of an exchange
"""
def grab_gas_estimate(id_name):
    with open('feeds/chainlink.json') as f:
        data = json.load(f)
    address = (data[id_name]['address'])
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/50b206f08a5745818266c90ac93c86b2'))
    f = open('contracts/chainlink.json', 'r')
    abi = json.load(f)
    contract = web3.eth.contract(address=address, abi=abi)
    return (contract.functions.latestRoundData().estimateGas())

""" 
Function: print_info()
Prints out the info for the user
"""
def print_info(name, roundId, answer, startedAt, updatedAt, answeredInRound, decimals):
    print('Chainlink data on ' + name + ' on Kovan Testnet')
    print("Round Id: " + str(roundId))
    print("Coversation Rate: " + str(calculate_price(answer, decimals)))
    print("Started At: " + str(startedAt))
    print("Updated At: " + str(updatedAt))
    print("\n")

""" 
Function: main
Runs all of the entirety of the helper functions
"""
if __name__ == "__main__":
   print(get_better_price("BTC/USD"))