""" Oracle Comparison
- This project visualizes the differences in oracles, including Chainlink,
Tellor, Bandchain, and others. """

""" Libraries necessary for development """
from web3 import Web3
import json

""" 
Function: get_chainlink_data
This function gets the value of all Chainlink Data necessary for running stuff
"""
def get_chainlink_data(name, address):
    web3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/50b206f08a5745818266c90ac93c86b2'))
    abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    contract = web3.eth.contract(address=address, abi=abi)
    latestData = contract.functions.latestRoundData().call()
    print('Chainlink data on ' + name + ' on Kovan Testnet')
    print(latestData)

""" 
Function: grab_feeds
This function grabs all of the existing data feeds, and then parses the JSON
to get all of the addresses
 """
def grab_feeds():
    with open('./feeds/chainlink.json') as f:
        data = json.load(f)
    for elem in data:
        get_chainlink_data(elem, data[elem]['address'])

if __name__ == "__main__":
    grab_feeds()


