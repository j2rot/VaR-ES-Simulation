# Monte Carlo VaR and Expected Shortfall for a 5-ETF Portfolio

This project implements a Monte Carlo simulation in Python to estimate **Value at Risk (VaR)**, **Expected Shortfall (ES)**, and perform **scenario analysis** on a 5-ETF equally weighted portfolio.  

## Features
- Download historical ETF data with `yfinance`
- Compute daily portfolio returns
- Monte Carlo simulation of returns (100,000+ trials)
- Calculate VaR and ES at 95%, 99%, and 99.9% confidence levels
- Perform scenario analysis (e.g., 20% market shock)
- Visualize risk distribution with VaR and ES markers

## Tools & Libraries
- Python  
- NumPy, Pandas  
- Matplotlib, Seaborn  
- yfinance 
