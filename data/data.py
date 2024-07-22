import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the indices and their tickers
indices = {
    'FTSE 100': '^FTSE',
    'S&P 100': '^OEX',
    'S&P 500': '^GSPC',
    'Nikkei 225': '^N225',
    'Kospi': '^KS11'
}

# Define the date range
start_date = '2006-01-01'
end_date = '2022-12-31'

# Function to get the index and its components data
def fetch_index_data(index_name, index_ticker):
    # Fetch index data
    index_data = yf.download(index_ticker, start=start_date, end=end_date)['Close']
    
    # Fetch components data
    ticker = yf.Ticker(index_ticker)
    try:
        components = ticker.get_info()['components']
    except KeyError:
        components = ticker.tickers
    
    components_data = yf.download(components, start=start_date, end=end_date)['Close']
    
    # Combine index data and components data
    combined_data = pd.concat([index_data, components_data], axis=1)
    combined_data.rename(columns={'Close': index_name}, inplace=True)
    
    # Save to CSV
    filename = f'{index_name}.csv'
    combined_data.to_csv(filename)
    print(f'{filename} saved successfully.')

# Fetch and save data for each index
for index_name, index_ticker in indices.items():
    fetch_index_data(index_name, index_ticker)
