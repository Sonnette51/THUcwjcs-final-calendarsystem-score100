"""
主菜单视图模块
"""
import tkinter as tk
from tkinter import ttk

class MenuView(ttk.Frame):
    """主菜单视图"""
    
    def __init__(self, parent, controller):
        """
        初始化主菜单视图
        parent: 父窗口
        controller: 主控制器
        """
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 标题
        title_label = ttk.Label(
            self,
            text="日历管不好系统",
            font=('Times New Roman', 24, 'bold')
        )
        title_label.pack(pady=40)
        
        # 按钮容器
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # 月历打印按钮
        btn_calendar = ttk.Button(
            button_frame,
            text="嘟嘟可月历打印服务 Calendar printing",
            command=lambda: self.controller.show_view('calendar'),
            style='Large.TButton'
        )
        btn_calendar.pack(pady=15, fill='x')
        
        # 日期查询按钮
        btn_date_query = ttk.Button(
            button_frame,
            text="嘟嘟可日期查询服务 Date query",
            command=lambda: self.controller.show_view('date_query'),
            style='Large.TButton'
        )
        btn_date_query.pack(pady=15, fill='x')
        
        # 事件管理按钮
        btn_event_manage = ttk.Button(
            button_frame,
            text="嘟嘟可事件管理服务 Event management",
            command=lambda: self.controller.show_view('event_manage'),
            style='Large.TButton'
        )
        btn_event_manage.pack(pady=15, fill='x')
        
        # 退出按钮
        btn_exit = ttk.Button(
            button_frame,
            text="乘坐蹦蹦炸弹离开 Exit",
            command=self.controller.quit_app,
            style='Exit.TButton'
        )
        btn_exit.pack(pady=15, fill='x')
        
        # 版本信息
        version_label = ttk.Label(
            self,
            text="Version 8.0 | bug全都可以炸完！",
            font=('Times New Roman', 12)
        )
        version_label.pack(side='bottom', pady=10)