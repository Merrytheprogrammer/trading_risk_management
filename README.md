# Topological Early Warning System for Financial Markets

This project applies Topological Data Analysis (TDA) to financial time series to detect early warning signals of market crashes. 

Using a 20-day sliding window, the algorithm embeds the daily log-returns of four major tech stocks (AAPL, MSFT, AMZN, NVDA) into a 4-dimensional point cloud. It then uses Vietoris-Rips filtration to track the persistence of 1-dimensional loops ($H_1$). Massive spikes in the $L^1$-Norm of these loops indicate a breakdown in market geometry and serve as a crash warning.


