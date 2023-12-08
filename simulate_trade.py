"""
As a product owner
I want to simulate one trade per day based on the script's recommendation
So that I can evaluate the index
"""
import pandas as pd
import requests


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())


def simulate_trades(data, initial_investment):
    owned = False
    investment = initial_investment
    shares = 0

    for _, row in data.iterrows():
        if row['Recommendation'] == 'BUY':
            if not owned:
                owned = True
                shares = investment / row['IndexPrice']
                print(f"INFO - {row['Date']} bought {shares:.2f} shares at ", row['IndexPrice'])
            else:
                additional_shares = investment / row['IndexPrice']
                shares += additional_shares
                print(f"INFO - {row['Date']} bought {additional_shares:.2f} shares at ", row['IndexPrice'])
        elif row['Recommendation'] == 'SELL' and owned:
            print(f"INFO - {row['Date']} sold {shares:.2f} shares at ", row['IndexPrice'])
            owned = False
            investment = shares * row['IndexPrice']
            shares = 0

    # Calculate final value if still owning the asset
    if owned:
        investment = shares * data.iloc[-1]['IndexPrice']

    return investment


def main():
    url = 'https://europe-west2-crypto-catfish-407213.cloudfunctions.net/mervaleta-data-service'
    data = fetch_data(url)
    final_investment_value = simulate_trades(data, 100)
    print(f"Final Investment Value: ${final_investment_value:.2f}")

    days = len(data)  # Assuming each row in the data represents one day
    aer = ((final_investment_value / 100) ** (365 / days)) - 1
    print(f"Annual Equivalent Rate (AER): {aer * 100:.2f}%")


if __name__ == "__main__":
    main()
