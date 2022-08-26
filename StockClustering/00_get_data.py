import yfinance as yf
import numpy as np
import pandas as pd

stock_list = [
  "TUPRS.IS", 
  "VAKBN.IS", 
  "KRDMD.IS", 
  "DOHOL.IS", 
  "AKBNK.IS", 
  "TKFEN.IS", 
  "FROTO.IS", 
  "GARAN.IS", 
  "KOZAA.IS", 
  "HALKB.IS", 
  "TCELL.IS", 
  "KOZAL.IS", 
  "VESTL.IS", 
  "YKBNK.IS", 
  "TTKOM.IS", 
  "BIMAS.IS", 
  "PETKM.IS", 
  "ARCLK.IS", 
  "EREGL.IS", 
  "SAHOL.IS",
  "EKGYO.IS",
  "THYAO.IS",
  "PGSUS.IS",
  "ISCTR.IS",
  "KCHOL.IS",
  "ASELS.IS",
  "TAVHL.IS",
  "GUBRF.IS",
  "SISE.IS",
  "SASA.IS"
]

price_data = yf.download(stock_list, period="3y")
price_data = price_data["Adj Close"]

return_data = []

for stock in stock_list:
  stock1y = price_data[stock].resample("1BY").agg(lambda x:x[-1])
  return_data.append(
    {
      'stock': stock,
      'return1y': (np.log(stock1y) - np.log(stock1y.shift(1))).values[-1],
      'return2y': (np.log(stock1y) - np.log(stock1y.shift(2))).values[-1],
      'return3y': (np.log(stock1y) - np.log(stock1y.shift(3))).values[-1],
    }
  )
  
return_data = pd.DataFrame(return_data)
return_data.set_index('stock', inplace=True)

momentum_volatility_data = []

for stock in stock_list:
  print(stock)
  stock3m = price_data[stock].resample("3BM").agg(lambda x:x[-1])
  stock6m = price_data[stock].resample("6BM").agg(lambda x:x[-1])
  stock1y = price_data[stock].resample("1BY").agg(lambda x:x[-1])
  
  momentum_volatility_data.append({
    'stock': stock,
    'momentum_3m' : (np.log(stock3m) - np.log(stock3m.shift(1))).values[-1],
    'momentum_6m' : (np.log(stock6m) - np.log(stock6m.shift(1))).values[-1],
    'momentum_1y' : (np.log(stock1y) - np.log(stock1y.shift(1))).values[-1],
    'volatility_1y' : np.std(price_data[stock].values[-252:]),
    'volatility_2y' : np.std(price_data[stock].values[-504:]),
    'volatility_3y' : np.std(price_data[stock].values),
  })
  
momentum_volatility_data = pd.DataFrame(momentum_volatility_data)
momentum_volatility_data.set_index('stock', inplace=True)

fund_data = []

for stock in stock_list:
  print(stock)
  tckr = yf.Ticker(stock)
  tckr_inf = tckr.info
  fund_data.append({
    'stock': stock,
    'priceToBook': tckr_inf['priceToBook'],
    'marketCap': tckr_inf['marketCap'],
    'returnOnEquity': tckr_inf['returnOnEquity'],
    'earningsGrowth': tckr_inf['earningsGrowth'],
    })
  
fund_data = pd.DataFrame(fund_data)
fund_data.set_index('stock', inplace=True)

final_data = pd.concat([return_data, momentum_volatility_data, fund_data], axis=1)

final_data.to_csv("data.csv")
