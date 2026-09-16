import pandas as pd
import matplotlib.pyplot as plt
import glob
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch

# 1. 環境設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

tickers = ['0050', '006208', '00692', '00922', '00850', '0056', '00919', '00878', '00900', '00929']
fig = plt.figure(figsize=(26, 42)) 

# --- A. 彩色事件定義 ---
events = [
    ('2023-05-25', 'NVIDIA AI浪潮', '#1f77b4'), 
    ('2024-08-05', '美國經濟衰退擔憂', '#2ca02c'),
    ('2025-04-07', '關稅政策衝擊', '#d62728')
]

# --- B. 左側重大事件表 (縮減右框線版) ---
text_x = 0.02 # 文字起始位置稍微往左微調以適應窄框

plt.figtext(text_x, 0.70, "【 2023 重大事件 】", fontsize=16, color='#1f77b4', fontweight='bold')
plt.figtext(text_x, 0.675, "● 05/25 NVIDIA AI浪潮", fontsize=14, color='#1f77b4')

plt.figtext(text_x, 0.58, "【 2024 重大事件 】", fontsize=16, color='#2ca02c', fontweight='bold')
plt.figtext(text_x, 0.555, "● 08/05 美國衰退擔憂", fontsize=14, color='#2ca02c')

plt.figtext(text_x, 0.46, "【 2025 重大事件 】", fontsize=16, color='#d62728', fontweight='bold')
plt.figtext(text_x, 0.435, "● 04/07 關稅政策衝擊", fontsize=14, color='#d62728')

# 背景框寬度從 0.18 縮減至 0.15，起點 0.015
box = FancyBboxPatch((0.015, 0.40), 0.15, 0.35, transform=fig.transFigure,
                     facecolor='#fdfdfd', edgecolor='#ced4da', alpha=0.9,
                     boxstyle="round,pad=0.01", mutation_scale=1, zorder=-1)
fig.patches.append(box)

# 統一時間跨度
start_dt = pd.to_datetime('2023-01-01')
end_dt = pd.to_datetime('2025-12-31')

# 2. 遍歷繪圖
for i, ticker in enumerate(tickers):
    search_pattern = f"*{ticker}*.csv"
    files = glob.glob(search_pattern)
    
    if files:
        df = pd.read_csv(files[0], encoding='utf-8-sig')
        df['date'] = pd.to_datetime(df['date'].apply(lambda x: str(x).replace('112', '2023').replace('113', '2024').replace('114', '2025')))
        df = df.sort_values('date').reset_index(drop=True)
        df['close'] = pd.to_numeric(df['close'].astype(str).str.replace(',', ''), errors='coerce')
        df['cum_return'] = (df['close'] / df['close'].iloc[0] - 1) * 100

        ax = plt.subplot(5, 2, i + 1)
        ax.plot(df['date'], df['cum_return'], color='#7f8c8d', linewidth=1.5, alpha=0.4)
        
        y_max = df['cum_return'].max()
        y_min = df['cum_return'].min()
        y_range = y_max - y_min

        # --- C. 事件標註 ---
        for edate, ename, ecolor in events:
            edt = pd.to_datetime(edate)
            ax.axvline(edt, color=ecolor, linestyle='--', alpha=0.4, linewidth=1.2)
            
            day_data = df[df['date'] <= edt].tail(2)
            if len(day_data) == 2:
                change = ((day_data['close'].iloc[1] / day_data['close'].iloc[0]) - 1) * 100
                v_pos = y_max - (y_range * 0.25) if change > 0 else y_min + (y_range * 0.25)
                
                ax.text(edt, v_pos, f'{change:+.1f}%', color=ecolor, 
                        fontsize=12, fontweight='bold', ha='center',
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

        ax.set_title(f'ETF {ticker}', fontsize=20, fontweight='bold', pad=15)
        ax.set_ylabel('收益率 (%)', fontsize=12)
        ax.set_xlim(start_dt, end_dt)
        ax.axhline(0, color='black', linewidth=0.8, alpha=0.2)
        ax.grid(True, linestyle=':', alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m'))
        plt.xticks(fontsize=10)

    else:
        plt.subplot(5, 2, i + 1).text(0.5, 0.5, f'找不到 {ticker}', ha='center')

# --- D. 佈局核心修正 ---
# left 縮減至 0.20，讓圖表向左側窄框靠攏，減少中間留白
plt.subplots_adjust(left=0.177, right=0.97, top=0.88, bottom=0.04, hspace=0.7, wspace=0.28)

# 大標題中心點隨之移動
plt.suptitle('2023~2025年 台股重大事件對 ETF 收益影響', 
             fontsize=38, fontweight='bold', y=0.96, x=0.57)

plt.show()
