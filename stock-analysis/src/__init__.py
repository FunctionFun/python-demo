from .data_loader import (
    download_stock_data,
    load_stock_data,
    download_multiple_stocks,
    load_multiple_stocks,
    save_stock_data,
    get_stock_info,
    validate_data,
    clean_data
)

from .indicators import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_technical_indicators,
    calculate_returns,
    calculate_cumulative_returns,
    calculate_volatility
)

from .visualization import (
    setup_chinese_font,
    plot_price_trend,
    plot_candlestick,
    plot_technical_indicators,
    plot_rsi,
    plot_macd,
    plot_bollinger_bands,
    plot_returns_distribution,
    plot_volume,
    plot_correlation_heatmap
)

from .multi_stock_analysis import (
    create_price_dataframe,
    normalize_prices,
    plot_multi_stock_prices,
    calculate_returns_correlation,
    plot_correlation_heatmap as plot_multi_correlation_heatmap,
    calculate_stock_metrics,
    plot_returns_comparison,
    plot_risk_return_scatter,
    compare_performance,
    find_best_performer,
    find_worst_performer
)

from .report_generator import (
    generate_html_report,
    generate_pdf_report,
    save_html_report,
    generate_multi_stock_report,
    create_summary_report
)

__all__ = [
    'download_stock_data',
    'load_stock_data',
    'download_multiple_stocks',
    'load_multiple_stocks',
    'save_stock_data',
    'get_stock_info',
    'validate_data',
    'clean_data',
    'calculate_sma',
    'calculate_ema',
    'calculate_rsi',
    'calculate_macd',
    'calculate_bollinger_bands',
    'calculate_technical_indicators',
    'calculate_returns',
    'calculate_cumulative_returns',
    'calculate_volatility',
    'setup_chinese_font',
    'plot_price_trend',
    'plot_candlestick',
    'plot_technical_indicators',
    'plot_rsi',
    'plot_macd',
    'plot_bollinger_bands',
    'plot_returns_distribution',
    'plot_volume',
    'plot_correlation_heatmap',
    'create_price_dataframe',
    'normalize_prices',
    'plot_multi_stock_prices',
    'calculate_returns_correlation',
    'calculate_stock_metrics',
    'plot_returns_comparison',
    'plot_risk_return_scatter',
    'compare_performance',
    'find_best_performer',
    'find_worst_performer',
    'generate_html_report',
    'generate_pdf_report',
    'save_html_report',
    'generate_multi_stock_report',
    'create_summary_report'
]
