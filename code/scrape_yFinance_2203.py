# Define the ticker list
# All 30 indices on the Dow Jones Industrial Average
import pandas as pd
from datetime import datetime
import yfinance as yf
import csv
import re
import os
import time

tickers_list = ['RTX', 'WBA', 'AAPL', 'MSFT', 'JNJ', 'PG', 'KO','HD',
'CSCO','PFE','NKE','INTC','V','WMT','MRK','BA','JPM','AXP','XOM','GS','CVX','DOW',
'CAT','MCD','IBM','DIS','TRV','MMM','VZ','UNH']

# Fetch the data
data = yf.download(tickers_list,'2020-03-22','2020-04-15',interval ='1d')['Close']
# Print first 5 rows of the data
print(data.head())
# Obtain timestamp in a readable format
to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
# Define working path and filename
path = os.getcwd()
filename = path + '/data/' + to_csv_timestamp + '_yFinance.csv'
# Store dataframe in csv with creation date timestamp
data.to_csv(filename, index = True)