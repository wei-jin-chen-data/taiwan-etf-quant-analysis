import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 環境與中文設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 載入數據並清洗
df = pd.read_csv('平均配息&填息天數&內扣費用.csv', index_col=0)
df['總配息'] = df['112-114 總累計配息'].astype(str).str.replace(' 元', '').str.strip().astype(float)
df['填息天數'] = df['112-114平均填息天數 '].astype(str).str.replace(' 天', '').str.strip().astype(float)
df['內扣費用_num'] = df['內扣費用'].astype(str).str.replace('%', '').str.strip().astype(float) / 100

# 計算單項得分
df['配息得分'] = (df['總配息'] - df['總配息'].min()) / (df['總配息'].max() - df['總配息'].min()) * 100
df['填息得分'] = (df['填息天數'].max() - df['填息天數']) / (df['填息天數'].max() - df['填息天數'].min()) * 100
df['費用得分'] = (df['內扣費用_num'].max() - df['內扣費用_num']) / (df['內扣費用_num'].max() - df['內扣費用_num'].min()) * 100

# 計算兩種情境的綜合評分
df['綜合評分_情境一'] = (df['配息得分'] * 0.25) + (df['填息得分'] * 0.50) + (df['費用得分'] * 0.25)
df['綜合評分_情境二'] = (df['配息得分'] * 0.25) + (df['填息得分'] * 0.25) + (df['費用得分'] * 0.50)

etf_labels = ['0050', '006208', '00692', '00922', '00850', '0056', '00919', '00878', '00900', '00929']
df.index = etf_labels

# 設定10支ETF的特定點顏色 
etf_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]

# 更淡的 Box 顏色
box_colors_1 = ['#f4f9fd', '#f4fbf4', '#fff5f6', '#fffdf6']
box_colors_2 = ['#f4f9fd', '#f4fbf4', '#fff5f6', '#fdf6fd']

labels = ['配息得分\n(收益)', '填息得分\n(效率)', '費用得分\n(成本)', '綜合價值評分']

# 防止點互相擋到，10支ETF使用固定的、間隔開的x軸偏移量，不會重疊
x_offsets = np.linspace(-0.15, 0.15, 10)

def draw_plot(scenario_data, title, filename, box_colors):
    fig, ax = plt.subplots(figsize=(13, 8))
    
    # 畫 boxplot，關閉預設的異常值圓圈 (showfliers=False)
    box = ax.boxplot(scenario_data, labels=labels, patch_artist=True, showfliers=False,
                      medianprops={'color': '#e056d0', 'linewidth': 2},
                      boxprops={'linewidth': 1.2, 'color': '#95a5a6'},
                      whiskerprops={'color': '#95a5a6'}, capprops={'color': '#95a5a6'})
    
    # 著色
    for patch, color in zip(box['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
        
    # 散點繪製 
    for i, data_series in enumerate(scenario_data):
        y_values = data_series.values
        x_base = i + 1
        for idx in range(10):
            ax.scatter(x_base + x_offsets[idx], y_values[idx], 
                       color=etf_colors[idx], edgecolor='none', s=65, alpha=0.95, zorder=3)
            
    # 右上角圖例,不遮擋圖表
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=etf_colors[k], markersize=9, label=etf_labels[k]) for k in range(10)]
    ax.legend(handles=legend_elements, title="ETF代號", loc="upper left", bbox_to_anchor=(1.02, 1), frameon=True, facecolor='#ffffff', edgecolor='#dcdde1')
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=25, color='#2c3e50')
    ax.set_ylabel('評分 (0-100)', fontsize=13)
    ax.set_ylim(-5, 105)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

# 繪製新圖
draw_plot([df['配息得分'], df['填息得分'], df['費用得分'], df['綜合評分_情境一']], '2023~2025年ETF綜合價值評分分佈', 'ETF_Box_Value_Final_1.png', box_colors_1)
draw_plot([df['配息得分'], df['填息得分'], df['費用得分'], df['綜合評分_情境二']], '2023~2025年ETF綜合價值評分分佈', 'ETF_Box_Value_Final_2.png', box_colors_2)

print("兩張優化圖表已重新繪製完成！")