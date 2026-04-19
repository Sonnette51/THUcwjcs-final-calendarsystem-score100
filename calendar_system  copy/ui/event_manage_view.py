"""
事件管理视图模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
from models.event import Event, RepeatType
from models.date_utils import parse_and_validate_date

class EventManageView(ttk.Frame):
    """事件管理视图"""
    
    def __init__(self, parent, controller):
        """初始化"""
        super().__init__(parent)
        self.controller = controller
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
            text="事件管理｜流水奔去远方呢，或许只是经过我而不停留",
            font=('Times New Roman', 20, 'bold')
        )
        title_label.pack(side='left', padx=20)
        
        # 添加事件按钮
        btn_add = ttk.Button(
            toolbar,
            text="添加事件",
            command=self.show_add_dialog
        )
        btn_add.pack(side='right')
        
        # 刷新按钮
        btn_refresh = ttk.Button(
            toolbar,
            text="刷新",
            command=self.refresh_event_list
        )
        btn_refresh.pack(side='right', padx=5)
        
        # 搜索区域
        search_frame = ttk.Frame(self)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(search_frame, text="搜索:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_event_list())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # 统计信息
        self.stats_label = ttk.Label(search_frame, text="", foreground='gray')
        self.stats_label.pack(side='left', padx=20)
        
        # 事件列表区域
        list_frame = ttk.LabelFrame(self, text="事件列表", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 创建树形视图
        columns = ('name', 'date', 'repeat', 'description')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        # 设置列
        self.tree.heading('#0', text='ID')
        self.tree.heading('name', text='事件名称')
        self.tree.heading('date', text='开始日期')
        self.tree.heading('repeat', text='重复类型')
        self.tree.heading('description', text='描述')
        
        self.tree.column('#0', width=80)
        self.tree.column('name', width=200)
        self.tree.column('date', width=120)
        self.tree.column('repeat', width=150)
        self.tree.column('description', width=250)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 右键菜单
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="编辑", command=self.edit_selected_event)
        self.context_menu.add_command(label="删除", command=self.delete_selected_event)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="切换星标", command=self.toggle_star)
        
        self.tree.bind('<Button-2>', self.show_context_menu)
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_event())
        
        # 初始加载事件列表
        self.refresh_event_list()
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def refresh_event_list(self):
        """刷新事件列表"""
        # 清空列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取搜索关键词
        keyword = self.search_var.get()
        
        # 搜索事件
        events = self.controller.storage.search_events(
            self.controller.events,
            keyword
        )
        
        # 添加到列表
        for event in events:
            star = '⭐' if event.starred else ''
            name = f"{star} {event.name}"
            date = f"{event.start_year}-{event.start_month:02d}-{event.start_day:02d}"
            repeat = event.get_repeat_type_name()
            
            # 获取总次数
            total = None
            try:
                total = event.total_occurrences()
            except Exception as e:
                print(f"计算事件{event.id}次数出错: {e}")
                total = None

            if total is not None:
                repeat += f" (共{total}次)"
            else:
                repeat += " (无限)"
            
            self.tree.insert(
                '',
                'end',
                text=str(event.id),
                values=(name, date, repeat, event.description or '')
            )
        
        # 更新统计信息
        total_count = len(self.controller.events)
        shown_count = len(events)
        if keyword:
            self.stats_label.config(text=f"显示 {shown_count}/{total_count} 个事件")
        else:
            self.stats_label.config(text=f"共 {total_count} 个事件")
    
    def show_add_dialog(self):
        """显示添加事件对话框"""
        dialog = EventDialog(self, self.controller, mode='add')
        self.wait_window(dialog)
    
    def edit_selected_event(self):
        """编辑选中的事件"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个事件")
            return
        
        item = selection[0]
        event_id = int(self.tree.item(item, 'text'))
        
        # 找到事件
        event = self._find_event_by_id(event_id)
        
        if event is None:
            messagebox.showerror("事件不存在")
            self.refresh_event_list()
            return
        
        dialog = EventDialog(self, self.controller, mode='edit', event=event)
        self.wait_window(dialog)
    
    def delete_selected_event(self):
        """删除选中的事件"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个事件")
            return
        
        item = selection[0]
        event_id = int(self.tree.item(item, 'text'))
        
        # 找到事件
        event = self._find_event_by_id(event_id)
        
        if event is None:
            messagebox.showerror("事件不存在")
            self.refresh_event_list()
            return
        
        event_name = event.name
        
        result = messagebox.askyesno(
            "确认删除",
            f"确定要删除事件 '{event_name}' 及其所有重复吗？"
        )
        
        if result:
            # 创建新的事件列表
            new_events = [e for e in self.controller.events if e.id != event_id]
            # 统一应用变更
            self.controller.apply_events_change(new_events)
            messagebox.showinfo("成功", "事件已删除")
    
    def toggle_star(self):
        """切换星标状态"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个事件")
            return
        
        item = selection[0]
        event_id = int(self.tree.item(item, 'text'))
        
        # 找到事件
        event = self._find_event_by_id(event_id)
        
        if event is None:
            messagebox.showerror("事件不存在")
            self.refresh_event_list()
            return
        
        # 切换星标
        event.starred = not event.starred
        # 统一应用变更
        self.controller.apply_events_change(self.controller.events)
    
    def _find_event_by_id(self, event_id):
        """
        通过ID查找事件
        """
        for event in self.controller.events:
            if event.id == event_id:
                return event
        return None
    
    def show(self):
        """显示视图时自动刷新"""
        self.refresh_event_list()

class EventDialog(tk.Toplevel):
    """事件添加/编辑对话框"""
    
    def __init__(self, parent, controller, mode='add', event=None):
        """
        初始化对话框
        mode: 'add' 或 'edit'
        """
        super().__init__(parent)
        self.controller = controller
        self.mode = mode
        self.event = event
        
        self.title("添加事件" if mode == 'add' else "编辑事件")
        self.geometry("550x650")
        self.resizable(False, False)
        
        # 居中显示
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        if mode == 'edit' and event:
            self.load_event_data()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """关闭对话框时的处理"""
        self.grab_release()
        self.destroy()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 事件名称
        ttk.Label(main_frame, text="事件名称:").grid(row=1, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=1, column=1, columnspan=2, sticky='ew', pady=5)
        name_entry.bind('<FocusIn>', lambda e: e.widget.selection_range(0, tk.END))
        
        # 事件描述
        ttk.Label(main_frame, text="描述:").grid(row=2, column=0, sticky='nw', pady=5)
        self.description_text = tk.Text(main_frame, height=3, width=40)
        self.description_text.grid(row=2, column=1, columnspan=2, sticky='ew', pady=5)
        
        # 开始日期
        ttk.Label(main_frame, text="开始日期:").grid(row=3, column=0, sticky='w', pady=5)
        
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=3, column=1, columnspan=2, sticky='w', pady=5)
        
        self.year_var = tk.StringVar(value="2025")
        year_spinbox = ttk.Spinbox(date_frame, from_=1, to=9999, textvariable=self.year_var, width=8)
        year_spinbox.pack(side='left', padx=2)
        ttk.Label(date_frame, text="年").pack(side='left')
        
        self.month_var = tk.StringVar(value="1")
        month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, textvariable=self.month_var, width=6)
        month_spinbox.pack(side='left', padx=2)
        ttk.Label(date_frame, text="月").pack(side='left')
        
        self.day_var = tk.StringVar(value="1")
        day_spinbox = ttk.Spinbox(date_frame, from_=1, to=31, textvariable=self.day_var, width=6)
        day_spinbox.pack(side='left', padx=2)
        ttk.Label(date_frame, text="日").pack(side='left')
        
        # 重复类型
        ttk.Label(main_frame, text="重复类型:").grid(row=4, column=0, sticky='w', pady=5)
        self.repeat_var = tk.StringVar(value=RepeatType.ONCE)
        repeat_combo = ttk.Combobox(main_frame, textvariable=self.repeat_var, width=37, state='readonly')
        repeat_combo['values'] = (
            '单次事件',
            '每日重复',
            '每周重复',
            '每月重复',
            '每年重复',
            '自定义间隔'
        )
        repeat_combo.current(0)
        repeat_combo.bind('<<ComboboxSelected>>', self.on_repeat_change)
        repeat_combo.grid(row=4, column=1, columnspan=2, sticky='ew', pady=5)
        
        # 自定义间隔
        self.custom_frame = ttk.Frame(main_frame)
        self.custom_frame.grid(row=5, column=1, columnspan=2, sticky='w', pady=5)
        self.custom_frame.grid_remove()
        
        ttk.Label(self.custom_frame, text="间隔天数：").pack(side='left')
        self.custom_interval_var = tk.StringVar(value="1")
        custom_spinbox = ttk.Spinbox(
            self.custom_frame, 
            from_=1, 
            to=365, 
            textvariable=self.custom_interval_var, 
            width=10
        )
        custom_spinbox.pack(side='left', padx=5)
        
        # 重复次数
        self.repeat_count_frame = ttk.Frame(main_frame)
        self.repeat_count_frame.grid(row=6, column=0, columnspan=3, sticky='w', pady=5)
        
        ttk.Label(self.repeat_count_frame, text="重复次数:").pack(side='left')
        self.infinite_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.repeat_count_frame,
            text="无限重复",
            variable=self.infinite_var,
            command=self.on_infinite_change
        ).pack(side='left', padx=10)
        
        ttk.Label(self.repeat_count_frame, text="或指定次数 (1-10000):").pack(side='left', padx=5)
        self.repeat_count_var = tk.StringVar(value="")
        self.repeat_count_entry = ttk.Spinbox(
            self.repeat_count_frame,
            from_=1,
            to=10000,
            textvariable=self.repeat_count_var,
            width=10,
            state='disabled'
        )
        self.repeat_count_entry.pack(side='left')
        
        # 星标
        self.starred_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            main_frame,
            text="⭐ 标记为重要",
            variable=self.starred_var
        ).grid(row=7, column=1, columnspan=2, sticky='w', pady=10)
        
        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=9, column=0, columnspan=3, pady=20)
        
        ttk.Button(
            btn_frame,
            text="保存" if self.mode == 'add' else "更新",
            command=self.save_event,
            width=15
        ).pack(side='left', padx=10)
        
        ttk.Button(
            btn_frame,
            text="取消",
            command=self.on_closing,
            width=15
        ).pack(side='left', padx=10)
    
    def on_repeat_change(self, event=None):
        """重复类型改变时的处理"""
        repeat_type = self.repeat_var.get()
        
        if repeat_type == '自定义间隔':
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()
        
        if repeat_type == '单次事件':
            self.repeat_count_frame.grid_remove()
        else:
            self.repeat_count_frame.grid()
    
    def on_infinite_change(self):
        """无限重复复选框改变时的处理"""
        if self.infinite_var.get():
            self.repeat_count_entry.config(state='disabled')
            self.repeat_count_var.set("")
        else:
            self.repeat_count_entry.config(state='normal')
    
    def load_event_data(self):
        """加载事件数据（编辑模式）"""
        self.name_var.set(self.event.name)
        self.description_text.insert('1.0', self.event.description or '')
        self.year_var.set(str(self.event.start_year))
        self.month_var.set(str(self.event.start_month))
        self.day_var.set(str(self.event.start_day))
        
        # 设置重复类型
        repeat_map = {
            RepeatType.ONCE: 0,
            RepeatType.DAILY: 1,
            RepeatType.WEEKLY: 2,
            RepeatType.MONTHLY: 3,
            RepeatType.YEARLY: 4,
            RepeatType.CUSTOM: 5
        }
        idx = repeat_map.get(self.event.repeat_type, 0)
        self.repeat_var.set(['单次事件', '每日重复', '每周重复', '每月重复', '每年重复', '自定义间隔'][idx])
        self.on_repeat_change()
        
        if self.event.repeat_type == RepeatType.CUSTOM:
            self.custom_interval_var.set(str(self.event.custom_interval))
        
        if self.event.repeat_count:
            self.infinite_var.set(False)
            self.repeat_count_var.set(str(self.event.repeat_count))
            self.on_infinite_change()
        
        self.starred_var.set(self.event.starred)


    def save_event(self):
        """保存事件"""
        try:
            # 验证事件名称
            name = self.name_var.get().strip()
            if not name:
                messagebox.showerror("输入错误", "事件名称不能为空")
                return
            
            if len(name) > 100:
                messagebox.showerror("输入错误", "事件名称不能超过100个字符")
                return
            
            # 验证描述
            description = self.description_text.get('1.0', 'end').strip()
            if len(description) > 500:
                messagebox.showerror("输入错误", "事件描述不能超过500个字符")
                return
            
            # 日期验证
            is_valid, year, month, day, error_msg = parse_and_validate_date(
                self.year_var.get(),
                self.month_var.get(),
                self.day_var.get()
            )
            
            if not is_valid:
                messagebox.showerror("输入错误", error_msg)
                return
            
            # 获取重复类型
            repeat_text = self.repeat_var.get()
            repeat_map = {
                '单次事件': RepeatType.ONCE,
                '每日重复': RepeatType.DAILY,
                '每周重复': RepeatType.WEEKLY,
                '每月重复': RepeatType.MONTHLY,
                '每年重复': RepeatType.YEARLY,
                '自定义间隔': RepeatType.CUSTOM
            }
            repeat_type = repeat_map[repeat_text]
            
            # 获取自定义间隔
            custom_interval = 1
            if repeat_type == RepeatType.CUSTOM:
                try:
                    custom_interval = int(self.custom_interval_var.get())
                    if custom_interval < 1:
                        messagebox.showerror("输入错误", "自定义间隔必须是正整数")
                        return
                except ValueError:
                    messagebox.showerror("输入错误", "自定义间隔必须是整数")
                    return
            
            # 获取重复次数
            repeat_count = None
            if not self.infinite_var.get():
                repeat_count_str = self.repeat_count_var.get().strip()
                
                if not repeat_count_str:
                    messagebox.showerror("输入错误", "请输入重复次数，或勾选无限重复")
                    return
                
                try:
                    repeat_count = int(repeat_count_str)
                    if repeat_count < 1:
                        messagebox.showerror("输入错误", "重复次数必须是正整数")
                        return
                    if repeat_count > 10000:
                        messagebox.showerror("输入错误", "重复次数不能超过10000次")
                        return
                except ValueError:
                    messagebox.showerror("输入错误", "重复次数必须是整数")
                    return
            
            starred = self.starred_var.get()
            
            if self.mode == 'add':
                # 添加新事件
                event = Event(
                    event_id=int(time.time() * 1000000),
                    name=name,
                    description=description,
                    start_year=year,
                    start_month=month,
                    start_day=day,
                    repeat_type=repeat_type,
                    custom_interval=custom_interval,
                    repeat_count=repeat_count,
                    starred=starred
                )
                
                new_events = self.controller.events + [event]
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件已成功添加!")
            else:
                new_events = []
                event_found = False
                
                for e in self.controller.events:
                    if e.id == self.event.id:
                        e.name = name
                        e.description = description
                        e.start_year = year
                        e.start_month = month
                        e.start_day = day
                        e.repeat_type = repeat_type
                        e.custom_interval = custom_interval
                        e.repeat_count = repeat_count
                        e.starred = starred
                        # 重置结束日期与排除日期（编辑事件时清除 enddate 相关数据）
                        e.end_year = None
                        e.end_month = None
                        e.end_day = None
                        e.excluded_dates = []
                        event_found = True
                    new_events.append(e)
                
                if not event_found:
                    messagebox.showerror("错误", "该事件已被删除或修改，无法更新")
                    self.on_closing()
                    return
                
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件已成功更新!")
            
            self.on_closing()
        
        except Exception as e:
            messagebox.showerror("未知错误", f"保存事件时发生错误：{str(e)}")