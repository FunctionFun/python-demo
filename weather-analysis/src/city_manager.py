"""
城市管理工具 - 方便地管理和切换目标城市
"""
import json
import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到Python路径以便正确导入
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config import config

class CityManager:
    """城市配置管理器"""
    
    def __init__(self, preset_file='cities_preset.json'):
        self.preset_file = Path(preset_file)
        self.presets = self._load_presets()
    
    def _load_presets(self) -> Dict:
        """加载城市预设，没有则创建默认预设"""
        try:
            if self.preset_file.exists():
                with open(self.preset_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # 如果文件不存在，创建默认城市预设
            default_presets = {
                'cities': {
                    'beijing': {
                        'name': 'Beijing',
                        'country': 'CN',
                        'lat': 39.9042,
                        'lon': 116.4074,
                        'display_name': '北京'
                    },
                    'shanghai': {
                        'name': 'Shanghai',
                        'country': 'CN',
                        'lat': 31.2304,
                        'lon': 121.4737,
                        'display_name': '上海'
                    },
                    'guangzhou': {
                        'name': 'Guangzhou',
                        'country': 'CN',
                        'lat': 23.1291,
                        'lon': 113.2644,
                        'display_name': '广州'
                    },
                    'shenzhen': {
                        'name': 'Shenzhen',
                        'country': 'CN',
                        'lat': 22.5431,
                        'lon': 114.0579,
                        'display_name': '深圳'
                    },
                    'chengdu': {
                        'name': 'Chengdu',
                        'country': 'CN',
                        'lat': 30.5728,
                        'lon': 104.0668,
                        'display_name': '成都'
                    },
                    'guilin': {
                        'name': 'Guilin',
                        'country': 'CN',
                        'lat': 25.2741,
                        'lon': 110.2993,
                        'display_name': '桂林'
                    }
                }
            }
            
            # 保存默认预设到文件
            with open(self.preset_file, 'w', encoding='utf-8') as f:
                json.dump(default_presets, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 已创建默认城市预设文件: {self.preset_file}")
            return default_presets
        except Exception as e:
            print(f"❌ 加载城市预设失败: {e}")
            return {'cities': {}}
    
    def list_cities(self) -> List[Dict]:
        """列出所有预设城市"""
        cities = []
        for city_id, city_info in self.presets.get('cities', {}).items():
            cities.append({
                'id': city_id,
                **city_info
            })
        return cities
    
    def switch_city(self, city_id: str):
        """切换到指定城市"""
        city_info = self.presets.get('cities', {}).get(city_id)
        
        if not city_info:
            print(f"❌ 未找到城市预设: {city_id}")
            return False
        
        # 更新内存配置
        config.CITY = city_info.get('name', city_id)
        config.COUNTRY = city_info.get('country', 'CN')
        config.LAT = city_info.get('lat', 0)
        config.LON = city_info.get('lon', 0)
        config.CITY_DISPLAY_NAME = city_info.get('display_name', city_id)
        
        # 持久化到 config.py 文件
        if self._save_config():
            print(f"✅ 已切换到: {config.CITY_DISPLAY_NAME}")
            print(f"   英文名: {config.CITY}, 国家: {config.COUNTRY}")
            print(f"   坐标: ({config.LAT}, {config.LON})")
            return True
        else:
            print("❌ 城市切换失败: 无法保存配置文件")
            return False
    
    def _save_config(self) -> bool:
        """保存配置到 config.py 文件"""
        try:
            config_file_path = Path(__file__).parent.parent / "config" / "config.py"
            config_content = f'''
"""天气分析应用配置"""

class config:
    """配置类"""
    # API配置
    API_KEY = "your_api_key_here"  # 请替换为您的OpenWeatherMap API密钥
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # 默认城市配置
    CITY = "{config.CITY}"
    COUNTRY = "{config.COUNTRY}"
    LAT = {config.LAT}
    LON = {config.LON}
    CITY_DISPLAY_NAME = "{config.CITY_DISPLAY_NAME}"
    
    # 应用配置
    LANGUAGE = "zh_cn"
    FORECAST_DAYS = 5
    USE_CACHE = True
    CACHE_HOURS = 1
    
    # 天气状况映射
    WEATHER_MAP = {{
        "Clear": "晴朗",
        "Clouds": "多云",
        "Rain": "降雨",
        "Drizzle": "小雨",
        "Thunderstorm": "雷雨",
        "Snow": "降雪",
        "Mist": "薄雾",
        "Fog": "雾",
        "Haze": "霾",
        "Smoke": "烟雾"
    }}
'''
            with open(config_file_path, 'w', encoding='utf-8') as f:
                f.write(config_content.strip())
            return True
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            return False
    
    def add_city(self, city_id: str, city_info: Dict):
        """添加新城市预设"""
        try:
            if 'cities' not in self.presets:
                self.presets['cities'] = {}
            
            self.presets['cities'][city_id] = city_info
            
            # 保存到文件
            with open(self.preset_file, 'w', encoding='utf-8') as f:
                json.dump(self.presets, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 已添加城市预设: {city_id}")
            return True
        except Exception as e:
            print(f"❌ 添加城市预设失败: {e}")
            return False

# 命令行接口
if __name__ == '__main__':
    import sys
    
    manager = CityManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            cities = manager.list_cities()
            print(f"\n📋 可用城市 ({len(cities)}个):")
            print("-" * 50)
            for city in cities:
                print(f"  {city['id']:10} -> {city['display_name']}")
        
        elif command == 'switch' and len(sys.argv) > 2:
            city_id = sys.argv[2]
            manager.switch_city(city_id)
        
        elif command == 'current':
            print(f"\n📍 当前配置城市:")
            print(f"   显示名: {config.CITY_DISPLAY_NAME}")
            print(f"   英文名: {config.CITY}")
            print(f"   国家: {config.COUNTRY}")
            print(f"   坐标: ({config.LAT}, {config.LON})")
        
        else:
            print("可用命令:")
            print("  python -m src.city_manager list     # 列出所有城市")
            print("  python -m src.city_manager switch <city_id>  # 切换城市")
            print("  python -m src.city_manager current  # 显示当前城市")
    else:
        print("请指定命令。使用 'list' 查看可用城市。")