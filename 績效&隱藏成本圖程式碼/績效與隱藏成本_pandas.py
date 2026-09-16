import pandas as pd
import matplotlib.pyplot as plt
import re

# 1. 環境設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 2. 讀取資料
# 注意：這裡檔案名稱需確認與你資料夾中的 CSV 一致
try:
    df = pd.read_csv('ETF.csv', index_col=0, dtype={0: str}, encoding='utf-8-sig')
except:
    df = pd.read_csv('ETF.csv', index_col=0, dtype={0: str}, encoding='cp950')

# 3. 定義清洗函數
def clean_to_float(val):
    if pd.isna(val): return 0.0
    # 移除百分比符號並處理數值
    s = str(val).replace('%', '').strip()
    match = re.search(r"[-+]?\d*\.\d+|\d+", s)
    if match:
        num = float(match.group())
        # 如果原始字串包含 %，則轉換為小數 (例如 0.22% -> 0.22)
        # 這裡根據你的需求，若圖表 Y 軸是 Percentage，可直接回傳 num
        return num
    return 0.0

# 4. 準備數據與格式化代號 (補上 00)
raw_tickers = df.index.astype(str).str.strip().tolist()
# 格式化代號邏輯：若不滿 4 位或沒以 00 開頭則補上
tickers = [t if t.startswith('00') else f'00{t}' for t in raw_tickers]

# 取得欄位名稱 (自動匹配)
col_div = [c for c in df.columns if '總累計配息' in c or 'Total Dividend' in c][0]
col_day = [c for c in df.columns if '填息天數' in c or 'Days to Recovery' in c][0]
col_cost = [c for c in df.columns if '內扣費用' in c or 'Expense Ratio' in c][0]

dividends = [clean_to_float(df.loc[t, col_div]) for t in raw_tickers]
recovery_days = [clean_to_float(df.loc[t, col_day]) for t in raw_tickers]
expense_ratios = [clean_to_float(df.loc[t, col_cost]) for t in raw_tickers]

# 5. 開始畫圖 (建立 3 個子圖)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15), sharex=True)

# 子圖 1：2023~2025 總累計配息
ax1.bar(tickers, dividends, color='#2ecc71', alpha=0.7)
ax1.set_title('2023~2025 總累計配息', fontsize=16, fontweight='bold', pad=15)
ax1.set_ylabel('配息金額 (元)')

# 子圖 2：平均填息天數
ax2.bar(tickers, recovery_days, color='#e74c3c', alpha=0.7)
ax2.set_title('平均填息天數', fontsize=16, fontweight='bold', pad=15)
ax2.set_ylabel('天數')

# 子圖 3：內扣費用
ax3.bar(tickers, expense_ratios, color='#3498db', alpha=0.7)
ax3.set_title('內扣費用', fontsize=16, fontweight='bold', pad=15)
ax3.set_ylabel('百分比 (%)')

# 在最後一個圖增加 X 軸標籤
ax3.set_xlabel('ETF 代號', fontsize=12)

# 共同優化：增加網格與數值標籤
for ax in [ax1, ax2, ax3]:
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}' if height < 1 else f'{height:.1f}', 
                    (p.get_x() + p.get_width()/2., height),
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()