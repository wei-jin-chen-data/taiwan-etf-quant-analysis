import pandas as pd
import matplotlib.pyplot as plt
import glob
import matplotlib.dates as mdates
import re

# 1. 環境設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

tickers = ['0050', '006208', '00692', '00922', '00850', '0056', '00919', '00878', '00900', '00929']
fig = plt.figure(figsize=(20, 35))

start_dt = pd.to_datetime('2023-01-01')
end_dt = pd.to_datetime('2025-12-31')

# 3. 遍歷繪圖
for i, ticker in enumerate(tickers):
    search_pattern = f"*{ticker}*.csv"
    files = glob.glob(search_pattern)
    
    if files:
        df = pd.read_csv(files[0], encoding='utf-8-sig')
        
        # --- 日期處理 ---
        def clean_date_strict(x):
            x = str(x).strip()
            if x.startswith('112'): x = '2023' + x[3:]
            elif x.startswith('113'): x = '2024' + x[3:]
            elif x.startswith('114'): x = '2025' + x[3:]
            return x

        df['date'] = df['date'].apply(clean_date_strict)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)
        
        # --- 成交量處理 (去逗號 + 換算百萬股) ---
        df['capacity'] = df['capacity'].astype(str).str.replace(',', '')
        df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce')
        df = df.dropna(subset=['capacity'])
        df['vol_million'] = df['capacity'] / 1_000_000

        # 4. 繪製長條圖
        ax = plt.subplot(5, 2, i + 1)
        
        # 使用橘色長條，設定 width 讓它在長年分下依然清晰
        ax.bar(df['date'], df['vol_million'], color='orange', alpha=0.6, label='成交量(百萬股)', width=1.0)
        
        # 格式設定
        ax.set_title(f'ETF {ticker} ', fontsize=16, fontweight='bold', pad=15)
        ax.set_ylabel('百萬股', fontsize=10)
        ax.set_xlim(start_dt, end_dt)
        ax.grid(True, linestyle=':', alpha=0.5, axis='y') # 只保留水平網格，畫面更乾淨
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m'))
        
        # 左上角縮小小標示
        ax.legend(loc='upper left', fontsize=8, framealpha=0.3)

    else:
        plt.subplot(5, 2, i + 1).text(0.5, 0.5, f'找不到 {ticker} 檔案', ha='center')

# 5. 整體佈局調整
plt.subplots_adjust(top=0.91, bottom=0.05, hspace=0.482, wspace=0.25)
plt.suptitle('2023~2025年 ETF 成交量長條圖', fontsize=28, fontweight='bold', y=0.98)

plt.show()