"""
创建示例股票数据（模拟数据）
由于Yahoo Finance API限流，使用模拟数据进行演示
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def create_sample_data(ticker='AAPL', years=5):
    """
    创建模拟股票数据
    
    参数:
        ticker: str, 股票代码
        years: int, 数据年数
        
    返回:
        DataFrame: 模拟股票数据
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = dates[dates.dayofweek < 5]  # 只保留工作日
    
    np.random.seed(hash(ticker) % 2**32)
    
    base_price = 100 + np.random.randint(0, 200)
    volatility = 0.02
    
    close_prices = []
    for i in range(len(dates)):
        if i == 0:
            price = base_price
        else:
            change = np.random.normal(0, volatility)
            price = close_prices[-1] * (1 + change)
        close_prices.append(price)
    
    prices = []
    for i, close_price in enumerate(close_prices):
        high = close_price * (1 + abs(np.random.normal(0, 0.01)))
        low = close_price * (1 - abs(np.random.normal(0, 0.01)))
        open_price = low + np.random.random() * (high - low)
        volume = int(np.random.normal(10000000, 2000000))
        
        prices.append({
            'Open': round(open_price, 2),
            'High': round(high, 2),
            'Low': round(low, 2),
            'Close': round(close_price, 2),
            'Adj Close': round(close_price, 2),
            'Volume': max(0, volume)
        })
    
    df = pd.DataFrame(prices, index=dates)
    df.index.name = 'Date'
    
    return df


def main():
    """创建示例数据"""
    
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("=" * 60)
    print("创建示例股票数据")
    print("=" * 60)
    
    os.makedirs('data', exist_ok=True)
    
    for ticker in tickers:
        print(f"\n创建 {ticker} 数据...")
        
        data = create_sample_data(ticker, years=5)
        
        file_path = f'data/{ticker}_stock_data.csv'
        data.to_csv(file_path)
        
        print(f"   ✓ {ticker} 数据创建成功，共 {len(data)} 行")
        print(f"   ✓ 已保存至: {file_path}")
        print(f"   ✓ 日期范围: {data.index[0].strftime('%Y-%m-%d')} 到 {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"   ✓ 价格范围: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
    
    print("\n" + "=" * 60)
    print("示例数据创建完成！")
    print("=" * 60)
    print("\n下一步:")
    print("  1. 运行 'uv run python example.py' 查看示例")
    print("  2. 运行 'jupyter lab' 启动交互式环境")


if __name__ == "__main__":
    main()
