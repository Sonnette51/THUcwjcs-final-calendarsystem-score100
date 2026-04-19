"""
主窗口模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
from storage.event_storage import EventStorage
from config import Config
from ui.menu_view import MenuView
from ui.calendar_view import CalendarView
from ui.date_query_view import DateQueryView
from ui.event_manage_view import EventManageView

class MainWindow:
    """主窗口控制器"""
    
    def __init__(self):
        """初始化主窗口"""
        self.root = tk.Tk()
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.get_window_size())
        
        # 居中显示
        self.center_window()
        
        # 初始化存储
        self.storage = EventStorage()
        self.events = self.storage.load_events()
        
        # 选中的日期
        from datetime import date
        today = date.today()
        self.selected_date = (today.year, today.month, today.day)
        
        # 设置样式
        self.setup_styles()
        
        # 创建主容器
        self.container = ttk.Frame(self.root)
        self.container.pack(fill='both', expand=True)
        
        # 创建视图字典
        self.views = {}
        self.current_view = None
        
        # 初始化所有视图
        self.init_views()
        
        # 显示主菜单
        self.show_view('menu')
        
        # 关闭窗口
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 大按钮
        style.configure(
            'Large.TButton',
            font=('Times New Roman', 18),
            padding=20
        )
        
        # 退出按钮
        style.configure(
            'Exit.TButton',
            font=('Times New Roman', 15),
            padding=15
        )
        
        # 标签
        style.configure(
            'TLabel',
            font=('Times New Roman', 11)
        )
    
    def init_views(self):
        """初始化所有视图"""
        self.views['menu'] = MenuView(self.container, self)
        self.views['calendar'] = CalendarView(self.container, self)
        self.views['date_query'] = DateQueryView(self.container, self)
        self.views['event_manage'] = EventManageView(self.container, self)
        
        # 将所有视图放置在同一位置
        for view in self.views.values():
            view.place(x=0, y=0, relwidth=1, relheight=1)
    
    def show_view(self, view_name):
        """显示指定视图"""
        if view_name in self.views:
            # 隐藏当前视图
            if self.current_view:
                self.current_view.lower()
            
            # 显示新视图
            self.current_view = self.views[view_name]
            self.current_view.lift()
            
            # 如果视图实现了 show() 方法，调用它
            if hasattr(self.current_view, 'show'):
                try:
                    self.current_view.show()
                except Exception as e:
                    print(f"视图显示错误: {e}")
    
    def quit_app(self):
        """退出应用"""
        # 保存事件数据
        self.storage.save_events(self.events)
        self.root.quit()
        self.root.destroy()

    def apply_events_change(self, new_events):
        """
        统一应用事件变更：更新内存、保存到文件、各视图刷新
        """
        # 更新内存中的事件列表
        self.events = new_events
        
        # 保存
        try:
            self.storage.save_events(self.events)
        except Exception as e:
            print(f"保存事件失败: {e}")
            messagebox.showwarning("警告", "事件保存失败")
        
        #刷新所有视图
        self.refresh_all_views()
    
    def refresh_all_views(self):
        """刷新所有视图"""
        # 刷新事件管理视图
        if 'event_manage' in self.views:
            try:
                self.views['event_manage'].refresh_event_list()
            except Exception as e:
                print(f"刷新事件管理视图失败: {e}")
        
        # 刷新日历视图
        if 'calendar' in self.views:
            try:
                self.views['calendar'].update_calendar()
            except Exception as e:
                print(f"刷新日历视图失败: {e}")
        
        # 刷新日期查询视图（
        if 'date_query' in self.views and hasattr(self, 'selected_date'):
            try:
                if self.current_view == self.views['date_query']:
                    self.views['date_query'].query_date()
            except Exception as e:
                print(f"刷新日期查询视图失败: {e}")
    
    def run(self):
        """运行主循环"""
        self.root.mainloop()