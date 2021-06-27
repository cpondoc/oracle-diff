import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

"""
# Comparing Oracles
In order to dip my feet into the world of crypto and blockchain development, I decided to analyze different oracles
within the space and compare relevant metrics, enabling me to gain comprehension through practical data science work.

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
The first step is to grab pertinent data from each of the oracles.
"""

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

"""
# Here is a sample line chart
This is pretty cool
"""
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

"""
## Works Cited
[1] https://www.coindesk.com/what-is-an-oracle
"""