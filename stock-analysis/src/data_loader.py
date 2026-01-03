import yfinance as yf
import pandas as pd
import os
from typing import Optional, List
from datetime import datetime, timedelta


def download_stock_data(
    ticker: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = '5y'
) -> pd.DataFrame:
    """
    从Yahoo Finance下载股票数据
    
    参数:
        ticker: str, 股票代码（如 'AAPL'）
        start_date: str, 开始日期（格式：'YYYY-MM-DD'），可选
        end_date: str, 结束日期（格式：'YYYY-MM-DD'），可选
        period: str, 数据周期（如 '1y', '5y', 'max'），默认 '5y'
        
    返回:
        DataFrame: 股票数据
    """
    if start_date and end_date:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    else:
        data = yf.download(ticker, period=period, progress=False)
    
    return data


def load_stock_data(
    file_path: str,
    ticker: str = 'AAPL',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = '5y',
    force_download: bool = False
) -> pd.DataFrame:
    """
    加载股票数据，如果文件不存在则自动下载
    
    参数:
        file_path: str, CSV文件路径
        ticker: str, 股票代码
        start_date: str, 开始日期（格式：'YYYY-MM-DD'），可选
        end_date: str, 结束日期（格式：'YYYY-MM-DD'），可选
        period: str, 数据周期（如 '1y', '5y', 'max'），默认 '5y'
        force_download: bool, 是否强制重新下载
        
    返回:
        DataFrame: 股票数据
    """
    if not os.path.exists(file_path) or force_download:
        print(f"正在下载 {ticker} 数据...")
        try:
            data = download_stock_data(ticker, start_date, end_date, period)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            data.to_csv(file_path)
            print(f"数据已保存至: {file_path}")
        except Exception as e:
            print(f"下载 {ticker} 数据时出错: {e}")
            if os.path.exists(file_path):
                print(f"尝试从本地文件加载数据: {file_path}")
                data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            else:
                raise
    else:
        print(f"从本地文件加载数据: {file_path}")
        try:
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
        except Exception as e:
            print(f"读取CSV文件时出错: {e}")
            try:
                data = pd.read_csv(file_path, parse_dates=True)
                if 'Date' in data.columns:
                    data.set_index('Date', inplace=True)
            except Exception as e2:
                print(f"尝试读取CSV文件失败: {e2}")
                raise
    
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    
    if 'Close' not in data.columns and 'Adj Close' in data.columns:
        data['Close'] = data['Adj Close']
    
    return data


def download_multiple_stocks(
    tickers: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = '5y'
) -> dict:
    """
    下载多只股票数据
    
    参数:
        tickers: List[str], 股票代码列表
        start_date: str, 开始日期（格式：'YYYY-MM-DD'），可选
        end_date: str, 结束日期（格式：'YYYY-MM-DD'），可选
        period: str, 数据周期（如 '1y', '5y', 'max'），默认 '5y'
        
    返回:
        dict: 键为股票代码，值为对应的DataFrame
    """
    stock_data = {}
    
    for ticker in tickers:
        print(f"正在下载 {ticker} 数据...")
        try:
            data = download_stock_data(ticker, start_date, end_date, period)
            stock_data[ticker] = data
            print(f"{ticker} 数据下载完成")
        except Exception as e:
            print(f"下载 {ticker} 数据时出错: {e}")
    
    return stock_data


def load_multiple_stocks(
    tickers: List[str],
    data_dir: str = 'data',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = '5y',
    force_download: bool = False
) -> dict:
    """
    加载多只股票数据，文件不存在则自动下载
    
    参数:
        tickers: List[str], 股票代码列表
        data_dir: str, 数据目录
        start_date: str, 开始日期（格式：'YYYY-MM-DD'），可选
        end_date: str, 结束日期（格式：'YYYY-MM-DD'），可选
        period: str, 数据周期（如 '1y', '5y', 'max'），默认 '5y'
        force_download: bool, 是否强制重新下载
        
    返回:
        dict: 键为股票代码，值为对应的DataFrame
    """
    stock_data = {}
    
    for ticker in tickers:
        file_path = os.path.join(data_dir, f"{ticker}_stock_data.csv")
        try:
            data = load_stock_data(file_path, ticker, start_date, end_date, period, force_download)
            stock_data[ticker] = data
        except Exception as e:
            print(f"加载 {ticker} 数据时出错: {e}")
    
    return stock_data


def save_stock_data(data: pd.DataFrame, file_path: str) -> None:
    """
    保存股票数据到CSV文件
    
    参数:
        data: DataFrame, 股票数据
        file_path: str, CSV文件路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data.to_csv(file_path)
    print(f"数据已保存至: {file_path}")


def get_stock_info(ticker: str) -> dict:
    """
    获取股票基本信息
    
    参数:
        ticker: str, 股票代码
        
    返回:
        dict: 股票基本信息
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    
    key_info = {
        'ticker': ticker,
        'name': info.get('longName', 'N/A'),
        'sector': info.get('sector', 'N/A'),
        'industry': info.get('industry', 'N/A'),
        'market_cap': info.get('marketCap', 'N/A'),
        'current_price': info.get('currentPrice', 'N/A'),
        'previous_close': info.get('previousClose', 'N/A'),
        '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
        '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
    }
    
    return key_info


def validate_data(data: pd.DataFrame) -> bool:
    """
    验证股票数据的完整性
    
    参数:
        data: DataFrame, 股票数据
        
    返回:
        bool: 数据是否有效
    """
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    for col in required_columns:
        if col not in data.columns:
            print(f"缺少必需列: {col}")
            return False
    
    if data.isnull().sum().sum() > 0:
        print(f"发现缺失值: {data.isnull().sum().sum()} 个")
        return False
    
    if len(data) == 0:
        print("数据为空")
        return False
    
    return True


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    清理股票数据
    
    参数:
        data: DataFrame, 原始股票数据
        
    返回:
        DataFrame: 清理后的数据
    """
    cleaned_data = data.copy()
    
    if cleaned_data.isnull().sum().sum() > 0:
        print("处理缺失值...")
        cleaned_data = cleaned_data.ffill()
        cleaned_data = cleaned_data.bfill()
    
    cleaned_data = cleaned_data.dropna()
    
    return cleaned_data
