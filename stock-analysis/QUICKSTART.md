# 快速开始指南

## 项目状态

✅ 项目已完全配置并可以运行！

## 已完成的工作

1. ✅ 创建了完整的项目结构
2. ✅ 实现了所有核心功能模块
3. ✅ 创建了5个Jupyter Notebook教程
4. ✅ 生成了示例数据（5只股票）
5. ✅ 修复了所有配置问题
6. ✅ 生成了示例分析报告

## 立即开始

### 方式1：运行示例脚本（推荐）

```bash
uv run python example.py
```

这将演示所有功能并生成分析报告。

### 方式2：使用Jupyter Notebook

```bash
jupyter lab
```

然后在浏览器中打开 `notebooks/01_data_collection.ipynb` 开始学习。

## 可用的数据文件

已创建以下股票数据（模拟数据）：
- AAPL_stock_data.csv (苹果公司)
- MSFT_stock_data.csv (微软)
- GOOGL_stock_data.csv (谷歌)
- AMZN_stock_data.csv (亚马逊)
- TSLA_stock_data.csv (特斯拉)

每个文件包含5年的每日股票数据（约1300行）。

## 已生成的报告

查看已生成的示例报告：
- HTML报告: [reports/example_report.html](file:///Users/fang/Documents/Code/python-demo/stock-analysis/reports/example_report.html)
- 文本摘要: [reports/example_summary.txt](file:///Users/fang/Documents/Code/python-demo/stock-analysis/reports/example_summary.txt)

## 核心功能演示

### 1. 数据加载

```python
from src.data_loader import load_stock_data

data = load_stock_data('data/AAPL_stock_data.csv', 'AAPL')
print(f"加载了 {len(data)} 行数据")
```

### 2. 技术指标计算

```python
from src.indicators import calculate_technical_indicators

data = calculate_technical_indicators(data)
print(data[['SMA_20', 'RSI_14', 'MACD']].head())
```

### 3. 数据可视化

```python
from src.visualization import plot_price_trend, plot_rsi

plot_price_trend(data, title='AAPL股票价格走势')
plot_rsi(data)
```

### 4. 多股票分析

```python
from src.multi_stock_analysis import load_multiple_stocks, plot_multi_stock_prices

stock_data = load_multiple_stocks(['AAPL', 'MSFT', 'GOOGL'], 'data')
plot_multi_stock_prices(stock_data)
```

### 5. 报告生成

```python
from src.report_generator import save_html_report

save_html_report(data, 'reports/my_report.html', 'AAPL')
```

## Notebook学习路径

按照以下顺序学习：

1. **00_test_kernel.ipynb** - 测试Jupyter内核配置
2. **01_data_collection.ipynb** - 数据获取和加载
3. **02_technical_indicators.ipynb** - 技术指标计算
4. **03_visualization.ipynb** - 数据可视化
5. **04_multi_stock_analysis.ipynb** - 多股票分析
6. **05_final_report.ipynb** - 生成分析报告

## 注意事项

⚠️ **Yahoo Finance API限流**: 由于API限制，当前使用模拟数据。如需下载真实数据：
- 等待几小时后重试
- 使用其他数据源（Alpha Vantage、IEX Cloud等）
- 分批下载，每次下载一只股票后等待2-3秒

## 常见问题

### Q: 如何重新创建示例数据？
```bash
uv run python create_sample_data.py
```

### Q: 如何下载真实数据？
```bash
uv run python download_data.py
```

### Q: Jupyter Notebook无法运行？
确保内核已正确安装：
```bash
python -m ipykernel install --user --name=stock-analysis --display-name "Stock Analysis (Python 3.10)"
```

### Q: 中文字体显示为方框？
这是正常的警告，不影响功能。可以安装中文字体：
```bash
# macOS
brew install font-source-han-sans

# Ubuntu
sudo apt-get install fonts-wqy-zenhei
```

## 项目文件说明

- **create_sample_data.py** - 创建示例数据（推荐使用）
- **download_data.py** - 从Yahoo Finance下载数据（可能遇到限流）
- **example.py** - 完整功能演示
- **test_setup.py** - 环境测试脚本

## 下一步

1. 运行 `uv run python example.py` 查看完整演示
2. 打开 `reports/example_report.html` 查看生成的报告
3. 启动 Jupyter Lab 并运行 Notebook 学习
4. 修改代码实现自己的分析逻辑

## 技术支持

如遇到问题，请查看：
- [README.md](file:///Users/fang/Documents/Code/python-demo/stock-analysis/README.md) - 完整文档
- [pyproject.toml](file:///Users/fang/Documents/Code/python-demo/stock-analysis/pyproject.toml) - 项目配置

---

**祝您使用愉快！**
