from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt import black_litterman
from tqdm import tqdm
from pandas import DataFrame, DateOffset
from numpy import array
import pandas as pd
import numpy as np


def portfolio_mix_function(
        style_weights_prior: dict,
        estimation_window: int,
        style_returns: DataFrame,
        p_matrix: array,
        q_matrix: array,
        delta: float,
        tau: float,
        portfolio_start: str,
        portfolio_end: str,
        recursive: bool = False
):
    style_returns = style_returns[(style_returns.index >= pd.to_datetime(portfolio_start) -
                                   DateOffset(months=estimation_window - 1)) & (style_returns.index <= portfolio_end)]
    time_keys = style_returns[style_returns.index >= pd.to_datetime(portfolio_start)].index
    styles_num = style_returns.shape[1]
    bayesian_weights = dict()
    for key in tqdm(time_keys):
        if recursive:
            style_returns_subset = style_returns.loc[:key]
        else:
            style_returns_subset = style_returns[(style_returns.index >= pd.to_datetime(key)
                                                  - DateOffset(months=estimation_window - 1)) & (
                                                         style_returns.index <= key)]
        cov_matrix = CovarianceShrinkage(style_returns_subset.fillna(0), returns_data=True,
                                         log_returns=True, frequency=12).ledoit_wolf('single_factor')
        mu = black_litterman.market_implied_prior_returns(market_caps=style_weights_prior, risk_aversion=5,
                                                          cov_matrix=cov_matrix)
        omega = BlackLittermanModel.default_omega(cov_matrix, P=p_matrix, tau=tau)
        bl_model = BlackLittermanModel(cov_matrix, P=p_matrix, Q=q_matrix, omega=omega, pi=mu)
        weights_key = np.reshape(np.array(list(bl_model.bl_weights(delta).values())), (styles_num, 1))
        bayesian_weights[key] = np.reshape(weights_key, styles_num)
    bayesian_weights = pd.DataFrame(bayesian_weights.values(), index=bayesian_weights.keys())
    bayesian_weights = bayesian_weights.fillna(0).apply(lambda x: x.divide(bayesian_weights.abs().
                                                                           sum(axis=1, skipna=True)))
    bayesian_weights.columns = style_returns.columns
    bayesian_style_return = (bayesian_weights.shift(1) *
                             style_returns[(style_returns.index >= portfolio_start)
                                           & (style_returns.index <= portfolio_end)]).fillna(0).sum(axis=1)
    return bayesian_style_return
