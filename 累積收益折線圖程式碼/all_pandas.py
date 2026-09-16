import pandas as pd
import matplotlib.pyplot as plt
import glob
import matplotlib.dates as mdates
import re

# 1. 環境與中文設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 2. 定義標的
tickers = ['0050', '006208', '00692', '00922', '00850', '0056', '00919', '00878', '00900', '00929']

fig, axes = plt.subplots(5, 2, figsize=(20, 32))
axes = axes.flatten()

# 統一 X 軸範圍：2023-01-01 到 2025-12-31
start_dt = pd.to_datetime('2023-01-01')
end_dt = pd.to_datetime('2025-12-31')

# 3. 遍歷繪圖
for i, ticker in enumerate(tickers):
    search_pattern = f"*{ticker}*.csv"
    files = glob.glob(search_pattern)
    
    if files:
        df = pd.read_csv(files[0], encoding='utf-8-sig')
        
        # --- 【核心修正】超強效日期清理與轉換 ---
        def clean_date(x):
            x = str(x).strip()
            # 移除所有非數字與非斜線/連字號的字元
            x = re.sub(r'[^\d/\-]', '', x)
            # 民國轉西元強力替換
            x = re.sub(r'^112', '2023', x)
            x = re.sub(r'^113', '2024', x)
            x = re.sub(r'^114', '2025', x)
            return x

        df['date'] = df['date'].apply(clean_date)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # 排序並過濾掉轉換失敗的空值
        df = df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)
        
        # 轉換價格
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df = df.dropna(subset=['close'])

        if not df.empty:
            # --- 計算累積收益率 ---
            initial_price = df['close'].iloc[0]
            df['cum_return'] = (df['close'] / initial_price - 1) * 100

            # --- 繪圖 ---
            ax = axes[i]
            ax.set_xlim(start_dt, end_dt)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            
            # 繪製主線
            ax.plot(df['date'], df['cum_return'], color='#1f77b4', linewidth=2)
            ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.6)
            ax.fill_between(df['date'], df['cum_return'], 0, color='#1f77b4', alpha=0.1)

            ax.set_ylabel('收益率 (%)', fontweight='bold')
            ax.set_title(f'ETF {ticker}', fontsize=18, fontweight='bold', pad=15)
            ax.grid(True, linestyle=':', alpha=0.6)
            
            # 在結尾標註數據 (若最後一筆在 2025 年範圍內)
            final_date = df['date'].iloc[-1]
            final_return = df['cum_return'].iloc[-1]
            ax.annotate(f'{final_return:.1f}%', 
                        xy=(final_date, final_return),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=11, color='#1f77b4', fontweight='bold')
        else:
            axes[i].text(0.5, 0.5, f'{ticker} 數據轉換後為空', ha='center', va='center')

    else:
        axes[i].text(0.5, 0.5, f'找不到 {ticker} 檔案', ha='center', va='center')

# 4. 佈局修正
plt.suptitle('10 支 ETF 累積收益率對比 (2023-2025 終極修復版)', 
             fontsize=26, y=0.985, fontweight='bold')

plt.subplots_adjust(
    top=0.92,
    bottom=0.04,
    left=0.08,
    right=0.92,
    hspace=0.6,
    wspace=0.3
)

plt.show()