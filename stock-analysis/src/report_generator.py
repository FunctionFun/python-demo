import pandas as pd
import numpy as np
from jinja2 import Template
from datetime import datetime
from typing import Dict, Optional
import os


def generate_html_report(
    metrics_df: pd.DataFrame,
    ticker: str = 'AAPL',
    analysis_period: str = '5年',
    additional_info: Optional[Dict] = None
) -> str:
    """
    生成HTML格式的分析报告
    
    参数:
        metrics_df: DataFrame, 包含分析指标的DataFrame
        ticker: str, 股票代码
        analysis_period: str, 分析周期
        additional_info: dict, 额外信息
        
    返回:
        str: HTML内容
    """
    report_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>股票分析报告 - {{ ticker }}</title>
        <style>
            body {
                font-family: 'Heiti TC', 'Kaiti SC', 'LXGW WenKai', 'LiSong Pro', 'Kai', 'Hannotate SC', 'HanziPen SC', Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }
            h2 {
                color: #555;
                margin-top: 30px;
            }
            .info-box {
                background-color: #e8f5e9;
                padding: 15px;
                border-left: 4px solid #4CAF50;
                margin: 20px 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .positive {
                color: #4CAF50;
                font-weight: bold;
            }
            .negative {
                color: #f44336;
                font-weight: bold;
            }
            .footer {
                margin-top: 40px;
                text-align: center;
                color: #666;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>股票分析报告</h1>
            
            <div class="info-box">
                <p><strong>股票代码:</strong> {{ ticker }}</p>
                <p><strong>分析周期:</strong> {{ analysis_period }}</p>
                <p><strong>生成日期:</strong> {{ date }}</p>
            </div>
            
            <h2>策略表现总结</h2>
            {{ table_html }}
            
            {% if additional_info %}
            <h2>附加信息</h2>
            <ul>
                {% for key, value in additional_info.items() %}
                <li><strong>{{ key }}:</strong> {{ value }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            
            <div class="footer">
                <p>本报告由股票分析系统自动生成 | 数据来源: Yahoo Finance</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def format_value(value):
        if pd.isna(value):
            return 'N/A'
        if isinstance(value, (int, float)):
            if abs(value) < 0.01:
                return f'{value:.6f}'
            return f'{value:.2f}'
        return str(value)
    
    def style_value(value, column):
        if pd.isna(value):
            return format_value(value)
        if isinstance(value, (int, float)):
            formatted = format_value(value)
            if 'Return' in column or 'Change' in column:
                return f'<span class="{"positive" if value > 0 else "negative"}">{formatted}%</span>'
            return formatted
        return str(value)
    
    table_html = '<table>\n'
    table_html += '<tr>\n'
    for col in metrics_df.columns:
        table_html += f'<th>{col}</th>\n'
    table_html += '</tr>\n'
    
    for idx, row in metrics_df.iterrows():
        table_html += '<tr>\n'
        table_html += f'<td><strong>{idx}</strong></td>\n'
        for col in metrics_df.columns[1:]:
            table_html += f'<td>{style_value(row[col], col)}</td>\n'
        table_html += '</tr>\n'
    table_html += '</table>\n'
    
    html_content = Template(report_template).render(
        ticker=ticker,
        analysis_period=analysis_period,
        date=date_str,
        table_html=table_html,
        additional_info=additional_info
    )
    
    return html_content


def generate_pdf_report(
    metrics_df: pd.DataFrame,
    output_path: str,
    ticker: str = 'AAPL',
    analysis_period: str = '5年',
    additional_info: Optional[Dict] = None
) -> None:
    """
    生成PDF格式的分析报告
    
    参数:
        metrics_df: DataFrame, 包含分析指标的DataFrame
        output_path: str, 输出文件路径
        ticker: str, 股票代码
        analysis_period: str, 分析周期
        additional_info: dict, 额外信息
    """
    try:
        import weasyprint
    except ImportError:
        print("警告: weasyprint 未安装，无法生成PDF报告")
        print("请运行: pip install weasyprint")
        return
    
    html_content = generate_html_report(
        metrics_df, ticker, analysis_period, additional_info
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    weasyprint.HTML(string=html_content).write_pdf(output_path)
    print(f"PDF报告已保存至: {output_path}")


def save_html_report(
    metrics_df: pd.DataFrame,
    output_path: str,
    ticker: str = 'AAPL',
    analysis_period: str = '5年',
    additional_info: Optional[Dict] = None
) -> None:
    """
    保存HTML格式的分析报告
    
    参数:
        metrics_df: DataFrame, 包含分析指标的DataFrame
        output_path: str, 输出文件路径
        ticker: str, 股票代码
        analysis_period: str, 分析周期
        additional_info: dict, 额外信息
    """
    html_content = generate_html_report(
        metrics_df, ticker, analysis_period, additional_info
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML报告已保存至: {output_path}")


def generate_multi_stock_report(
    stock_metrics: pd.DataFrame,
    output_path: str,
    analysis_period: str = '5年',
    additional_info: Optional[Dict] = None
) -> None:
    """
    生成多股票对比报告
    
    参数:
        stock_metrics: DataFrame, 包含多股票指标的DataFrame
        output_path: str, 输出文件路径
        analysis_period: str, 分析周期
        additional_info: dict, 额外信息
    """
    report_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>多股票分析报告</title>
        <style>
            body {
                font-family: 'Heiti TC', 'Kaiti SC', 'LXGW WenKai', 'LiSong Pro', 'Kai', 'Hannotate SC', 'HanziPen SC', Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #2196F3;
                padding-bottom: 10px;
            }
            h2 {
                color: #555;
                margin-top: 30px;
            }
            .info-box {
                background-color: #e3f2fd;
                padding: 15px;
                border-left: 4px solid #2196F3;
                margin: 20px 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #2196F3;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .positive {
                color: #4CAF50;
                font-weight: bold;
            }
            .negative {
                color: #f44336;
                font-weight: bold;
            }
            .best {
                background-color: #c8e6c9 !important;
            }
            .worst {
                background-color: #ffcdd2 !important;
            }
            .footer {
                margin-top: 40px;
                text-align: center;
                color: #666;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>多股票分析报告</h1>
            
            <div class="info-box">
                <p><strong>分析周期:</strong> {{ analysis_period }}</p>
                <p><strong>生成日期:</strong> {{ date }}</p>
            </div>
            
            <h2>股票表现对比</h2>
            {{ table_html }}
            
            <h2>关键发现</h2>
            {{ summary_html }}
            
            {% if additional_info %}
            <h2>附加信息</h2>
            <ul>
                {% for key, value in additional_info.items() %}
                <li><strong>{{ key }}:</strong> {{ value }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            
            <div class="footer">
                <p>本报告由股票分析系统自动生成 | 数据来源: Yahoo Finance</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def format_value(value):
        if pd.isna(value):
            return 'N/A'
        if isinstance(value, (int, float)):
            if abs(value) < 0.01:
                return f'{value:.6f}'
            return f'{value:.2f}'
        return str(value)
    
    table_html = '<table>\n'
    table_html += '<tr>\n'
    table_html += '<th>股票代码</th>\n'
    for col in stock_metrics.columns:
        table_html += f'<th>{col}</th>\n'
    table_html += '</tr>\n'
    
    for idx, row in stock_metrics.iterrows():
        table_html += '<tr>\n'
        table_html += f'<td><strong>{idx}</strong></td>\n'
        for col in stock_metrics.columns:
            value = row[col]
            formatted = format_value(value)
            if isinstance(value, (int, float)):
                if 'Return' in col or 'Change' in col:
                    formatted = f'<span class="{"positive" if value > 0 else "negative"}">{formatted}%</span>'
            table_html += f'<td>{formatted}</td>\n'
        table_html += '</tr>\n'
    table_html += '</table>\n'
    
    summary_html = '<ul>\n'
    
    best_return_ticker = stock_metrics['Total_Return_Pct'].idxmax()
    worst_return_ticker = stock_metrics['Total_Return_Pct'].idxmin()
    best_sharpe_ticker = stock_metrics['Sharpe_Ratio'].idxmax()
    lowest_volatility_ticker = stock_metrics['Volatility_Annual'].idxmin()
    
    summary_html += f'<li><strong>最佳表现:</strong> {best_return_ticker} (收益率: {stock_metrics.loc[best_return_ticker, "Total_Return_Pct"]:.2f}%)</li>\n'
    summary_html += f'<li><strong>最差表现:</strong> {worst_return_ticker} (收益率: {stock_metrics.loc[worst_return_ticker, "Total_Return_Pct"]:.2f}%)</li>\n'
    summary_html += f'<li><strong>最佳风险调整收益:</strong> {best_sharpe_ticker} (夏普比率: {stock_metrics.loc[best_sharpe_ticker, "Sharpe_Ratio"]:.2f})</li>\n'
    summary_html += f'<li><strong>最低波动率:</strong> {lowest_volatility_ticker} (年化波动率: {stock_metrics.loc[lowest_volatility_ticker, "Volatility_Annual"]:.2f}%)</li>\n'
    summary_html += '</ul>\n'
    
    html_content = Template(report_template).render(
        analysis_period=analysis_period,
        date=date_str,
        table_html=table_html,
        summary_html=summary_html,
        additional_info=additional_info
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"多股票分析报告已保存至: {output_path}")


def create_summary_report(
    data: pd.DataFrame,
    ticker: str,
    output_path: str
) -> None:
    """
    创建简化的摘要报告
    
    参数:
        data: DataFrame, 股票数据
        ticker: str, 股票代码
        output_path: str, 输出文件路径
    """
    summary = {
        '股票代码': ticker,
        '数据开始日期': data.index[0].strftime('%Y-%m-%d'),
        '数据结束日期': data.index[-1].strftime('%Y-%m-%d'),
        '数据天数': len(data),
        '起始价格': f'{data["Close"].iloc[0]:.2f}',
        '结束价格': f'{data["Close"].iloc[-1]:.2f}',
        '最高价': f'{data["High"].max():.2f}',
        '最低价': f'{data["Low"].min():.2f}',
        '平均成交量': f'{data["Volume"].mean():,.0f}',
        '总收益率': f'{((data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100):.2f}%'
    }
    
    report_content = f"""股票分析摘要报告
{'='*50}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

"""
    
    for key, value in summary.items():
        report_content += f"{key}: {value}\n"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"摘要报告已保存至: {output_path}")
