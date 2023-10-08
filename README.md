# Bayesian portfolio mix using Blacklittleman model
### This repository comprised the following files:
1. `style_rets.csv` - includes monthly returns of 5 styles: Basis, Hedging pressure, Momentum, Skewness, and Basis-momentum. 
2. `bayesian_portfolio_mix.py` - defines the function for bayesian style portfolio mix.
3. `Portfolio_mix.ipnb` - shows the results using the sample data.
### Quick start
The aim of style portfolio mix is to combine different style portfolio strategies and determine their weights. For instance, 
there are five style portfolios-basis, hedging pressure, momentum, skewness, and basis-momentum. There are many ways to 
combine them. The simplest method is take equal weights for them 