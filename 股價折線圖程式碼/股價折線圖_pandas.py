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
        
        # --- 數值清理與單位換算 (百萬股) ---
        for col in ['close', 'capacity']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['close', 'capacity'])
        
        # 新增：換算單位為「百萬股」
        df['vol_million'] = df['capacity'] / 1_000_000
        df['MA20'] = df['close'].rolling(window=20).mean()

        # 4. 繪圖
        ax_price = plt.subplot(5, 2, i + 1)
        ax_vol = ax_price.twinx() 
        
        # 成交量 (使用換算後的 vol_million)
        v_bars = ax_vol.bar(df['date'], df['vol_million'], color='orange', alpha=0.3, label='成交量(百萬股)', width=1.0)
        ax_vol.set_ylim(0, df['vol_million'].max() * 4) 
        ax_vol.set_ylabel('成交量 (百萬股)', fontsize=8, color='gray', rotation=270, labelpad=15) # 標註單位
        ax_vol.set_yticks([]) # 隱藏右側刻度，保持畫面乾淨
        
        # 股價與均線
        p_line, = ax_price.plot(df['date'], df['close'], color='#e31a1c', label='收盤價', linewidth=1.5)
        m_line, = ax_price.plot(df['date'], df['MA20'], color='#33a02c', label='20MA', linewidth=1.2, linestyle='--')
        
        ax_price.set_xlim(start_dt, end_dt)
        ax_price.set_title(f'ETF {ticker}', fontsize=16, fontweight='bold', pad=15)
        ax_price.set_ylabel('股價 (TWD)', fontsize=9)
        ax_price.grid(True, linestyle=':', alpha=0.4)
        ax_price.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m'))
        
        # --- 縮小並微調圖例 ---
        lines = [p_line, m_line, v_bars]
        labels = [l.get_label() for l in lines]
        ax_price.legend(
            lines, labels, 
            loc='upper left', 
            fontsize=7,          
            framealpha=0.3,      
            ncol=3,              
            handlelength=0.8,    # 再縮短一點
            handletextpad=0.4,   
            columnspacing=0.8    
        )

    else:
        plt.subplot(5, 2, i + 1).text(0.5, 0.5, f'找不到 {ticker} 檔案', ha='center')

plt.subplots_adjust(top=0.92, bottom=0.05, hspace=0.5, wspace=0.3) # 稍微增加 wspace 留給單位文字
plt.suptitle('2023~2025年 ETF 價量表', fontsize=28, fontweight='bold', y=0.97)

plt.show()