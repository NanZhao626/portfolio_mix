# Bayesian portfolio mix using Black Littlerman model
### This repository comprised the following files:
1. `style_rets.csv` - includes monthly returns of 5 commodity styles: Basis, Hedging pressure, Momentum, Skewness, and Basis-momentum. 
2. `bayesian_portfolio_mix.py` - defines the function for bayesian style portfolio mix.
3. `Portfolio_mix.ipynb` - shows the results using the sample data.
### Quick start
The aim of style portfolio mix is to combine different style portfolio strategies and determine their weights. For instance, 
there are five style portfolios-basis, hedging pressure, momentum, skewness, and basis-momentum. There are many ways to 
combine them. The simplest method is taking equal weights for each style portfolio which will be called naive approach thereafter.
Other sophisticated methods include mean-variance, minimum-variance, max-diversification optimization, etc. DeMiguel et al. (2009)
evaluates 14 sophisticated models across seven empirical datasets. They show that none is consistently better than the  1/N rule in terms 
of Sharpe ratio, certainty-equivalent return, or turnover, which indicates that, out of sample, the gain from optimal diversification is 
more than offset by estimation error. Therefore, a natural solution to enhance the performance of sophisticated portfolio strategies, 
like the mean-variance optimization, is to systematically combine the naive and the sophisticated approach. A Black Littlerman
framework could be used to serve the purpose.

### Black Littleman model
The Black-Litterman (BL) model combines a prior estimate of returns with views on certain assets, to produce a posterior estimate of 
expected returns. Meanwhile, the model could easily incorporate the shrinkage estimates for covariance matrix (eg, Ledoit and Wolf, 2008),
to reduce the estimation errors even further. The benefit of using the Black Littlerman model for Bayesian portfolio mix is
that the posterior distribution of returns is conjugate and thus the closed form is known, while other Bayesian methods may require
MCMC methods to generate the posterior distibutions for returns which is time-consuming. In addition, using Black-Litterman posterior returns 
results in much more stable portfolios than using mean-historical return.

The Black-Litterman formula is given below:
$$E(R) = [(\tau \Sigma)^{-1}+P^T \Omega^{-1}P]^{-1}[(\tau \Sigma)^{-1}\Pi + P^T\Omega^{-1}Q]$$
* $E(R)$ is a Nx1 vector of expected returns, where N is the number of assets.
* $Q$ is a Kx1 vector of views.
* $P$ is the KxN picking matrix which maps views to the universe of assets. Essentially, it tells the model which view corresponds to which asset(s).
* $\Omega$ is the KxK uncertainty matrix of views.
* $\Pi$ is the Nx1 vector of prior expected returns.
* $\Sigma$ is the NxN covariance matrix of asset returns (as always)
* $\tau$ is a scalar tuning constant.

#### Priors
We set the prior weights for styles-mix as equally weighted. In this example, prior weights is a dictionary:`style_weights_prior = {"Basis": 0.20, "HP": 0.20, 
"Momentum": 0.20, "Skewness": 0.20, "Basis-Mom": 0.20}.` The mean-variance optimization suggests the optimal portfolio weights are
$w_{MV}=\delta^{-1}\Sigma^{-1}\mu$, where $\delta$ is risk-aversion, $Sigma$ is the covariance matrix of returns, and $\mu$ is the mean of returns. 
Through this formula, we could input the priors for weights and the covariance matrix, and generate a prior for the mean of the portfolio:
$$\Pi=\delta\Sigma w_{style_weights_prior}$$