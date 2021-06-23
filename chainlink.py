""" 
File: chainlink.py
Retrieves necessary data and prices from Chainlink!
"""

""" Libraries necessary for development """
from web3 import Web3
import json

""" Used to help calculate the actual conversion rate from the raw number
on the blockchain """
def calculate_price(price, decimals):
    return float(price) / (10 ** decimals)

""" 
Function: get_chainlink_data
This function gets the value of all Chainlink Data necessary for running stuff
"""
def get_chainlink_data(name, address):
    web3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/50b206f08a5745818266c90ac93c86b2'))
    abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    contract = web3.eth.contract(address=address, abi=abi)
    num_decimals = contract.functions.decimals().call()
    latestData = contract.functions.latestRoundData().call()
    latestData.append(num_decimals)
    return latestData

""" 
Function: grab_feeds
This function grabs all of the existing data feeds, and then parses the JSON
to get all of the addresses
 """
def grab_feeds():
    with open('./feeds/chainlink.json') as f:
        data = json.load(f)
    for elem in data:
        [roundId, answer, startedAt, updatedAt, answeredInRound, decimals] = get_chainlink_data(elem, data[elem]['address'])
        print_info(elem, roundId, answer, startedAt, updatedAt, answeredInRound, decimals)


""" 
Function: print_info
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
    grab_feeds()
    #[roundId, answer, startedAt, updatedAt, answeredInRound] = grab_feeds()


