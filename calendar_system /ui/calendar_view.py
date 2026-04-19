"""
月历打印视图
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.date_utils import get_month_calendar, parse_and_validate_date

class CalendarView(ttk.Frame):
    """月历打印视图"""
    
    def __init__(self, parent, controller):
        """初始化月历打印视图"""
        super().__init__(parent)
        self.controller = controller
        from datetime import date
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 顶部工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=10)

        # 返回按钮
        btn_back = ttk.Button(
            toolbar,
            text="←返回主菜单",
            command=lambda: self.controller.show_view('menu')
        )
        btn_back.pack(side='left')
        
        # 标题
        title_label = ttk.Label(
            toolbar,
            text="月历打印｜风带来故事的种子，时间使之发芽",
            font=('Times New Roman', 20, 'bold')
        )
        title_label.pack(side='left', padx=20)
        
        # 日期选择区域
        date_frame = ttk.Frame(self)
        date_frame.pack(pady=20)
        
        # 上个月按钮
        btn_prev = ttk.Button(
            date_frame,
            text="◀",
            width=3,
            command=self.prev_month
        )
        btn_prev.grid(row=0, column=0, padx=5)
        
        # 年份输入
        ttk.Label(date_frame, text="年份:").grid(row=0, column=1, padx=5)
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_entry = ttk.Entry(
            date_frame,
            textvariable=self.year_var,
            width=8,
            justify='center'
        )
        year_entry.grid(row=0, column=2, padx=5)
        year_entry.bind('<Return>', lambda e: self.update_calendar())
        
        # 月份输入
        ttk.Label(date_frame, text="月份:").grid(row=0, column=3, padx=5)
        self.month_var = tk.StringVar(value=str(self.current_month))
        month_entry = ttk.Entry(
            date_frame,
            textvariable=self.month_var,
            width=6,
            justify='center'
        )
        month_entry.grid(row=0, column=4, padx=5)
        month_entry.bind('<Return>', lambda e: self.update_calendar())
        
        # 下个月按钮
        btn_next = ttk.Button(
            date_frame,
            text="▶",
            width=3,
            command=self.next_month
        )
        btn_next.grid(row=0, column=5, padx=5)
        
        # 刷新按钮
        btn_refresh = ttk.Button(
            date_frame,
            text="刷新",
            command=self.update_calendar
        )
        btn_refresh.grid(row=0, column=6, padx=10)
        
        # 统计信息
        self.stats_label = ttk.Label(date_frame, text="", foreground='gray')
        self.stats_label.grid(row=0, column=7, padx=10)
        
        # 日历显示区域
        self.calendar_frame = ttk.Frame(self)
        self.calendar_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # 初始化日历
        self.update_calendar()
    
    def prev_month(self):
        """上一个月"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        
        self.year_var.set(str(self.current_year))
        self.month_var.set(str(self.current_month))
        self.update_calendar()
    
    def next_month(self):
        """下一个月"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        
        self.year_var.set(str(self.current_year))
        self.month_var.set(str(self.current_month))
        self.update_calendar()
    
    def update_calendar(self):
        """更新日历显示"""
        # 验证
        is_valid, year, month, _, error_msg = parse_and_validate_date(
            self.year_var.get(),
            self.month_var.get(),
            "1"
        )
        
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
        self.current_year = year
        self.current_month = month
        
        # 清空现有日历
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # 星期标题
        weekdays = ['日', '一', '二', '三', '四', '五', '六']
        for col, day in enumerate(weekdays):
            label = ttk.Label(
                self.calendar_frame,
                text=day,
                font=('Times New Roman', 12, 'bold'),
                width=8,
                anchor='center',
                relief='solid',
                borderwidth=1
            )
            label.grid(row=0, column=col, sticky='nsew', padx=1, pady=1)
        
        # 获取日历数据
        calendar_data = get_month_calendar(year, month)
        
        # 本月有事件的天数
        days_with_events = 0
        total_events_count = 0
        
        # 显示日期
        for row_idx, week in enumerate(calendar_data):
            for col_idx, day in enumerate(week):
                if day == 0:
                    # 空白日期
                    label = ttk.Label(
                        self.calendar_frame,
                        text="",
                        width=8,
                        anchor='center',
                        relief='solid',
                        borderwidth=1
                    )
                else:
                    # 检查是否有事件
                    events = self.controller.storage.get_events_for_date(
                        self.controller.events,
                        year, month, day
                    )
                    has_events = len(events) > 0
                    
                    if has_events:
                        days_with_events += 1
                        total_events_count += len(events)
                    
                    # 创建日期标签
                    bg_color = "#c0eec7" if has_events else "#e5f0e6"
                    fg_color = "#0e3c28" if has_events else "#041f13"
                    
                    # 如果有多个事件，显示数量
                    if len(events) > 1:
                        text = f"{day}\n●×{len(events)}"
                    elif has_events:
                        text = f"{day}\n●"
                    else:
                        text = str(day)
                    
                    label = tk.Label(
                        self.calendar_frame,
                        text=text,
                        font=('Times New Roman', 11, 'bold' if has_events else 'normal'),
                        width=8,
                        height=3,
                        anchor='center',
                        relief='solid',
                        borderwidth=1,
                        bg=bg_color,
                        fg=fg_color,
                        cursor='hand2'
                    )
                    
                    # 点击跳转到日期查询
                    label.bind('<Button-1>', 
                             lambda e, d=day: self.on_day_click(d))
                
                label.grid(row=row_idx + 1, column=col_idx, 
                         sticky='nsew', padx=1, pady=1)
        
        # 配置网格权重
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(calendar_data) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)
        
        # 更新统计信息
        if days_with_events > 0:
            self.stats_label.config(
                text=f"本月 {days_with_events} 天有事件，共 {total_events_count} 个"
            )
        else:
            self.stats_label.config(text="本月暂无事件")
    
    def on_day_click(self, day):
        """点击日期时的处理"""
        self.controller.selected_date = (self.current_year, self.current_month, day)
        self.controller.show_view('date_query')
    
    def show(self):
        """显示视图时自动刷新"""
        self.update_calendar()