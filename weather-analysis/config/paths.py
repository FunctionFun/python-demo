import os
from pathlib import Path


class PathManager:
    """路径管理类，用于动态管理项目中的所有路径"""
    
    def __init__(self):
        # 获取项目根目录（基于当前文件的位置）
        self.ROOT_DIR = Path(__file__).parent.parent.absolute()
        
        # 核心目录路径
        self.CONFIG_DIR = self.ROOT_DIR / "config"
        self.SRC_DIR = self.ROOT_DIR / "src"
        self.NOTEBOOKS_DIR = self.ROOT_DIR / "notebooks"
        
        # 数据文件路径
        self.CITIES_PRESET_FILE = self.ROOT_DIR / "cities_preset.json"
        
        # 环境变量配置
        self.ENV_FILE = self.ROOT_DIR / ".env"
        self.ENV_EXAMPLE_FILE = self.ROOT_DIR / ".env.example"
    
    def get_path(self, relative_path: str) -> Path:
        """获取相对于项目根目录的路径"""
        return self.ROOT_DIR / relative_path
    
    def exists(self, path: Path) -> bool:
        """检查路径是否存在"""
        return path.exists()
    
    def __str__(self):
        """友好的路径信息显示"""
        return f"""
路径配置
────────
根目录: {self.ROOT_DIR}
配置目录: {self.CONFIG_DIR}
源码目录: {self.SRC_DIR}
笔记本目录: {self.NOTEBOOKS_DIR}
城市预设文件: {self.CITIES_PRESET_FILE}
        """.strip()


# 全局路径管理实例
paths = PathManager()