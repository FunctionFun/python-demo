# 股票数据分析与投资模拟项目学习指南

## 📋 项目概述
通过这个项目，你将学习使用Python分析股票数据、可视化结果，并模拟投资策略。即使你是金融新手，我也会带你一步步理解基本概念，掌握从数据获取到策略评估的完整流程。

## 🛠️ 环境配置步骤

### 1. 环境设置
```bash
# 创建项目目录
mkdir -p stock-analysis-project/{data,notebooks,src}
cd stock-analysis-project

# 使用uv初始化项目
uv init

# 安装核心库
uv add pandas numpy matplotlib seaborn jupyterlab yfinance pandas-datareader scikit-learn plotly ipywidgets tqdm pytest mplfinance jinja2 weasyprint

# 注意：weasyprint 需要系统级依赖 (Pango/Cairo)
# Mac: brew install pango
# Ubuntu/Debian: sudo apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

## 📚 学习路径与项目步骤

### 第一阶段：基础知识 (1-2天)

#### 步骤1.1：学习金融基础知识
- 了解股票、股价、涨跌幅、成交量等基本概念
- 理解K线图（开盘价、最高价、最低价、收盘价）
- 学习简单移动平均线(SMA)概念

#### 步骤1.2：获取股票数据
创建 `notebooks/01_data_collection.ipynb`：

```python
import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

# 设置中文字体支持（适配多系统）
plt.rcParams["font.family"] = ["PingFang SC", "Heiti TC", "SimHei", "Arial Unicode MS", "sans-serif"]
plt.rcParams['axes.unicode_minus'] = False 

def load_stock_data(file_path, ticker='AAPL'):  # 增加ticker参数
    """加载股票数据并设置日期索引，不存在则下载"""
    if not os.path.exists(file_path):
        # 新增下载逻辑
        print(f"文件不存在，正在下载{ticker}数据...")
        data = yf.download(ticker)
        data.to_csv(file_path)
        print(f"数据已保存至: {file_path}")
    
    data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    
    if 'Close' not in data.columns:
        data['Close'] = data['Adj Close']
    
    return data

# 加载数据
file_path = "data/AAPL_stock_data.csv"
data = load_stock_data(file_path, 'AAPL')  # 传入ticker参数

# 缺失值检查与处理
print("\n缺失值检查:")
if data.isnull().sum().sum() > 0:
    data = data.ffill() # 使用新版Pandas推荐的ffill()
    print("缺失值已处理")

# 计算基本指标
data['Daily_Change_Pct'] = data['Close'].pct_change() * 100

# 可视化价格走势
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='收盘价')
plt.title('AAPL股票收盘价走势')
plt.legend()
plt.show()
```

### 第二阶段：技术指标计算 (2天)

#### 步骤2.1：编写计算函数
创建 `src/indicators.py` 或在 Notebook 中定义：

```python
def calculate_technical_indicators(df):
    data = df.copy()
    
    # 1. 移动平均线 (SMA)
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # 2. 相对强弱指数 (RSI)
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    # 新增：从第15个数据点开始使用指数移动平均（标准RSI计算方式）
    avg_gain = avg_gain.fillna(0)
    avg_loss = avg_loss.fillna(0)
    for i in range(14, len(gain)):
        avg_gain[i] = (avg_gain[i-1] * 13 + gain[i]) / 14
        avg_loss[i] = (avg_loss[i-1] * 13 + loss[i]) / 14
    
    rs = avg_gain / avg_loss.replace(0, 0.001) # 防止除以0
    data['RSI_14'] = 100 - (100 / (1 + rs))
    
    # 3. MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    return data
```

### 第三阶段：多股票分析 (2-3天)

#### 步骤3.1：多股票对比
创建 `notebooks/06_multi_stock_analysis.ipynb`：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
stock_data = {}

# 模拟加载多只股票
for ticker in tickers:
    # 实际项目中应从data目录读取
    df = pd.read_csv(f"data/{ticker}_stock_data.csv", index_col='Date', parse_dates=True)
    stock_data[ticker] = df['Close']

price_df = pd.DataFrame(stock_data)
# 修正：先向前填充再删除特定缺失值，避免因个别停牌导致整行丢失
price_df = price_df.ffill().dropna()

# 1. 股票价格走势比较（标准化）
# 修正：使用mask避免除零，保留原始数据特性
initial_prices = price_df.iloc[0]
normalized_prices = price_df.div(initial_prices.where(initial_prices != 0, 1)) * 100

plt.figure(figsize=(14, 7))
for column in normalized_prices.columns:
    plt.plot(normalized_prices.index, normalized_prices[column], label=column)
plt.title('股票价格走势比较（起始点=100）')
plt.legend()
plt.show()

# 2. 收益率相关性分析
return_df = price_df.pct_change().dropna()
plt.figure(figsize=(10, 8))
sns.heatmap(return_df.corr(), annot=True, cmap='coolwarm')
plt.title('股票收益率相关性矩阵')
plt.show()
```

### 第四阶段：报告生成 (1天)

#### 步骤4.1：自动化报告
创建 `notebooks/07_final_report.ipynb`：

```python
from jinja2 import Template
import weasyprint
import pandas as pd

# 报告模板定义
report_template = """
<html>
    <head>
        <title>股票分析报告</title>
        <style>
            body { font-family: SimHei, Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
        </style>
    </head>
    <body>
        <h1>投资策略回测报告</h1>
        <p>生成日期: {{ date }}</p>
        <h2>策略表现总结</h2>
        {{ table_html }}
    </body>
</html>
"""

def generate_pdf_report(metrics_df, output_path):
    date_str = pd.Timestamp.now().strftime('%Y-%m-%d')
    html_content = Template(report_template).render(
        date=date_str, 
        table_html=metrics_df.to_html()
    )
    # 生成PDF
    weasyprint.HTML(string=html_content).write_pdf(output_path)
    print(f"报告已保存至: {output_path}")

# 使用示例
# generate_pdf_report(risk_return, "reports/final_analysis.pdf")
```

## 🚀 后续进阶建议
1. **引入机器学习**：尝试使用 `scikit-learn` 预测次日股价方向。
2. **实时数据分析**：使用 `Streamlit` 搭建一个实时监控仪表盘。
3. **风险管理**：加入最大回撤（Max Drawdown）计算和仓位控制逻辑。
