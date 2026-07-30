# taiwan-etf-quant-analysis
抓取熱門ETF，分析在各種狀況下表現
# 📊 台股熱門 ETF 量化分析與綜合評分決策模型 (2023-2025)

> 運用 Python 進行多維度台股 ETF 價量、事件衝擊與成分股分析，並建立動態權重的標準化 Scoring 模型，輔助投資人進行理性投資決策。

---

## 📌 專案背景與痛點 (Background & Problem)

在台灣的 ETF 投資市場中，投資人常落入**「高配息迷思」**，單純追逐高殖利率而忽視了：
1. **填息天數過長**：領了股息卻賠了股價，導致本金實質耗損。
2. **總費用率（內扣費用）**：長期持有下，高昂的內扣成本會劇烈侵蝕長期複利收益。

**本專案目標：** 清洗並分析 2023 至 2025 年台股市值型與高股息 ETF 數據，透過資料視覺化進行多維度比對，並建立一個**可動態調整權重的綜合評分決策模型**，客觀評估各 ETF 的綜合表現。

---

## 🛠️ 技術棧 (Tech Stack)

- **程式語言：** Python 3.x
- **數據處理與清洗：** `Pandas`, `NumPy`, `Glob`, `Re` (正規表示法處理民國/西元日期轉換與數值格式化)
- **視覺化與繪圖：** `Matplotlib` (Subplots, Date Formatter, Boxplot, Scatter Jitter, Pie Chart)
- **統計模型：** Min-Max 標準化（Min-Max Normalization）、權重評分模型（Weighted Scoring Model）

---

## 🔍 核心分析與洞察 (Key Insights)

### 1. 價量與趨勢分析 (20MA Trend Analysis)
- **市值型 ETF (如 0050, 006208)：** 20 日移動平均線（20MA）整體呈階梯式緩步墊高，跌破均線後修復能力強。
- **高股息 ETF：** 受到頻繁除息與成分股調整影響，20MA 走勢較為崎嶇且短線波動較顯著。

### 2. 重大事件衝擊評估 (Event Impact Analysis)
- 追蹤 Nvidia AI 浪潮大漲、2024/08/05 盤勢劇烈修正等重大時間點之影響。
- **發現：** 市值型 ETF 因重倉科技龍頭股，在單一利空事件下跌幅較為明顯，但同時展現出**較快的填息與復甦速度**。

### 3. 成分股結構與填息相關性 (Portfolio Analysis)
- 透過產業成分股分析（圓餅圖）顯示：半導體龍頭（如台積電）持股佔比與「填息得分」呈顯著正相關，是確保資產長期實質增值（而非左手換右手）的核心關鍵。

---

## 📐 綜合評分決策模型 (Standardized Scoring Model)

為了打破單一指標的偏誤，本模型將三大關鍵指標轉化為可比對的標準化分數（0~1 分）：

1. **配息金額 (Dividend Yield / Amount)**：衡量現金流回饋
2. **平均填息天數 (Days to Fill Gap)**：衡量資金回籠與本金修復效率（數值越低越好，模型取倒數轉化）
3. **總費用率 (Total Expense Ratio)**：衡量持有成本（數值越低越好，模型取倒數轉化）

### 🧮 評分公式 (Scoring Formula)

$$\text{Score} = (w_1 \times \text{配息得分}) + (w_2 \times \text{填息得分}) + (w_3 \times \text{費用得分})$$

---

### 🎯 動態權重策略比對 (Strategy Weight Scenarios)

本專案針對三種不同投資性格，擬定客製化權重比例：

| 策略導向 | 配息權重 ($w_1$) | 填息權重 ($w_2$) | 費用權重 ($w_3$) | 適合對象 |
| :--- | :---: | :---: | :---: | :--- |
| **1. 收益導向 (Income-Focused)** | **50%** | 25% | 25% | 追求穩定現金流、退休族群 |
| **2. 效率導向 (Efficiency-Focused)** | 25% | **50%** | 25% | 重視資金靈活度與填息速度的投資人 |
| **3. 成本導向 (Cost-Focused)** | 25% | 25% | **50%** | 長期Buy and Hold、極度在意內扣損耗者 |

---

## 📊 視覺化成果展現 (Visualizations)

> *(提示：請將你的分析圖片放至專案資料夾 `images/` 中，並替換下方圖片連結)*

### 1. 20MA 價量趨勢與事件衝擊圖
![20MA Trend Analysis](<img width="2048" height="1173" alt="2023~2025ETF重大事件對收益影響peg" src="https://github.com/user-attachments/assets/3d593c9a-7a08-4946-a32f-33e9131aa030" />
)
*說明：繪製 2023-2025 年間熱門 ETF 價格與 20MA 走勢，並標註重大市場事件節點。*

### 2. 填息天數與費用率箱形圖 (Boxplot & Scatter)
![Gap Days and Expense Ratio](images/expense_vs_gap.png)
*說明：比較市值型與高股息 ETF 在填息天數分佈與內扣費用率上的差異。*

### 3. 三大策略綜合評分排名比較
![Scoring Model Result](images/scoring_result.png)
*說明：展示在收益、效率、成本三種不同權重偏好下，各 ETF 的最終綜合得分與排名變化。*

---

## 📂 專案檔案結構 (Project Structure)

```text
.
├── README.md                 # 專案總覽說明檔案
├── etf_quant_analysis.py     # 主要資料處理、視覺化與評分模型程式碼
├── data/                     # 原始與清洗後之 CSV 數據集 (2023-2025)
│   ├── etf_prices.csv
│   └── etf_dividends.csv
└── images/                   # 視覺化成果圖表
    ├── etf_trend_analysis.png
    ├── expense_vs_gap.png
    └── scoring_result.png
