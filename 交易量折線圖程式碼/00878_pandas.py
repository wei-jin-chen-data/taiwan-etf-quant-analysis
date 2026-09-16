import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 設定字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False

# 1. 讀取與處理日期 (跟剛才一樣)
df = pd.read_csv('ETF00878.csv')
df['date'] = df['date'].str.replace('112', '2023').str.replace('113', '2024').str.replace('114', '2025')
df['date'] = pd.to_datetime(df['date'])

# 2. 處理成交量資料 (關鍵步驟！)
# 因為 csv 裡的成交量有逗號 "223,192,943"，要先去掉逗號再轉成數字
df['capacity'] = df['capacity'].astype(str).str.replace(',', '').astype(float)

# 為了讓圖表更好看，我們把單位換算成「百萬股」
df['vol_million'] = df['capacity'] / 1000000

# 3. 畫圖 (長條圖用 plt.bar)
plt.figure(figsize=(12, 6))
plt.bar(df['date'], df['vol_million'], color='orange', alpha=0.7, label='成交量 (百萬股)')

# 設定圖表標籤


plt.plot(df['date'], df['close'], label='00878 Close Price') # label 改英文
plt.title('00878 Price Trend', fontsize=15) # Title 改英文
plt.xlabel('Date')
plt.ylabel('Price (TWD)')
plt.legend() #

plt.show()