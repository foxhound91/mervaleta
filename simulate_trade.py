"""
As a product owner
I want to simulate one trade per day based on the script's recommendation
So that I can evaluate the index
"""
import io
from datetime import datetime

import functions_framework
import pandas as pd
import requests


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())


def simulate_trades(data, initial_investment, output_stream):
    owned = False
    investment = initial_investment
    shares = 0

    for _, row in data.iterrows():
        formatted_date = datetime.strptime(row['Date'], '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d')
        if row['Recommendation'] == 'BUY':
            if not owned:
                owned = True
                shares = investment / row['IndexPrice']
                output_stream.write(f"INFO - {formatted_date} bought {shares:.2f} shares at {row['IndexPrice']:.2f}<br>")
            else:
                additional_shares = investment / row['IndexPrice']
                shares += additional_shares
                output_stream.write(f"INFO - {formatted_date} bought {additional_shares:.2f} shares at {row['IndexPrice']:.2f}<br>")
        elif row['Recommendation'] == 'SELL' and owned:
            output_stream.write(f"INFO - {formatted_date} sold {shares:.2f} shares at {row['IndexPrice']:.2f}<br>")
            owned = False
            investment = shares * row['IndexPrice']
            shares = 0

    # Calculate final value if still owning the asset
    if owned:
        investment = shares * data.iloc[-1]['IndexPrice']

    return investment


@functions_framework.http
def post_trades_simulation(request):
    output_stream = io.StringIO()
    url = 'https://europe-west2-crypto-catfish-407213.cloudfunctions.net/mervaleta-data-service'
    data = fetch_data(url)
    final_investment_value = simulate_trades(data, 100, output_stream)
    output_stream.write(f"Final Investment Value: ${final_investment_value:.2f}<br>")

    days = len(data)  # Assuming each row in the data represents one day
    aer = ((final_investment_value / 100) ** (365 / days)) - 1
    output_stream.write(f"Annual Equivalent Rate (AER): {aer * 100:.2f}<br>")
    output = output_stream.getvalue()
    output_stream.close()
    return (f"<html><body>{output}</body></html>", 200, {'Content-Type': 'text/html'})
