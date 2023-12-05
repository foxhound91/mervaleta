"""
As a product owner
I want to simulate one trade per day based on the script's recommendation
So that I can evaluate the index
"""
import pandas as pd


def read_data(file_path):
    return pd.read_csv(file_path)


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
    file_path = 'index_record.csv'
    data = read_data(file_path)
    final_investment_value = simulate_trades(data, 100)
    print(f"Final Investment Value: ${final_investment_value:.2f}")

    days = len(data)  # Assuming each row in the data represents one day
    AER = ((final_investment_value / 200) ** (365 / days)) - 1
    print(f"Annual Equivalent Rate (AER): {AER * 100:.2f}%")


if __name__ == "__main__":
    main()
