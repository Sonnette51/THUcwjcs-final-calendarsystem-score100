"""
日历管不好系统
主程序入口

作者: 楼诗雨2025013092
收工日期: 2025.12.25
版本: 8.0

"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

def main():
    """主函数"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"程序运行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()