"""
开发者配置文件
"""

class Config:
    """开发者配置类"""

    # 窗口标题
    WINDOW_TITLE = "菜菜捞捞"
    
    # 窗口尺寸
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    
    # ====================================================
    
    @classmethod
    def get_window_size(cls):
        """获取窗口尺寸"""
        return f"{cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}"