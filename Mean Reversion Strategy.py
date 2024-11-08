import yfinance as yf 
import datetime as dt 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import statsmodels.api as sm 
import warnings
warnings.filterwarnings('ignore')
# To perform ADF Test
from statsmodels.tsa.stattools import adfuller
#help(adfuller)



end_date = dt.date.today()
start_date = end_date - dt.timedelta (days= 500)

#
a = ['CIPLA.NS',"TCS.NS"]

for stock in a:
 data = yf.download(a, start = start_date, end = end_date ,auto_adjust=True)


data["Moving_average"] = data["Close"].rolling(window = 5).mean()
data["Standard_deviation"] = data["Close"].rolling(window = 5).std()  

data["Upper_band"] = data["Moving_average"] + .6*data["Standard_deviation"]
data["Lower_band"] = data["Moving_average"] - .6*data["Standard_deviation"]      

#Long Position    
data["Long_entry"] = data["Lower_band"] > data["Close"]
data["Exit_long"] = data["Close"] >= data["Moving_average"]

#Stroring the Value of Long and short 
data["Position_long"] = np.nan

data.loc[data["Long_entry"],"Position_long"] = 1
data.loc[data["Exit_long"],"Position_long"] = 0

data["Position_long"] = data["Position_long"].fillna(method = "ffill")

#Short Position
data["Short_entry"] = data["Upper_band"] < data["Close"]
data["Exit_short"] = data["Close"] <= data["Moving_average"]

data["Short_long"] = np.nan

data.loc[data["Short_entry"], "Short_long"] = -1
data.loc[data["Exit_short"], "Short_long"] = 0 

#Filling all the values of rest column 
data["Short_long"] = data["Short_long"].fillna(method = "ffill") 

#Combining all the short and long values 
data["Position"] = data["Position_long"] + data["Short_long"]

#Valuecounts 
#a = data["Position"].value_counts()

#Profit and Loss 
data["Price_difference"] = data["Close"]- data["Close"].shift()
data["Profit_loss"] = data["Position"].shift() - data["Price_difference"] 
data["Cumpnl"] = data["Profit_loss"].cumsum()
#print(data["Cumpnl"].tail(1))

#Return
data["pct_change"] = data["Close"].pct_change()
data["SS Return"] = data["Position"].shift(1)*data["pct_change"]
data["cumcr"] = (data["SS Return"] + 1).cumprod()
#print(data["cumcr"])

data["cumcr"].plot()
plt.xlabel("Date")
plt.ylabel("cumcr")

#plt.figure(figsize=(20,15))
plt.title(f"Return of {a} ")  
plt.show()  




