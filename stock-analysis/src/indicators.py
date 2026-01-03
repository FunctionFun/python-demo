import pandas as pd
import numpy as np


def calculate_sma(df, column='Close', window=20):
    """
    计算简单移动平均线 (Simple Moving Average)
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        window: int, 移动窗口大小
        
    返回:
        Series: SMA值
    """
    return df[column].rolling(window=window).mean()


def calculate_ema(df, column='Close', span=12):
    """
    计算指数移动平均线 (Exponential Moving Average)
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        span: int, 跨度
        
    返回:
        Series: EMA值
    """
    return df[column].ewm(span=span, adjust=False).mean()


def calculate_rsi(df, column='Close', window=14):
    """
    计算相对强弱指数 (Relative Strength Index)
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        window: int, RSI周期
        
    返回:
        Series: RSI值 (0-100)
    """
    delta = df[column].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    avg_gain = avg_gain.fillna(0)
    avg_loss = avg_loss.fillna(0)
    
    for i in range(window, len(gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (window - 1) + gain.iloc[i]) / window
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (window - 1) + loss.iloc[i]) / window
    
    rs = avg_gain / avg_loss.replace(0, 0.001)
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(df, column='Close', fast=12, slow=26, signal=9):
    """
    计算MACD指标 (Moving Average Convergence Divergence)
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        fast: int, 快速EMA周期
        slow: int, 慢速EMA周期
        signal: int, 信号线EMA周期
        
    返回:
        DataFrame: 包含MACD, Signal_Line, Histogram列
    """
    exp_fast = df[column].ewm(span=fast, adjust=False).mean()
    exp_slow = df[column].ewm(span=slow, adjust=False).mean()
    
    macd_line = exp_fast - exp_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return pd.DataFrame({
        'MACD': macd_line,
        'Signal_Line': signal_line,
        'Histogram': histogram
    }, index=df.index)


def calculate_bollinger_bands(df, column='Close', window=20, num_std=2):
    """
    计算布林带 (Bollinger Bands)
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        window: int, 移动窗口大小
        num_std: int, 标准差倍数
        
    返回:
        DataFrame: 包含Middle, Upper, Lower列
    """
    sma = df[column].rolling(window=window).mean()
    std = df[column].rolling(window=window).std()
    
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return pd.DataFrame({
        'Middle': sma,
        'Upper': upper_band,
        'Lower': lower_band
    }, index=df.index)


def calculate_technical_indicators(df):
    """
    计算所有技术指标
    
    参数:
        df: DataFrame, 包含股票数据（至少包含Close列）
        
    返回:
        DataFrame: 包含原始数据和技术指标的DataFrame
    """
    data = df.copy()
    
    if 'Close' not in data.columns:
        raise ValueError("DataFrame must contain 'Close' column")
    
    data['SMA_20'] = calculate_sma(data, 'Close', 20)
    data['SMA_50'] = calculate_sma(data, 'Close', 50)
    
    data['RSI_14'] = calculate_rsi(data, 'Close', 14)
    
    macd_df = calculate_macd(data, 'Close')
    data['MACD'] = macd_df['MACD']
    data['Signal_Line'] = macd_df['Signal_Line']
    data['MACD_Histogram'] = macd_df['Histogram']
    
    bb_df = calculate_bollinger_bands(data, 'Close')
    data['BB_Middle'] = bb_df['Middle']
    data['BB_Upper'] = bb_df['Upper']
    data['BB_Lower'] = bb_df['Lower']
    
    data['Daily_Change_Pct'] = data['Close'].pct_change() * 100
    data['Volume_SMA_20'] = data['Volume'].rolling(window=20).mean() if 'Volume' in data.columns else None
    
    return data


def calculate_returns(df, column='Close'):
    """
    计算收益率
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        
    返回:
        Series: 日收益率
    """
    return df[column].pct_change()


def calculate_cumulative_returns(df, column='Close'):
    """
    计算累计收益率
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        
    返回:
        Series: 累计收益率
    """
    returns = calculate_returns(df, column)
    return (1 + returns).cumprod() - 1


def calculate_volatility(df, column='Close', window=20):
    """
    计算波动率（标准差）
    
    参数:
        df: DataFrame, 包含股票数据
        column: str, 计算的列名
        window: int, 移动窗口大小
        
    返回:
        Series: 波动率
    """
    returns = calculate_returns(df, column)
    return returns.rolling(window=window).std() * np.sqrt(252)
