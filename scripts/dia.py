'''
File: dia.py
Get important data for the DIA Oracle

Notes: 
- Only takes in Bitcoin, Litecoin, and Ethereum through their ABI
'''

''' Libraries '''
import requests
import scripts.helpers.contract

''' Smart Contract Set-Up '''
dia_contract = scripts.helpers.contract.get_contract('contracts/dia.json', '0xD47FDf51D61c100C447E2D4747c7126F19fa23Ef')

def get_value(coin):
    '''
    Get the value of the coin given the response from the DIA API Endpoint
    '''
    r = requests.get("https://api.diadata.org/v1/quotation/" + coin)
    return r.json()

def return_price(coin):
    '''
    Returns price from the .json response!
    '''
    coin_json = get_value(coin)
    return coin_json['Price']

def grab_gas_estimate(coin_name):
    '''
    Gets the estimate of gas from pulling info from one data point from the oracle
    '''
    return dia_contract.functions.getCoinInfo((coin_name)).estimateGas()

def print_info(name, price, comparison, time):
    '''
    Print information relevant to each coin
    '''
    print("DIA Oracle data on " + name + "/" + comparison)
    print("Conversation Rate: " + str(price))
    print("Time Updated: " + str(time))
    print("\n")

if __name__ == "__main__":
    '''
    Runs all of the entirety of the helper functions
    '''
    print(dia_contract.functions.getCoinInfo("Bitcoin").call())