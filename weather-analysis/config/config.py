import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WeatherConfig:
    """完全可配置的天气分析配置类"""
    
    def __init__(self):
        # 城市配置 - 优先从环境变量读取，环境变量不存在时使用默认值（桂林）
        self.CITY = os.getenv('WEATHER_CITY', 'Guilin')
        self.COUNTRY = os.getenv('WEATHER_COUNTRY', 'CN')
        self.LAT = float(os.getenv('WEATHER_LAT', '25.2741'))  # 桂林纬度
        self.LON = float(os.getenv('WEATHER_LON', '110.2993'))  # 桂林经度
        
        # 核心API配置
        self.API_KEY = os.getenv('OPENWEATHER_API_KEY')
        
        # 分析配置
        self.USE_CACHE = os.getenv('USE_CACHE', 'true').lower() == 'true'
        self.CACHE_HOURS = int(os.getenv('CACHE_HOURS', '1'))
        self.FORECAST_DAYS = int(os.getenv('FORECAST_DAYS', '5'))
        
        # 可视化配置
        self.TIMEZONE = os.getenv('TIMEZONE', 'Asia/Shanghai')
        self.LANGUAGE = os.getenv('LANGUAGE', 'zh_cn')
        
        # 城市显示名称（支持中英文）
        self.CITY_DISPLAY_NAME = os.getenv('CITY_DISPLAY_NAME', '桂林')
        
        # 天气状态映射
        self._load_weather_mappings()
    
    def _load_weather_mappings(self):
        """加载天气状态映射配置"""
        self.WEATHER_MAP = {
            'Clear': '晴朗',
            'Clouds': '多云',
            'Rain': '降雨',
            'Snow': '降雪',
            'Thunderstorm': '雷暴',
            'Drizzle': '毛毛雨',
            'Mist': '薄雾',
            'Fog': '雾',
            'Haze': '霾',
            'Dust': '沙尘',
            'Smoke': '烟雾',
            'Ash': '火山灰',
            'Squall': '飑',
            'Tornado': '龙卷风'
        }
    
    def validate(self) -> bool:
        """验证配置有效性"""
        errors = []
        
        if not self.API_KEY:
            errors.append("❌ OPENWEATHER_API_KEY 未设置")
        elif len(self.API_KEY) != 32:
            errors.append("⚠️  API密钥长度可能不正确")
        
        if not self.CITY:
            errors.append("❌ WEATHER_CITY 未设置")
        
        try:
            float(self.LAT)
            float(self.LON)
        except ValueError:
            errors.append("❌ WEATHER_LAT 或 WEATHER_LON 不是有效的浮点数")
        
        if errors:
            print("\n".join(errors))
            return False
        
        return True
    
    def get_city_info(self) -> dict:
        """获取城市信息字典"""
        return {
            'name': self.CITY,
            'country': self.COUNTRY,
            'display_name': self.CITY_DISPLAY_NAME,
            'coordinates': {
                'lat': self.LAT,
                'lon': self.LON
            }
        }
    
    def __str__(self):
        """友好的配置信息显示"""
        return f"""
🌍 天气分析配置
────────────────
📍 目标城市: {self.CITY_DISPLAY_NAME} ({self.CITY}, {self.COUNTRY})
📌 坐标: 纬度 {self.LAT}, 经度 {self.LON}
🔑 API状态: {'✅ 已配置' if self.API_KEY else '❌ 未配置'}
⚙️  缓存: {'启用' if self.USE_CACHE else '禁用'} ({self.CACHE_HOURS}小时)
📅 预报天数: {self.FORECAST_DAYS}天
🌐 语言: {self.LANGUAGE}
        """.strip()

# 全局配置实例
config = WeatherConfig()