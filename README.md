# Comparing Different Oracles
Looking at differences between oracles. Simply put, the functions look at the differences in prices across a couple of different cryptocurriences, looking at them on the mainnet in real-time.

Maintained by: Chris Pondoc

## Structure
* `helpers` helped me to organize connecting to each contract using `web3.py`, utilizing each application binary interface (ABI), and grabbing the correct values.
* `app.py` is the streamlit app that puts all of the data together.
* `feeds` help me organize IDs for different data feeds (or addresses, depending on the protocol). Contracts contain individual ABIs for each contract.

## Run
To run the app, simply install `requirements.txt` and then run `streamlit run app.py`.

## Conversions
* BTC/USD
* ETH/USD
* AMPL/USD
* LTC/USD

## Notes
Note that Band Protocol Network does not support AMPL or LTC, despite being listed as one of the available price data feeds.

## Updates
* 6/28 - Fixing up adding Chainlink, looking at change in time, and even adding in gas prices!
* 6/25 - Weekend of 6/27: Finalized calculations for the Tellor oracle, made updates/decided on presentation for other oracles.
* 6/24 - Data from just about every oracle is successfully being collected. Now need to consider a couple of other factors
    * Quantities/metrics to calculate
    * Unifying the logic
    * Style + Modularization if necessary