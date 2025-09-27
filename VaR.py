# Monte Carlo VaR and ES for a 5-ETF Portfolio
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


def run_var_simulation():
    # 1. Portfolio Setup
    tickers = ['SPY', 'QQQ', 'IWM', 'DIA', 'EFA']  # ETFs
    weights = np.array([0.2] * len(tickers))  # equally weighted

    # Get historical prices (last ~2 years)
    end = dt.date.today()
    start = end - dt.timedelta(days=730)
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)['Close']

    # Daily returns
    returns = data.pct_change().dropna()

    # 2. Portfolio Returns
    portfolio_returns = returns.dot(weights)
    mean_ret, std_ret = portfolio_returns.mean(), portfolio_returns.std()

    print("Portfolio weights:")
    for t, w in zip(tickers, weights):
        print(f"{t}: {w:.2f}")

    # 3. Monte Carlo Simulation
    N = 100_000
    simulated_returns = np.random.normal(mean_ret, std_ret, N)

    confidence_levels = [95, 99, 99.9]
    VaRs, ESs = {}, {}

    for cl in confidence_levels:
        VaRs[cl] = np.percentile(simulated_returns, 100 - cl)
        ESs[cl] = simulated_returns[simulated_returns <= VaRs[cl]].mean()
        print(f"{cl}% VaR: {VaRs[cl]:.2%}, Expected Shortfall: {ESs[cl]:.2%}")

    # 4. Scenario Analysis (20% drop in all assets)
    shock_factor = 0.8
    shocked_returns = returns * shock_factor
    shocked_portfolio_returns = shocked_returns.dot(weights)

    print("\nScenario Analysis (20% drop in all assets):")
    print(f"Mean shocked daily return: {shocked_portfolio_returns.mean():.4f}")
    print(f"95% VaR under shock: {np.percentile(shocked_portfolio_returns, 5):.4f}")

    # 5. Visualization
    sns.histplot(simulated_returns, bins=100, kde=True)

    var_colors = {95: 'red', 99: 'orange', 99.9: 'darkred'}
    es_colors = {95: 'blue', 99: 'green', 99.9: 'purple'}

    for cl in confidence_levels:
        plt.axvline(VaRs[cl], color=var_colors[cl], linestyle='--', label=f'{cl}% VaR')
        plt.axvline(ESs[cl], color=es_colors[cl], linestyle=':', label=f'{cl}% ES')

    plt.title('Monte Carlo Returns with VaR and ES')
    plt.xlabel('Daily Portfolio Return')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig("VaR_ES_histogram.png")  # save for README
    plt.show()


if __name__ == "__main__":
    run_var_simulation()