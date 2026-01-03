import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional
from .data_loader import load_multiple_stocks
from .indicators import calculate_returns, calculate_cumulative_returns


def create_price_dataframe(stock_data: Dict[str, pd.DataFrame], column: str = 'Close') -> pd.DataFrame:
    """
    创建多股票价格DataFrame
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        
    返回:
        DataFrame: 多股票价格数据
    """
    price_dict = {}
    
    for ticker, data in stock_data.items():
        if column in data.columns:
            price_dict[ticker] = data[column]
    
    price_df = pd.DataFrame(price_dict)
    price_df = price_df.ffill().dropna()
    
    return price_df


def normalize_prices(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    标准化价格（起始点=100）
    
    参数:
        price_df: DataFrame, 多股票价格数据
        
    返回:
        DataFrame: 标准化后的价格数据
    """
    initial_prices = price_df.iloc[0]
    normalized_prices = price_df.div(initial_prices.where(initial_prices != 0, 1)) * 100
    
    return normalized_prices


def plot_multi_stock_prices(
    stock_data: Dict[str, pd.DataFrame],
    column: str = 'Close',
    normalize: bool = True,
    title: str = '多股票价格走势',
    figsize: tuple = (14, 7),
    save_path: Optional[str] = None
) -> None:
    """
    绘制多股票价格走势图
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        normalize: bool, 是否标准化
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    plt.rcParams["font.family"] = ["Heiti TC", "Kaiti SC", "LXGW WenKai", "LiSong Pro", "Kai", "Hannotate SC", "HanziPen SC", "Arial Unicode MS", "sans-serif"]
    plt.rcParams['axes.unicode_minus'] = False
    
    price_df = create_price_dataframe(stock_data, column)
    
    if normalize:
        price_df = normalize_prices(price_df)
        ylabel = '标准化价格 (起始点=100)'
    else:
        ylabel = '价格'
    
    plt.figure(figsize=figsize)
    for column_name in price_df.columns:
        plt.plot(price_df.index, price_df[column_name], label=column_name, linewidth=1.5)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def calculate_returns_correlation(stock_data: Dict[str, pd.DataFrame], column: str = 'Close') -> pd.DataFrame:
    """
    计算收益率相关性矩阵
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        
    返回:
        DataFrame: 相关性矩阵
    """
    price_df = create_price_dataframe(stock_data, column)
    return_df = price_df.pct_change().dropna()
    
    return return_df.corr()


def plot_correlation_heatmap(
    stock_data: Dict[str, pd.DataFrame],
    column: str = 'Close',
    title: str = '股票收益率相关性矩阵',
    figsize: tuple = (10, 8),
    save_path: Optional[str] = None
) -> None:
    """
    绘制相关性热力图
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    plt.rcParams["font.family"] = ["Heiti TC", "Kaiti SC", "LXGW WenKai", "LiSong Pro", "Kai", "Hannotate SC", "HanziPen SC", "Arial Unicode MS", "sans-serif"]
    plt.rcParams['axes.unicode_minus'] = False
    
    corr_matrix = calculate_returns_correlation(stock_data, column)
    
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                fmt='.2f', annot_kws={'size': 10})
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def calculate_stock_metrics(stock_data: Dict[str, pd.DataFrame], column: str = 'Close') -> pd.DataFrame:
    """
    计算多股票的基本指标
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        
    返回:
        DataFrame: 包含各股票指标的DataFrame
    """
    metrics = []
    
    for ticker, data in stock_data.items():
        if column not in data.columns:
            continue
        
        returns = calculate_returns(data, column)
        cumulative_returns = calculate_cumulative_returns(data, column)
        
        metrics.append({
            'Ticker': ticker,
            'Start_Price': data[column].iloc[0],
            'End_Price': data[column].iloc[-1],
            'Total_Return_Pct': (data[column].iloc[-1] / data[column].iloc[0] - 1) * 100,
            'Mean_Return_Pct': returns.mean() * 100,
            'Std_Return_Pct': returns.std() * 100,
            'Max_Drawdown_Pct': (cumulative_returns.cummax() - cumulative_returns).max() * 100,
            'Sharpe_Ratio': (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0,
            'Volatility_Annual': returns.std() * np.sqrt(252) * 100
        })
    
    return pd.DataFrame(metrics).set_index('Ticker')


def plot_returns_comparison(
    stock_data: Dict[str, pd.DataFrame],
    column: str = 'Close',
    title: str = '收益率对比',
    figsize: tuple = (14, 7),
    save_path: Optional[str] = None
) -> None:
    """
    绘制多股票收益率对比图
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    plt.rcParams["font.family"] = ["Heiti TC", "Kaiti SC", "LXGW WenKai", "LiSong Pro", "Kai", "Hannotate SC", "HanziPen SC", "Arial Unicode MS", "sans-serif"]
    plt.rcParams['axes.unicode_minus'] = False
    
    price_df = create_price_dataframe(stock_data, column)
    cumulative_returns = (1 + price_df.pct_change()).cumprod()
    
    plt.figure(figsize=figsize)
    for column_name in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[column_name], 
                label=column_name, linewidth=1.5)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('累计收益率', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_risk_return_scatter(
    stock_data: Dict[str, pd.DataFrame],
    column: str = 'Close',
    title: str = '风险-收益散点图',
    figsize: tuple = (10, 8),
    save_path: Optional[str] = None
) -> None:
    """
    绘制风险-收益散点图
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    plt.rcParams["font.family"] = ["Heiti TC", "Kaiti SC", "LXGW WenKai", "LiSong Pro", "Kai", "Hannotate SC", "HanziPen SC", "Arial Unicode MS", "sans-serif"]
    plt.rcParams['axes.unicode_minus'] = False
    
    metrics = calculate_stock_metrics(stock_data, column)
    
    plt.figure(figsize=figsize)
    plt.scatter(metrics['Volatility_Annual'], metrics['Total_Return_Pct'], 
                s=100, alpha=0.6, c=range(len(metrics)), cmap='viridis')
    
    for i, ticker in enumerate(metrics.index):
        plt.annotate(ticker, (metrics['Volatility_Annual'].iloc[i], 
                             metrics['Total_Return_Pct'].iloc[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    plt.xlabel('年化波动率 (%)', fontsize=12)
    plt.ylabel('总收益率 (%)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def compare_performance(stock_data: Dict[str, pd.DataFrame], column: str = 'Close') -> pd.DataFrame:
    """
    比较多股票表现
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        
    返回:
        DataFrame: 包含各股票表现的DataFrame
    """
    return calculate_stock_metrics(stock_data, column)


def find_best_performer(stock_data: Dict[str, pd.DataFrame], column: str = 'Close', 
                       metric: str = 'Total_Return_Pct') -> tuple:
    """
    找出表现最好的股票
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        metric: str, 评价指标
        
    返回:
        tuple: (股票代码, 指标值)
    """
    metrics = calculate_stock_metrics(stock_data, column)
    
    if metric not in metrics.columns:
        raise ValueError(f"指标 {metric} 不存在")
    
    best_ticker = metrics[metric].idxmax()
    best_value = metrics[metric].loc[best_ticker]
    
    return best_ticker, best_value


def find_worst_performer(stock_data: Dict[str, pd.DataFrame], column: str = 'Close',
                        metric: str = 'Total_Return_Pct') -> tuple:
    """
    找出表现最差的股票
    
    参数:
        stock_data: dict, 键为股票代码，值为DataFrame
        column: str, 价格列名
        metric: str, 评价指标
        
    返回:
        tuple: (股票代码, 指标值)
    """
    metrics = calculate_stock_metrics(stock_data, column)
    
    if metric not in metrics.columns:
        raise ValueError(f"指标 {metric} 不存在")
    
    worst_ticker = metrics[metric].idxmin()
    worst_value = metrics[metric].loc[worst_ticker]
    
    return worst_ticker, worst_value
