import pandas as pd
import numpy as no
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Create a directory to save the plots if it doesn't exist
os.makedirs('images/', exist_ok=True)

#Load the dataset
df = pd.read_csv('data/sales.csv', parse_dates=['ORDERDATE'], encoding='ISO-8859-1')

#Change the column name 'Order Date' to 'Date'
df.rename(columns={'ORDERDATE':'Date'}, inplace=True)
#Convert the 'date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

#set the date as the index
df.set_index('Date', inplace=True)

#Create a new column 'Year' from the index
df['Year'] = df.index.year

monthly_sales = df.resample('ME').sum(numeric_only=True)
yearly_sales = df.resample('YE').sum(numeric_only=True)

#Plot the monthly sales moving average for 3 months
monthly_sales['MovingAvg_3'] = monthly_sales['SALES'].rolling(window=3).mean()

#Plot the monthly sales
plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_sales.index, y=monthly_sales['SALES'], marker = 'o')
plt.title('Monthly Sales')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.savefig('images/monthly_sales.png')
plt.show()









