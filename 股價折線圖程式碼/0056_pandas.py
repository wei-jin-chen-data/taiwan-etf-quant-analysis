import pandas as pd
import matplotlib.pyplot as plt

# 1. 讀取資料
df = pd.read_csv('ETF0056.csv')

# 2. 處理資料 (新手必學的兩招)
# A. 將民國年轉為西元年：把 '112' 替換成 '2023'，以此類推
df['date'] = df['date'].str.replace('112', '2023').str.replace('113', '2024').str.replace('114', '2025')
df['date'] = pd.to_datetime(df['date'])

# B. 確保股價是數字格式
df['close'] = pd.to_numeric(df['close'])

# 3. 畫圖
plt.figure(figsize=(12, 6)) # 設定圖表大小
plt.plot(df['date'], df['close'], label='0056 收盤價', color='blue')

# 設定圖表標籤
plt.title('0056 Price Trend (2023-2025)', fontsize=15)
plt.xlabel('Date')
plt.ylabel('Price (TWD)')
plt.grid(True) # 加上網格線方便看趨勢
plt.legend()

# 顯示圖表
plt.show()