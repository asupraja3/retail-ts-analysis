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
plt.close()

#This groups the DataFrame df by each month (using pd.Grouper(freq='M') on the index, which is the date) and by the
# CITY column. It then sums the SALES values for each group and resets the index to return a flat DataFrame.
monthly_by_region = df.groupby([pd.Grouper(freq='ME'), 'CITY'])['SALES'].sum().reset_index()


plt.figure(figsize=(12, 6))
sns.lineplot( data = monthly_by_region, x = 'Date', y = 'SALES', hue = 'CITY', marker = 'o')
plt.title('Monthly Sales by Region')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.savefig("images/sales_by_region.png")
plt.close()

# Plot moving average vs actual
plt.figure(figsize=(10, 6))
plt.plot(monthly_sales.index, monthly_sales['SALES'], label='Actual')
plt.plot(monthly_sales.index, monthly_sales['MovingAvg_3'], label='3-Month Avg', linestyle='--')
plt.title("Sales Trend with Moving Average")
plt.legend()
plt.ylabel("Sales")
plt.savefig("images/moving_avg.png")
plt.close()

#Anomaly detection
thredhold = monthly_sales['SALES'].mean() - 0.5 * monthly_sales['SALES'].std()
anomalies = monthly_sales[monthly_sales['SALES'] < thredhold]
print(anomalies)

#Plot the anomalies
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales['SALES'], label='Actual')
plt.scatter(anomalies.index, anomalies['SALES'], color='red', label='Anomalies')
plt.title("Sales Anomaly Detection")
plt.legend()
plt.ylabel("Sales")
plt.savefig("images/anomalies.png")
plt.show()

print("All visualizations saved to images/ folder.")




