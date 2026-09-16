import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 環境與中文設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

file_path = 'ETF產業佔比.csv'

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path, index_col=0, encoding='Big5')
    except Exception:
        df = pd.read_csv(file_path, index_col=0, encoding='utf-8-sig')
    
    # 2. 資料清洗
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('%', '', regex=True).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].max() > 1:
            df[col] = df[col] / 100

    # 3. 顏色分配
    all_industries = df.index.unique()
    colors_list = list(plt.cm.tab20.colors) + list(plt.cm.Set3.colors) + list(plt.cm.Pastel1.colors)
    industry_colors = {ind: colors_list[i % len(colors_list)] for i, ind in enumerate(all_industries)}

    # 4. 設定畫圖佈局 (5x2)
    fig, axes = plt.subplots(5, 2, figsize=(30, 45)) 
    axes = axes.flatten()

    # 5. 迴圈繪圖
    for i, ticker in enumerate(df.columns):
        plot_data = df[ticker][df[ticker] > 0].sort_values(ascending=False).dropna()
        
        if not plot_data.empty:
            colors = [industry_colors[ind] for ind in plot_data.index]
            explode = [0.05] + [0] * (len(plot_data) - 1)
            
            # 圓餅放大 (維持 radius=1.1)
            wedges, _ = axes[i].pie(
                plot_data, 
                explode=explode,
                labels=None,    
                autopct=None,   
                colors=colors,
                startangle=140,
                radius=1.1      
            )
            
            # 產業佔比列表 (維持間距與寬度)
            legend_labels = [f"{ind}: {val*100:>4.1f}%" for ind, val in plot_data.items()]
            num_cols = 2 if len(plot_data) > 8 else 1
            
            axes[i].legend(
                wedges, 
                legend_labels,
                title=f"【{ticker} 產業佔比】",
                loc="center left",
                bbox_to_anchor=(1.4, 0.5), 
                fontsize=12,
                title_fontsize=14,
                frameon=False,
                ncol=num_cols,
                columnspacing=1.8
            )
            
            # --- 核心修改：標題往下移 ---
            # 透過 y=1.02 手動微調標題高度，使其更靠近圓餅圖
            axes[i].set_title(f'ETF {ticker}', fontsize=28, fontweight='bold', y=1.02)
            
        else:
            axes[i].text(0.5, 0.5, f'{ticker}\n無數據', ha='center', va='center')

    # 6. 全域佈局調整
    plt.suptitle('ETF 成分占比圓餅圖 (2023-2025)', 
                 fontsize=42, y=0.97, fontweight='bold', color='#1a5276')

    plt.subplots_adjust(
        top=0.88, 
        bottom=0.04, 
        left=0.06,   
        right=0.72, 
        hspace=0.7,  
        wspace=0.9   
    )

    plt.show()

else:
    print(f"❌ 找不到檔案：{file_path}")