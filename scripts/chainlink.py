'''
File: chainlink.py
Retrieves necessary data and prices from Chainlink!

Notes:

Round Data format = [roundId, answer, startedAt, updatedAt, answeredInRound, decimals]
'''

''' Libraries necessary for development '''
from datetime import datetime, timedelta
import math
import scripts.helpers.contract

''' Constants '''
REF_PATH = 'feeds/chainlink.json' # Path for external data
NUM_VALS = 100 # Number of past values to grab for looking at history
TIME_CHANGE = 20 # Number of time changes to look at
DAYS_BACK = 8 # Number of days to look in past

def calculate_price(price, decimals):
    '''
    Used to help calculate the actual conversion rate from the raw number
    on the blockchain
    '''
    return float(price) / (10 ** decimals)

def get_chainlink_data(address):
    '''
    Grabs the value of all Chainlink Data for the latest round
    '''
    contract = scripts.helpers.contract.get_contract('contracts/chainlink.json', address)
    num_decimals = contract.functions.decimals().call()
    latestData = contract.functions.latestRoundData().call()
    latestData.append(num_decimals)
    return latestData

def grab_feeds():
    '''
    Grabs all of the existing data feeds, and then parses the JSON
    to get all of the addresses
    '''
    prices = []
    data = scripts.helpers.contract.reference_data(REF_PATH)
    for elem in data:
        roundData = get_chainlink_data(data[elem]['address'])
        prices.append(calculate_price(roundData[1], roundData[5]))
    return prices

def grab_round(address, roundId):
    '''
    Get data from a specific round
    '''
    contract = scripts.helpers.contract.get_contract('contracts/chainlink.json', address)
    return contract.functions.getRoundData(roundId).call()

def grab_price_change(exchange):
    '''
    Grab last NUM_VALS rounds of chainlink data for a specific exchange
    '''
    all_prices = []
    data = scripts.helpers.contract.reference_data(REF_PATH)
    roundData = get_chainlink_data(data[exchange]['address'])
    all_prices.append(calculate_price(roundData[1], roundData[5]))
    for i in range(0, NUM_VALS - 1):
            roundData = grab_round(data[exchange]['address'], roundData[0] - 1)
            all_prices.append(calculate_price(roundData[1], roundData[5]))
    return all_prices[::-1]

def get_better_price(exchange, number_values):
    '''
    Get the change in price over a certain amount of time!
    '''
    all_prices = []
    data = scripts.helpers.contract.reference_data(REF_PATH)
    old_date = datetime.timestamp(datetime.now() - timedelta(days=DAYS_BACK)) # Number of days to look back

    # Get current data
    roundData = get_chainlink_data(data[exchange]['address'])
    decimals = roundData[5]
    all_prices.append(calculate_price(roundData[1], decimals))
    while (old_date < roundData[2]):
        roundData = grab_round(data[exchange]['address'], roundData[0] - 1)
        all_prices.append(calculate_price(roundData[1], decimals))
    
    # Cuts down number of values to appropriate amount to display
    round_factor = math.floor(len(all_prices) / number_values)
    if len(all_prices) < number_values:
        round_factor = number_values
    all_prices = all_prices[::round_factor]
    last_offset = abs(len(all_prices) - number_values)
    return all_prices[last_offset:]
  
def grab_time_change(exchange):
    '''
    Grab the time in between each request for last TIME_VALUE rounds of chainlink data for an exchange
    '''
    all_diffs = []
    all_timestamps = []
    old_timestamp = datetime.now()
    new_timestamp = datetime.now()
    data = scripts.helpers.contract.reference_data(REF_PATH)
    roundData = get_chainlink_data(data[str(exchange)]['address'])
    new_timestamp = datetime.utcfromtimestamp(roundData[3])
    all_timestamps.append(datetime.fromtimestamp(roundData[3]))
    for i in range(0, TIME_CHANGE):
        roundData = grab_round(data[str(exchange)]['address'], roundData[0] - 1)
        new_timestamp = datetime.utcfromtimestamp(roundData[3])
        all_timestamps.append(datetime.fromtimestamp(roundData[3]))
        time_diff = new_timestamp - old_timestamp
        all_diffs.append(time_diff.seconds)
        new_timestamp = old_timestamp
    return all_diffs[::-1], all_timestamps[:TIME_CHANGE]

def grab_gas_estimate(id_name):
    '''
    Grabs the gas estimate for getting the latest value of an exchange
    '''
    data = scripts.helpers.contract.reference_data(REF_PATH)
    address = (data[id_name]['address'])
    contract = scripts.helpers.contract.get_contract('contracts/chainlink.json', address)
    return (contract.functions.latestRoundData().estimateGas())

def print_info(name, roundId, answer, startedAt, updatedAt, answeredInRound, decimals):
    '''
    Prints out the info for the user
    '''
    print('Chainlink data on ' + name + ' on Ethereum Mainnet')
    print("Round Id: " + str(roundId))
    print("Coversation Rate: " + str(calculate_price(answer, decimals)))
    print("Started At: " + str(startedAt))
    print("Updated At: " + str(updatedAt))
    print("\n")

if __name__ == "__main__":
    '''
    Runs all of the entirety of the helper functions
    '''
    grab_time_change("BTC/USD")