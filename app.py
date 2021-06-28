# Importing essential libraries for parsing data and presentation
import streamlit as st
import numpy as np
import pandas as pd

# Importing scripts from individual oracles
import scripts.chainlink
import scripts.tellor
import scripts.dia
import scripts.band

"""
# Comparing Oracles
Written by: Christopher Pondoc

In order to dip my feet into the world of crypto and blockchain development, I decided to analyze different oracles
within the space and compare relevant metrics, enabling me to gain comprehension through practical data science work.

*Note: Streamlit data app may take a few seconds to load in data from Ethereum Mainnet!*
"""

"""
## Background
Oracles help bring data from the outside world onto the blockchain, which help smart contracts make decisions/dispense money/
perform a plethora of tasks [1]. The data we'll be focusing on comes in the form on **conversion rates**, such as BTC/USD or BTC/ETH.

### Specific Oracles
In the case of this task, we'll be focusing on the following oracles:
* Tellor [2]
* Chainlink [3]
* Band Protocol [4]
* DIA [5]
"""

""" 
## Grabbing Data
The first step is to grab pertinent data from each of the oracles. In this case, I first decided 

### Conversion Rates
The first data I looked at were simply the pure conversion rates. For this, I simply pulled the data from each
of the smart contracts using their Application Binary Interface (ABI), as well as `web3.py`.

Specifically, I decided to key in on the following conversions:
* BTC/USD
* ETH/USD
* AMPL/USD
* LTC/USD

Below is a table of initial results. Note that for the Band Protocol, I had a bit of trouble communicating with their
smart contract to get the values for AMPL and LTC, so I marked those as `-1`.
"""

coins = ["BTC", "ETH", "AMPL", "LTC"] # Coins to look at!

# Dataframe for the Oracle
oracles = pd.DataFrame({
    'Name': [],
    'BTC/USD': [],
    'ETH/USD': [],
    'AMPL/USD': [],
    'LTC/USD': []
})

# Getting data for Chainlink
chainlink_prices = scripts.chainlink.grab_feeds()
chainlink_data = ['Chainlink'] + chainlink_prices
oracles.loc[len(oracles.index)] = chainlink_data

# Getting data for Tellor
tellor_contract = scripts.tellor.set_up_contract()
tellor_prices = scripts.tellor.grab_feeds(tellor_contract)
tellor_data = ['Tellor'] + tellor_prices
oracles.loc[len(oracles.index)] = tellor_data

# Getting data for Dia
dia_data = ['DIA']
for i in range(0, len(coins)):
    dia_data.append(scripts.dia.return_price(coins[i]))
oracles.loc[len(oracles.index)] = dia_data

# Getting data for Band Protocol
band_contract = scripts.band.get_contract()
band_data = ['Band']
for i in range(0, len(coins) - 2):
    band_data.append(scripts.band.return_prices(band_contract, coins[i]))
oracles.loc[len(oracles.index)] = band_data + [-1, -1]

# Display data as a table
oracles

"""
### Change in Exchange Rate over Time
The next metric I decided to look at was the change in value over time of a certain exchange. Specifically,
I looked at the last 50 values of each exchange, and then compared over each exchange. See the line chart for
each exchange, as well as for each protocol, below.

Key:
* 0 - Tellor
* 1 - Chainlink
"""

"""
#### BTC/USD
"""

coin_times = np.zeros((2, 51))

# For BTC
tellor_btc_prices = scripts.tellor.grab_price_change(tellor_contract, "BTC/USD")
chainlink_btc_prices = scripts.chainlink.grab_price_change("BTC/USD")
coin_times[0] = tellor_btc_prices
coin_times[1] = chainlink_btc_prices
st.line_chart(np.transpose(coin_times))

"""
#### ETH/USD
"""
tellor_eth_prices = scripts.tellor.grab_price_change(tellor_contract, "ETH/USD")
st.line_chart(tellor_eth_prices)

"""
#### LTC/USD
"""
tellor_ltc_prices = scripts.tellor.grab_price_change(tellor_contract, "LTC/USD")
st.line_chart(tellor_ltc_prices)

"""
### Average Time Between Each Request
Next, I decided to investigate the time that it took to satisfy each request. When looking at networks
like Tellor, due to the economics of the token, time between each request is not a pertinent 
"""

"""
#### Tellor
This graph takes a look at a couple of different requests for different conversions. The horizontal
axis represents request number while the vertical axis represents number of seconds.

Average amount of time (in seconds): 
"""
exchanges = ["BTC/USD", "ETH/USD"]
average = 0
tellor_times = np.zeros((2, 50))
for i in range(0, 2):
    tellor_current = scripts.tellor.grab_time_change(tellor_contract, exchanges[i])
    average = np.average(tellor_current)
    tellor_times[i] = tellor_current
average
st.line_chart(np.transpose(tellor_times))

"""
## Works Cited
[1] https://www.coindesk.com/what-is-an-oracle

[2] https://tellor.io/

[3] https://chain.link/

[4] https://bandprotocol.com/

[5] https://diadata.org/
"""