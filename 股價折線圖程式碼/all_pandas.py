import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# 1. 環境與中文設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 2. 定義要分析的代碼
tickers = ['0050', '006208', '00692', '00922', '00850', '0056', '00919', '00878', '00900', '00929']

# 建立一個 5x2 的子圖佈局，總共 10 張小圖
fig, axes = plt.subplots(5, 2, figsize=(15, 20), sharex=True)
axes = axes.flatten() # 將二維陣列轉為一維，方便迴圈使用

found_any = False

# 3. 遍歷每一個代碼並繪圖
for i, ticker in enumerate(tickers):
    # 自動尋找檔名中包含該代碼的 CSV
    search_pattern = f"*{ticker}*.csv"
    files = glob.glob(search_pattern)
    
    if files:
        file_path = files[0]
        try:
            df = pd.read_csv(file_path)
            
            # 日期處理
            df['date'] = df['date'].astype(str).str.strip()
            df['date'] = df['date'].str.replace('112', '2023').str.replace('113', '2024').str.replace('114', '2025')
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # 股價處理
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df = df.dropna(subset=['close', 'date'])
            
            # 繪製在對應的子圖上
            ax = axes[i]
            ax.plot(df['date'], df['close'], label=f'{ticker} Price', color='teal', linewidth=1.5)
            ax.set_title(f'{ticker} 股價走勢', fontsize=12, fontweight='bold')
            ax.set_ylabel('價格 (TWD)')
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper left')
            
            found_any = True
            
        except Exception as e:
            print(f"處理 {ticker} 時出錯: {e}")
    else:
        axes[i].text(0.5, 0.5, f'找不到 {ticker} 檔案', ha='center')

# 4. 整體佈局優化
plt.suptitle('10 支 ETF 原始股價走勢獨立觀測 (2023-2025)', fontsize=20, y=1.02)
plt.tight_layout()
plt.show()