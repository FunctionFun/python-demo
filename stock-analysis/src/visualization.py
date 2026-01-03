import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List
import mplfinance as mpf


def setup_chinese_font():
    """
    设置中文字体支持
    """
    plt.rcParams["font.family"] = ["Heiti TC", "Kaiti SC", "LXGW WenKai", "LiSong Pro", "Kai", "Hannotate SC", "HanziPen SC", "Arial Unicode MS", "sans-serif"]
    plt.rcParams['axes.unicode_minus'] = False


def plot_price_trend(
    df: pd.DataFrame,
    column: str = 'Close',
    title: str = '股票价格走势',
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
) -> None:
    """
    绘制价格走势图
    
    参数:
        df: DataFrame, 股票数据
        column: str, 要绘制的列名
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    plt.figure(figsize=figsize)
    plt.plot(df.index, df[column], label=column, linewidth=1.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('价格', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_candlestick(
    df: pd.DataFrame,
    title: str = 'K线图',
    mav: List[int] = [5, 10, 20],
    volume: bool = True,
    save_path: Optional[str] = None
) -> None:
    """
    绘制K线图
    
    参数:
        df: DataFrame, 股票数据（需包含OHLC列）
        title: str, 图表标题
        mav: List[int], 移动平均线周期列表
        volume: bool, 是否显示成交量
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    mc = mpf.make_marketcolors(
        up='r', down='g', edge='i', wick='i', volume='in', inherit=True
    )
    s = mpf.make_mpf_style(
        marketcolors=mc, 
        gridstyle='--', 
        y_on_right=False,
        facecolor='white',
        edgecolor='black'
    )
    
    kwargs = {
        'type': 'candle',
        'style': s,
        'title': title,
        'ylabel': 'Price',
        'ylabel_lower': 'Volume',
        'volume': volume,
        'mav': mav,
        'figscale': 1.2,
        'figsize': (14, 8),
        'warn_too_much_data': len(df) + 1
    }
    
    if save_path:
        kwargs['savefig'] = save_path
        print(f"图表已保存至: {save_path}")
    
    mpf.plot(df, **kwargs)


def plot_technical_indicators(
    df: pd.DataFrame,
    indicators: List[str] = ['SMA_20', 'SMA_50'],
    title: str = '技术指标',
    figsize: tuple = (14, 8),
    save_path: Optional[str] = None
) -> None:
    """
    绘制技术指标
    
    参数:
        df: DataFrame, 股票数据
        indicators: List[str], 要绘制的指标列表
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    fig, axes = plt.subplots(len(indicators), 1, figsize=figsize, squeeze=False)
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    for i, indicator in enumerate(indicators):
        if indicator in df.columns:
            axes[i, 0].plot(df.index, df[indicator], label=indicator, linewidth=1.5)
            axes[i, 0].plot(df.index, df['Close'], label='Close', alpha=0.5, linewidth=1)
            axes[i, 0].set_title(indicator, fontsize=12)
            axes[i, 0].legend()
            axes[i, 0].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_rsi(
    df: pd.DataFrame,
    rsi_column: str = 'RSI_14',
    title: str = 'RSI指标',
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
) -> None:
    """
    绘制RSI指标
    
    参数:
        df: DataFrame, 股票数据
        rsi_column: str, RSI列名
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    plt.figure(figsize=figsize)
    plt.plot(df.index, df[rsi_column], label='RSI', linewidth=1.5, color='purple')
    plt.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='超买线 (70)')
    plt.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='超卖线 (30)')
    plt.axhline(y=50, color='gray', linestyle='-', alpha=0.3)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('RSI值', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_macd(
    df: pd.DataFrame,
    title: str = 'MACD指标',
    figsize: tuple = (12, 8),
    save_path: Optional[str] = None
) -> None:
    """
    绘制MACD指标
    
    参数:
        df: DataFrame, 股票数据（需包含MACD, Signal_Line, Histogram列）
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    ax1.plot(df.index, df['Close'], label='Close', linewidth=1.5, color='blue')
    ax1.set_ylabel('价格', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(df.index, df['MACD'], label='MACD', linewidth=1.5, color='blue')
    ax2.plot(df.index, df['Signal_Line'], label='Signal', linewidth=1.5, color='orange')
    
    colors = ['red' if x >= 0 else 'green' for x in df['MACD_Histogram']]
    ax2.bar(df.index, df['MACD_Histogram'], color=colors, alpha=0.6, label='Histogram')
    
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.set_ylabel('MACD', fontsize=12)
    ax2.set_xlabel('日期', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_bollinger_bands(
    df: pd.DataFrame,
    title: str = '布林带',
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
) -> None:
    """
    绘制布林带
    
    参数:
        df: DataFrame, 股票数据（需包含Close, BB_Upper, BB_Middle, BB_Lower列）
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    plt.figure(figsize=figsize)
    plt.plot(df.index, df['Close'], label='Close', linewidth=1.5, color='blue')
    plt.plot(df.index, df['BB_Upper'], label='Upper Band', linewidth=1, color='red', linestyle='--')
    plt.plot(df.index, df['BB_Middle'], label='Middle Band', linewidth=1, color='orange')
    plt.plot(df.index, df['BB_Lower'], label='Lower Band', linewidth=1, color='green', linestyle='--')
    
    plt.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], alpha=0.1, color='gray')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('价格', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_returns_distribution(
    df: pd.DataFrame,
    column: str = 'Daily_Change_Pct',
    title: str = '收益率分布',
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
) -> None:
    """
    绘制收益率分布图
    
    参数:
        df: DataFrame, 股票数据
        column: str, 收益率列名
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    axes[0].hist(df[column].dropna(), bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_title('收益率直方图', fontsize=12)
    axes[0].set_xlabel('收益率 (%)', fontsize=10)
    axes[0].set_ylabel('频数', fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(df.index, df[column], linewidth=1, alpha=0.7)
    axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1].set_title('收益率时间序列', fontsize=12)
    axes[1].set_xlabel('日期', fontsize=10)
    axes[1].set_ylabel('收益率 (%)', fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_volume(
    df: pd.DataFrame,
    title: str = '成交量',
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
) -> None:
    """
    绘制成交量图
    
    参数:
        df: DataFrame, 股票数据
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    ax1.plot(df.index, df['Close'], label='Close', linewidth=1.5, color='blue')
    ax1.set_ylabel('价格', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    colors = ['red' if df['Close'].iloc[i] >= df['Open'].iloc[i] else 'green' 
              for i in range(len(df))]
    ax2.bar(df.index, df['Volume'], color=colors, alpha=0.6)
    ax2.set_ylabel('成交量', fontsize=12)
    ax2.set_xlabel('日期', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_correlation_heatmap(
    df: pd.DataFrame,
    title: str = '相关性热力图',
    figsize: tuple = (10, 8),
    save_path: Optional[str] = None
) -> None:
    """
    绘制相关性热力图
    
    参数:
        df: DataFrame, 股票数据
        title: str, 图表标题
        figsize: tuple, 图表大小
        save_path: str, 保存路径（可选）
    """
    setup_chinese_font()
    
    plt.figure(figsize=figsize)
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    plt.show()
