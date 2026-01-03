# 股票数据分析与投资模拟项目

这是一个完整的股票数据分析项目，使用Python进行股票数据获取、技术指标计算、可视化展示和多股票分析。

## 项目特点

- 数据获取：从Yahoo Finance获取实时和历史股票数据
- 技术指标：计算SMA、EMA、RSI、MACD、布林带等常用技术指标
- 数据可视化：丰富的图表展示，包括K线图、指标图、相关性热力图等
- 多股票分析：支持多只股票的对比分析和相关性分析
- 报告生成：自动生成HTML和PDF格式的分析报告
- 模块化设计：清晰的代码结构，易于扩展和维护

## 项目结构

```
stock-analysis/
├── data/                      # 数据存储目录
│   ├── AAPL_stock_data.csv    # 股票数据文件
│   └── ...
├── notebooks/                 # Jupyter Notebook教程
│   ├── 00_test_kernel.ipynb   # 内核测试
│   ├── 01_data_collection.ipynb
│   ├── 02_technical_indicators.ipynb
│   ├── 03_visualization.ipynb
│   ├── 04_multi_stock_analysis.ipynb
│   └── 05_final_report.ipynb
├── reports/                   # 生成的报告目录
│   ├── AAPL_analysis_report.html
│   ├── AAPL_analysis_report.pdf
│   └── ...
├── src/                       # 源代码
│   ├── __init__.py
│   ├── data_loader.py         # 数据加载模块
│   ├── indicators.py          # 技术指标计算模块
│   ├── visualization.py      # 可视化模块
│   ├── multi_stock_analysis.py # 多股票分析模块
│   └── report_generator.py   # 报告生成模块
├── create_sample_data.py      # 创建示例数据脚本
├── download_data.py           # 数据下载脚本
├── example.py                 # 示例脚本
├── test_setup.py              # 环境测试脚本
├── pyproject.toml            # 项目配置文件
└── README.md                 # 项目说明文档
```

## 环境要求

- Python 3.9 或更高版本
- uv (推荐的包管理工具) 或 pip

## 环境配置

### 1. 安装系统依赖

**macOS:**
```bash
brew install pango
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

### 2. 克隆或下载项目

```bash
cd /path/to/your/workspace
git clone <repository-url> stock-analysis
cd stock-analysis
```

### 3. 使用uv安装依赖（推荐）

```bash
# 安装uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\\Scripts\\activate  # Windows
```

### 4. 使用pip安装依赖（备选方案）

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\\Scripts\\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 5. 验证安装

```bash
python -c "import pandas, numpy, matplotlib, yfinance; print('依赖安装成功！')"
```

## 快速开始

### 1. 创建示例数据（推荐）

由于Yahoo Finance API限流，建议先创建示例数据进行学习和测试：

```bash
uv run python create_sample_data.py
```

这将创建5只股票（AAPL、MSFT、GOOGL、AMZN、TSLA）的模拟数据，数据保存在`data/`目录。

### 2. 运行测试脚本

首先运行测试脚本，确保环境配置正确：

```bash
uv run python test_setup.py
```

### 3. 运行示例脚本

查看完整的功能演示：

```bash
uv run python example.py
```

### 4. 启动Jupyter Lab

```bash
jupyter lab
```

### 5. 按顺序运行Notebook

按照以下顺序学习项目：

1. **01_data_collection.ipynb** - 学习如何获取股票数据
2. **02_technical_indicators.ipynb** - 学习技术指标计算
3. **03_visualization.ipynb** - 学习数据可视化
4. **04_multi_stock_analysis.ipynb** - 学习多股票分析
5. **05_final_report.ipynb** - 学习生成分析报告

### 3. 使用Python脚本

你也可以直接使用Python脚本：

```python
import sys
sys.path.append('.')

from src.data_loader import load_stock_data
from src.indicators import calculate_technical_indicators
from src.visualization import plot_price_trend

# 加载数据
data = load_stock_data('data/AAPL_stock_data.csv', 'AAPL')

# 计算技术指标
data = calculate_technical_indicators(data)

# 绘制图表
plot_price_trend(data, title='AAPL股票走势')
```

## 核心功能

### 数据加载

```python
from src.data_loader import load_stock_data, load_multiple_stocks

# 加载单只股票
data = load_stock_data('data/AAPL_stock_data.csv', 'AAPL')

# 加载多只股票
stock_data = load_multiple_stocks(['AAPL', 'MSFT', 'GOOGL'], 'data')
```

### 技术指标计算

```python
from src.indicators import calculate_technical_indicators

# 计算所有技术指标
data = calculate_technical_indicators(data)

# 可用指标：SMA_20, SMA_50, RSI_14, MACD, Signal_Line, 
# MACD_Histogram, BB_Upper, BB_Middle, BB_Lower等
```

### 数据可视化

```python
from src.visualization import (
    plot_price_trend,
    plot_candlestick,
    plot_rsi,
    plot_macd,
    plot_bollinger_bands
)

# 绘制价格走势
plot_price_trend(data, title='股票价格走势')

# 绘制K线图
plot_candlestick(data, mav=[5, 10, 20])

# 绘制RSI指标
plot_rsi(data)
```

### 多股票分析

```python
from src.multi_stock_analysis import (
    plot_multi_stock_prices,
    calculate_stock_metrics,
    plot_risk_return_scatter
)

# 绘制多股票价格对比
plot_multi_stock_prices(stock_data)

# 计算股票指标
metrics = calculate_stock_metrics(stock_data)

# 绘制风险-收益散点图
plot_risk_return_scatter(stock_data)
```

### 报告生成

```python
from src.report_generator import (
    save_html_report,
    generate_pdf_report,
    generate_multi_stock_report
)

# 生成HTML报告
save_html_report(metrics_df, 'reports/report.html', 'AAPL')

# 生成PDF报告
generate_pdf_report(metrics_df, 'reports/report.pdf', 'AAPL')

# 生成多股票对比报告
generate_multi_stock_report(stock_metrics, 'reports/multi_report.html')
```

## 常见问题

### 1. Yahoo Finance API限流问题

**问题**: 下载数据时出现"Too Many Requests"错误

**解决方案**:
- 使用示例数据进行学习和测试：`uv run python create_sample_data.py`
- 等待一段时间后重试（通常需要等待几小时）
- 使用不同的数据源（如Alpha Vantage、IEX Cloud等）
- 分批下载，每次下载一只股票后等待2-3秒

### 2. weasyprint安装失败

如果遇到weasyprint安装问题，可以跳过PDF生成功能，只使用HTML报告：

```bash
pip install weasyprint --no-cache-dir
```

或者使用系统包管理器安装：

```bash
# macOS
brew install pango

# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

### 2. 数据下载失败

如果Yahoo Finance数据下载失败，可能是网络问题或API限制。可以：
- 使用示例数据：`uv run python create_sample_data.py`
- 检查网络连接
- 等待一段时间后重试
- 使用VPN（如果在中国大陆）

### 3. 中文字体显示问题

如果图表中中文显示为方框，确保系统已安装中文字体：
- macOS: 系统自带PingFang SC
- Linux: 安装`fonts-wqy-zenhei`或`fonts-wqy-microhei`
- Windows: 系统自带SimHei

## 扩展功能

### 添加新的技术指标

在`src/indicators.py`中添加新的计算函数：

```python
def calculate_custom_indicator(df, column='Close'):
    # 实现你的指标计算逻辑
    return indicator_values
```

### 添加新的可视化

在`src/visualization.py`中添加新的绘图函数：

```python
def plot_custom_chart(data, **kwargs):
    # 实现你的可视化逻辑
    plt.show()
```

### 集成机器学习

可以使用scikit-learn进行股价预测：

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 准备数据
X = data[['SMA_20', 'RSI_14', 'MACD']].dropna()
y = data['Close'].shift(-1).loc[X.index]

# 训练模型
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 预测
predictions = model.predict(X_test)
```

## 性能优化建议

1. **数据缓存**：首次下载后，数据会自动缓存到`data/`目录，避免重复下载
2. **批量处理**：使用`load_multiple_stocks`批量加载多只股票数据
3. **增量更新**：只下载最近的数据，而不是全部重新下载

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过GitHub Issues联系。

## 致谢

- 数据来源：Yahoo Finance
- 参考文档：pandas、numpy、matplotlib、yfinance官方文档

---

**祝您学习愉快！**
