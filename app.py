# Importing essential libraries
import streamlit as st
import numpy as np
import pandas as pd
import scripts.chainlink
import scripts.tellor

"""
# Comparing Oracles
Written by: Christopher Pondoc

In order to dip my feet into the world of crypto and blockchain development, I decided to analyze different oracles
within the space and compare relevant metrics, enabling me to gain comprehension through practical data science work.

*Note: Streamlit data app may take a few seconds to load in data from testnet.*
"""

"""
## Background
Oracles help bring data from the outside world onto the blockchain, which help smart contracts make decisions/dispense money/
perform a plethora of tasks [1]. The data we'll be focusing on comes in the form on **conversion rates**, such as BTC/USD or BTC/ETH.

### Specific Oracles
In the case of this task, we'll be focusing on the following oracles:
* Tellor
* Chainlink
* Band Protocol
* DIA 
"""

""" 
## Grabbing Data
The first step is to grab pertinent data from each of the oracles. In this case, I first decided 

### Conversion Rates
The first data I looked at were simply the pure conversion rates. For this, I simply pulled the data from each
of the smart contracts using their Application Binary Interface (ABI), as well as `web3.py`.

Below is a table of initial results.
"""

# Dataframe for the Oracle
oracles = pd.DataFrame({
    'Name': [],
    'BTC/USD': [],
    'ETH/USD': [],
    'AMPL/ETH': [],
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

# Display data as a table
oracles

"""
### Average Time between Requests
The next metric I decided to look at was the average time in between each request.
"""

"""
### BTC/USD
"""
tellor_btc_prices = scripts.tellor.grab_price_change(tellor_contract, "BTC/USD")
st.line_chart(tellor_btc_prices)

"""
### ETH/USD
"""
tellor_eth_prices = scripts.tellor.grab_price_change(tellor_contract, "ETH/USD")
st.line_chart(tellor_eth_prices)

"""
### LTC/USD
"""
tellor_ltc_prices = scripts.tellor.grab_price_change(tellor_contract, "LTC/USD")
st.line_chart(tellor_ltc_prices)

"""
## Works Cited
[1] https://www.coindesk.com/what-is-an-oracle
"""