# 🔮 Comparing Different Oracles
Looking at differences between oracles. Simply put, the functions look at the differences in prices across a couple of different cryptocurriences, looking at them on the mainnet in real-time.

Maintained by: Chris Pondoc

![image info](./images/dashboard_screenshot.png)

## Reference
To check out the written version of this report, click [here](https://github.com/cpondoc/oracle-diff/tree/master/style/oracle-report.pdf)

To check out the accompanying video report during Tellor's community call, click [here](https://www.youtube.com/watch?v=QMVl0bInf6o&t=33s)

## Structure
* `helpers` helped me to organize connecting to each contract using `web3.py`, utilizing each application binary interface (ABI), and grabbing the correct values.
* `app.py` is the streamlit app that puts all of the data together.
* `feeds` help me organize IDs for different data feeds (or addresses, depending on the protocol). Contracts contain individual ABIs for each contract.

## Run
To run the app, simply install `requirements.txt` and then run `streamlit run app.py`.

## Analysis
This report analyzes the following oracles:
* Tellor
* Chainlink
* Band Protocol
* DIA

The report also looked at the following conversions:
* BTC/USD
* ETH/USD
* AMPL/USD

## Notes
Note that Band Protocol Network does not support AMPL, despite being listed as one of the available price data feeds.