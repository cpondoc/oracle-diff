"""
File: dia.py
Get important data for the DIA Oracle
"""

""" Necessary Libraries """
import requests

""" 
Function: get_value
Get the value of the coin given the response from the DIA API Endpoint
"""
def get_value(coin):
    r = requests.get("https://api.diadata.org/v1/quotation/" + coin)
    return r.json()

""" 
Function: print_info
Print information relevant to each coin
"""
def print_info(name, price, comparison, time):
    print("DIA Oracle data on " + name + "/" + comparison)
    print("Conversation Rate: " + str(price))
    print("Time Updated: " + str(time))
    print("\n")

""" 
Function: return_price
Returns price from the .json response!
"""
def return_price(coin):
    coin_json = get_value(coin)
    return coin_json['Price']

btc_price = return_price("BTC")
print(btc_price)

""" 
Function: main
Runs all of the entirety of the helper functions
"""
if __name__ == "__main__":
    coins = ["BTC", "ETH", "LTC", "AMPL"]
    for coin in coins:
        coin_json = get_value(coin)
        print_info(str(coin), coin_json['Price'], "USD", coin_json['Time'])