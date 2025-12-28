import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib

# 添加项目根目录到Python路径以便正确导入
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config import config

class UniversalWeatherFetcher:
    """通用天气数据获取器 - 支持任意城市"""
    
    def __init__(self):
        self.api_key = config.API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WeatherAnalysisApp/1.0'
        })
        
        # 缓存目录 - 使用绝对路径
        self.cache_dir = project_root / 'data/raw'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, city: str, endpoint: str) -> str:
        """生成缓存键"""
        date_str = datetime.now().strftime('%Y%m%d')
        key_string = f"{city}_{endpoint}_{date_str}"
        return hashlib.md5(key_string.encode()).hexdigest()[:8]
    
    def _load_from_cache(self, cache_key: str, endpoint: str) -> Optional[Dict]:
        """从缓存加载数据"""
        if not config.USE_CACHE:
            return None
            
        cache_file = self.cache_dir / f"{cache_key}_{endpoint}.json"
        
        if cache_file.exists():
            file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            if file_age < timedelta(hours=config.CACHE_HOURS):
                print(f"📂 使用缓存数据 ({cache_key})")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return None
    
    def _save_to_cache(self, cache_key: str, endpoint: str, data: Dict):
        """保存数据到缓存"""
        cache_file = self.cache_dir / f"{cache_key}_{endpoint}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_current_weather(self, city: str = None, country: str = None) -> Optional[Dict]:
        """获取任意城市的当前天气"""
        
        # 使用配置中的城市或传入的城市
        target_city = city or config.CITY
        target_country = country or config.COUNTRY
        
        cache_key = self._get_cache_key(target_city, 'current')
        
        # 尝试从缓存加载
        cached_data = self._load_from_cache(cache_key, 'current')
        if cached_data:
            return cached_data
        
        # 构建API请求参数
        params = {
            'q': f'{target_city},{target_country}',
            'appid': self.api_key,
            'units': 'metric',
            'lang': config.LANGUAGE
        }
        
        try:
            print(f"🌤️  正在获取 {target_city} 的实时天气...")
            response = self.session.get(
                f"{self.base_url}/weather",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # 保存到缓存
                self._save_to_cache(cache_key, 'current', data)
                print(f"✅ {target_city} 数据获取成功！")
                return data
            elif response.status_code == 404:
                print(f"❌ 未找到城市: {target_city}, {target_country}")
                return None
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 网络错误: {e}")
            return None
    
    def get_forecast(self, city: str = None, country: str = None, days: int = None) -> Optional[Dict]:
        """获取任意城市的天气预报"""
        
        target_city = city or config.CITY
        target_country = country or config.COUNTRY
        target_days = days or config.FORECAST_DAYS
        
        cache_key = self._get_cache_key(f"{target_city}_forecast", 'forecast')
        
        # 尝试从缓存加载
        cached_data = self._load_from_cache(cache_key, 'forecast')
        if cached_data:
            return cached_data
        
        params = {
            'q': f'{target_city},{target_country}',
            'appid': self.api_key,
            'units': 'metric',
            'lang': config.LANGUAGE,
            'cnt': target_days * 8  # 每3小时一个数据点
        }
        
        try:
            print(f"📅 正在获取 {target_city} 的{target_days}天天气预报...")
            response = self.session.get(
                f"{self.base_url}/forecast",
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                self._save_to_cache(cache_key, 'forecast', data)
                return data
            else:
                print(f"❌ 预报请求失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 网络错误: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat: float = None, lon: float = None) -> Optional[Dict]:
        """通过坐标获取天气（当城市名不明确时）"""
        target_lat = lat or config.LAT
        target_lon = lon or config.LON
        
        params = {
            'lat': target_lat,
            'lon': target_lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': config.LANGUAGE
        }
        
        try:
            print(f"📍 正在通过坐标获取天气 ({target_lat}, {target_lon})...")
            response = self.session.get(
                f"{self.base_url}/weather",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 坐标请求失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 网络错误: {e}")
            return None
    
    @staticmethod
    def parse_weather_data(data: Dict, city_display_name: str = None) -> Optional[Dict]:
        """通用天气数据解析方法"""
        if not data:
            return None
        
        # 获取城市显示名称
        display_name = city_display_name or data.get('name', '未知城市')
        
        # 天气描述转换
        weather_en = data['weather'][0]['main']
        weather_zh = config.WEATHER_MAP.get(weather_en, weather_en)
        
        parsed = {
            '城市': display_name,
            '实际城市名': data.get('name', '未知'),
            '国家': data['sys']['country'],
            '更新时间': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            '天气状况': weather_zh,
            '详细描述': data['weather'][0]['description'],
            '当前温度(℃)': round(data['main']['temp'], 1),
            '体感温度(℃)': round(data['main']['feels_like'], 1),
            '最高温度(℃)': round(data['main']['temp_max'], 1),
            '最低温度(℃)': round(data['main']['temp_min'], 1),
            '湿度(%)': data['main']['humidity'],
            '气压(hPa)': data['main']['pressure'],
            '风速(m/s)': data['wind']['speed'],
            '风向(°)': data['wind'].get('deg', '无数据'),
            '云量(%)': data['clouds']['all'],
            '能见度(m)': data.get('visibility', '无数据'),
            '日出时间': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
            '日落时间': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
            '时区偏移': data['timezone'],
            '数据来源': 'OpenWeatherMap'
        }
        
        # 添加舒适度计算
        parsed['舒适度评级'] = UniversalWeatherFetcher.calculate_comfort_index(
            parsed['当前温度(℃)'], 
            parsed['湿度(%)'],
            parsed['风速(m/s)']
        )
        
        return parsed
    
    @staticmethod
    def calculate_comfort_index(temp: float, humidity: float, wind_speed: float) -> str:
        """计算天气舒适度指数"""
        # 温度舒适度
        if temp < 0:
            temp_score = "严寒"
        elif temp < 10:
            temp_score = "寒冷"
        elif temp < 18:
            temp_score = "凉爽"
        elif temp < 26:
            temp_score = "舒适"
        elif temp < 32:
            temp_score = "温暖"
        else:
            temp_score = "炎热"
        
        # 湿度调整
        if humidity > 85:
            humidity_adj = "潮湿"
        elif humidity < 30:
            humidity_adj = "干燥"
        else:
            humidity_adj = "适中"
        
        # 风速调整
        if wind_speed > 10:
            wind_adj = "大风"
        elif wind_speed > 5:
            wind_adj = "有风"
        else:
            wind_adj = "微风"
        
        # 综合评级
        if temp_score == "舒适" and humidity_adj == "适中":
            return "非常舒适"
        elif temp_score in ["温暖", "凉爽"] and humidity_adj != "潮湿":
            return "较为舒适"
        else:
            return f"{temp_score}{humidity_adj}"
    
    def compare_cities(self, cities: List[Dict]) -> pd.DataFrame:
        """比较多个城市的天气"""
        comparisons = []
        
        for city_info in cities:
            city = city_info.get('city')
            country = city_info.get('country', 'CN')
            display_name = city_info.get('display_name', city)
            
            print(f"正在获取 {city} 的数据...")
            data = self.get_current_weather(city, country)
            
            if data:
                parsed = self.parse_weather_data(data, display_name)
                if parsed:
                    # 提取关键指标
                    comparisons.append({
                        '城市': parsed['城市'],
                        '温度(℃)': parsed['当前温度(℃)'],
                        '体感温度(℃)': parsed['体感温度(℃)'],
                        '天气状况': parsed['天气状况'],
                        '湿度(%)': parsed['湿度(%)'],
                        '风速(m/s)': parsed['风速(m/s)'],
                        '舒适度': parsed['舒适度评级']
                    })
            
            # 避免API速率限制
            import time
            time.sleep(1.1)
        
        return pd.DataFrame(comparisons)