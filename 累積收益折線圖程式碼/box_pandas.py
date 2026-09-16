import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. 環境與中文設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

def final_formal_clean_chart():
    # --- 檔案讀取邏輯 ---
    target_keyword = "平均配息"
    found_file = next((f for f in os.listdir('.') if target_keyword in f), None)
    
    if not found_file:
        print("❌ 找不到檔案")
        return

    try:
        df = pd.read_csv(found_file, index_col=0, encoding='utf-8-sig')
    except:
        df = pd.read_csv(found_file, index_col=0, encoding='cp950')

    # --- 2. 數據清洗函數 ---
    def clean_val(val):
        if pd.isna(val): return 0.0
        s = str(val).replace('元', '').replace('天', '').replace(',', '').strip()
        if '%' in s:
            return float(s.replace('%', '')) / 100.0
        try: return float(s)
        except: return 0.0

    # 自動匹配原始欄位
    col_div = [c for c in df.columns if '總累計配息' in c][0]
    col_day = [c for c in df.columns if '填息天數' in c][0]
    col_cost = [c for c in df.columns if '內扣費用' in c][0]

    df['配息'] = df[col_div].apply(clean_val)
    df['天數'] = df[col_day].apply(clean_val)
    df['成本'] = df[col_cost].apply(clean_val)

    # --- 3. 評分計算 (0-100分) ---
    df['配息分'] = (df['配息'] - df['配息'].min()) / (df['配息'].max() - df['配息'].min()) * 100
    df['填息分'] = (df['天數'].max() - df['天數']) / (df['天數'].max() - df['天數'].min()) * 100
    df['費用分'] = (df['成本'].max() - df['成本']) / (df['成本'].max() - df['成本'].min()) * 100
    df['綜合價值評分'] = (df['配息分'] * 0.5) + (df['填息分'] * 0.25) + (df['費用分'] * 0.25)

    # --- 4. 繪圖與視覺優化 ---
    fig, ax = plt.subplots(figsize=(14, 8))
    
    score_cols = ['配息分', '填息分', '費用分', '綜合價值評分']
    labels = ['配息得分\n(收益)', '填息得分\n(效率)', '內扣費用得分\n(成本)', '綜合價值評分']

    # 繪製背景盒鬚圖，加入 showfliers=False 移除黑圈 (異常值點)
    bp = ax.boxplot([df[c] for c in score_cols], 
                    labels=labels, 
                    patch_artist=True, 
                    widths=0.5, 
                    zorder=1,
                    showfliers=False)  # <-- 關鍵修正：隱藏黑圈

    box_colors = ['#E3F2FD', '#E8F5E9', '#FCE4EC', '#FFF9C4']
    for patch, color in zip(bp['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.3)

    # 為每支 ETF 設定顏色 (使用 tab10 色盤)
    color_map = plt.cm.get_cmap('tab10', len(df))
    original_etfs = df.index.tolist()

    # 繪製點位
    for i, col in enumerate(score_cols):
        x_base = i + 1
        for j, etf_name in enumerate(original_etfs):
            score = df.loc[etf_name, col]
            jitter = np.random.uniform(-0.1, 0.1)
            
            # 格式化代碼：確保開頭有 00
            formatted_name = str(etf_name)
            if not formatted_name.startswith('00'):
                formatted_name = '00' + formatted_name
            
            ax.scatter(x_base + jitter, score, color=color_map(j), 
                       s=150, edgecolors='white', linewidth=0.8, alpha=0.9, zorder=3, 
                       label=formatted_name if i == 0 else "")

    # 圖表裝飾
    ax.set_title('2023~2025年ETF綜合價值評分分佈', fontsize=20, pad=25)
    ax.set_ylabel('得分 (0-100)', fontsize=12)
    ax.set_ylim(-5, 110) # 稍微調整範圍讓頂端點位更清晰
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # 側邊圖例
    ax.legend(title="ETF 代號", bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=11)

    plt.tight_layout()
    plt.show()

# 執行
final_formal_clean_chart()