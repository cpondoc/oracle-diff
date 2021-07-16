'''
File: gas.py
Get historical gas prices using Chainlink oracle

Notes:
- Round Data format = [roundId, answer, startedAt, updatedAt, answeredInRound, decimals]
'''

''' Libraries '''
from datetime import datetime
import scripts.helpers.contract

''' Constants '''
TIME_CHANGE = 20 

''' Smart Contract Set-Up'''
gas_contract = scripts.helpers.contract.get_contract('contracts/chainlink_gas.json', '0x169E633A2D1E6c10dD91238Ba11c4A708dfEF37C')

def get_timestamps():
    '''
    Get the values and the timestamps for each value
    '''
    timestamps = []
    gas_prices = []
    data = gas_contract.functions.latestRoundData().call()
    update_id = data[0]
    for i in range(0, TIME_CHANGE):
        data = gas_contract.functions.getRoundData(update_id).call()
        timestamps.append(data[3])
        gas_prices.append(data[1])
        update_id -= 1
    return gas_prices, timestamps

def get_corresponding_prices(timestamps, gas_times, gas_prices):
    '''
    Gets the corresponding indices of gas prices to time differences
    '''
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