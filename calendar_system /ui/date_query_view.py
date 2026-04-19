"""
日期查询视图模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
from models.date_utils import (
    get_weekday_name, 
    get_lunar_date, 
    get_days_in_month,
    parse_and_validate_date
)

class DateQueryView(ttk.Frame):
    """日期查询视图"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 顶部工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=10)
        
        btn_back = ttk.Button(
            toolbar,
            text="←返回主菜单",
            command=lambda: self.controller.show_view('menu')
        )
        btn_back.pack(side='left')
        
        title_label = ttk.Label(
            toolbar,
            text="日期查询｜跟我回去十八岁,不要被命运找到",
            font=('Times New Roman', 20, 'bold')
        )
        title_label.pack(side='left', padx=20)
        
        # 日期输入区域
        input_frame = ttk.LabelFrame(self, text="输入日期", padding=20)
        input_frame.pack(pady=20, padx=20, fill='x')
        
        date_frame = ttk.Frame(input_frame)
        date_frame.pack()
        
        # 年份
        ttk.Label(date_frame, text="年份:").grid(row=0, column=0, padx=5, pady=5)
        self.year_var = tk.StringVar(value="2025")
        year_spinbox = ttk.Spinbox(
            date_frame,
            from_=1,
            to=9999,
            textvariable=self.year_var,
            width=10,
            justify='center'
        )
        year_spinbox.grid(row=0, column=1, padx=5, pady=5)
        year_spinbox.bind('<FocusIn>', lambda e: e.widget.selection_range(0, tk.END))
        
        # 月份
        ttk.Label(date_frame, text="月份:").grid(row=0, column=2, padx=5, pady=5)
        self.month_var = tk.StringVar(value="1")
        month_spinbox = ttk.Spinbox(
            date_frame,
            from_=1,
            to=12,
            textvariable=self.month_var,
            width=8,
            justify='center',
            command=self.on_month_change
        )
        month_spinbox.grid(row=0, column=3, padx=5, pady=5)
        month_spinbox.bind('<FocusIn>', lambda e: e.widget.selection_range(0, tk.END))
        
        # 日期
        ttk.Label(date_frame, text="日期:").grid(row=0, column=4, padx=5, pady=5)
        self.day_var = tk.StringVar(value="1")
        self.day_spinbox = ttk.Spinbox(
            date_frame,
            from_=1,
            to=31,
            textvariable=self.day_var,
            width=8,
            justify='center'
        )
        self.day_spinbox.grid(row=0, column=5, padx=5, pady=5)
        self.day_spinbox.bind('<FocusIn>', lambda e: e.widget.selection_range(0, tk.END))
        
        # 查询
        btn_query = ttk.Button(
            date_frame,
            text="查询",
            command=self.query_date
        )
        btn_query.grid(row=0, column=6, padx=10, pady=5)
        
        # 日期信息显示区域
        self.info_frame = ttk.LabelFrame(self, text="日期信息", padding=20)
        self.info_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # 事件列表显示区域
        self.events_frame = ttk.LabelFrame(self, text="当天事件", padding=20)
        self.events_frame.pack(pady=10, padx=20, fill='both', expand=True)
    
    def on_month_change(self):
        """月份改变时更新日期范围"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            max_day = get_days_in_month(year, month)
            self.day_spinbox.config(to=max_day)
        except:
            pass
    
    def show(self):
        """显示视图时的处理"""
        if hasattr(self.controller, 'selected_date'):
            year, month, day = self.controller.selected_date
            self.year_var.set(str(year))
            self.month_var.set(str(month))
            self.day_var.set(str(day))
            self.query_date()
    
    def query_date(self):
        """查询日期信息"""
        # 验证函数
        is_valid, year, month, day, error_msg = parse_and_validate_date(
            self.year_var.get(),
            self.month_var.get(),
            self.day_var.get()
        )
        
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
        # 清空信息显示区域
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        # 显示日期信息
        info_text = f"公历日期: {year}年{month}月{day}日\n"
        info_text += f"星期: {get_weekday_name(year, month, day)}\n"
            
        # 获取农历
        lunar_date = get_lunar_date(year, month, day)
        info_text += f"农历: {lunar_date}"
            
        info_label = ttk.Label(
            self.info_frame,
            text=info_text,
            font=('Times New Roman', 20),
            justify='left'
        )
        info_label.pack(anchor='w')
            
        # 显示事件列表
        self.display_events(year, month, day)
        
    def display_events(self, year, month, day):
        """显示事件列表"""
        for widget in self.events_frame.winfo_children():
            widget.destroy()
        
        events = self.controller.storage.get_events_for_date(
            self.controller.events,
            year, month, day
        )
        
        if not events:
            no_event_label = ttk.Label(
                self.events_frame,
                text="当天无事件",
                foreground='gray'
            )
            no_event_label.pack()
            return
        
        count_label = ttk.Label(
            self.events_frame,
            text=f"共 {len(events)} 个事件",
            font=('Times New Roman', 10, 'bold')
        )
        count_label.pack(anchor='w', pady=(0, 10))
        
        # 创建滚动区域
        canvas = tk.Canvas(self.events_frame, height=200)
        scrollbar = ttk.Scrollbar(self.events_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 显示每个事件
        for event in events:
            event_frame = ttk.Frame(scrollable_frame, relief='solid', borderwidth=1)
            event_frame.pack(fill='x', pady=5, padx=5)
            
            # 事件信息
            info_frame = ttk.Frame(event_frame)
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
            
            # 事件名称
            name_text = f"{'⭐ ' if event.starred else ''}{event.name}"
            name_label = ttk.Label(
                info_frame,
                text=name_text,
                font=('Times New Roman', 11, 'bold')
            )
            name_label.pack(anchor='w')
            
            # 事件描述
            if event.description:
                desc_label = ttk.Label(
                    info_frame,
                    text=event.description,
                    foreground='gray'
                )
                desc_label.pack(anchor='w')
            
            # 重复信息
            repeat_text = f"重复类型: {event.get_repeat_type_name()}"
            total = None
            try:
                total = event.total_occurrences()
            except Exception:
                total = None
            if total is not None:
                repeat_text += f" (共{total}次)"
            else:
                repeat_text += " (无限重复)"
            
            repeat_label = ttk.Label(
                info_frame,
                text=repeat_text,
                font=('Times New Roman', 9),
                foreground='blue'
            )
            repeat_label.pack(anchor='w')
            
            # 管理按钮
            btn_frame = ttk.Frame(event_frame)
            btn_frame.pack(side='right', padx=5)
            
            btn_edit = ttk.Button(
                btn_frame,
                text="编辑",
                width=12,
                command=lambda e=event, y=year, m=month, d=day: 
                    self.edit_event_instance(e, y, m, d)
            )
            btn_edit.pack(pady=2)
            
            btn_delete_single = ttk.Button(
                btn_frame,
                text="删除此次",
                width=12,
                command=lambda e=event, y=year, m=month, d=day: 
                    self.delete_single_instance(e, y, m, d)
            )
            btn_delete_single.pack(pady=2)
            
            btn_delete_future = ttk.Button(
                btn_frame,
                text="删除此后",
                width=12,
                command=lambda e=event, y=year, m=month, d=day: 
                    self.delete_from_date(e, y, m, d)
            )
            btn_delete_future.pack(pady=2)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def edit_event_instance(self, event, year, month, day):
        """编辑事件实例"""
        dialog = EventInstanceEditDialog(
            self, 
            self.controller, 
            event, 
            year, month, day
        )
        self.wait_window(dialog)
    
    def delete_single_instance(self, event, year, month, day):
        """删除单个事件实例"""
        from models.event import RepeatType
        
        if event.repeat_type == RepeatType.ONCE:
            result = messagebox.askyesno(
                "确认删除",
                f"确定要删除事件 '{event.name}' 吗？"
            )
            if result:
                new_events = [e for e in self.controller.events if e.id != event.id]
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件已删除")
        else:
            result = messagebox.askyesno(
                "确认删除",
                f"确定要删除 {year}年{month}月{day}日 的 '{event.name}' 事件吗？\n\n"
                f"该事件的其他重复实例将被分裂为两个系列：\n"
                f"此日期之前的系列\n"
                f"此日期之后的系列"
            )
            if result:
                new_id = lambda: int(time.time() * 1000000)
                before_event, after_event = event.delete_single_date(
                    year, month, day, new_id
                )
                
                new_events = [e for e in self.controller.events if e.id != event.id]
                
                if before_event:
                    new_events.append(before_event)
                if after_event:
                    new_events.append(after_event)
                
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件已删除，系列已分裂")
    
    def delete_from_date(self, event, year, month, day):
        """从指定日期开始删除"""
        from models.event import RepeatType
        
        if event.repeat_type == RepeatType.ONCE:
            result = messagebox.askyesno(
                "确认删除",
                f"确定要删除事件 '{event.name}' 吗？"
            )
            if result:
                new_events = [e for e in self.controller.events if e.id != event.id]
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件已删除")
        else:
            result = messagebox.askyesno(
                "确认删除",
                f"确定要删除从 {year}年{month}月{day}日 开始的所有 '{event.name}' 事件吗？\n\n"
                f"包括本次及未来的所有，但保留过去的记录"
            )
            if result:
                modified_event = event.delete_from_date(year, month, day)
                
                if modified_event is None:
                    new_events = [e for e in self.controller.events if e.id != event.id]
                else:
                    new_events = []
                    for e in self.controller.events:
                        if e.id == event.id:
                            new_events.append(modified_event)
                        else:
                            new_events.append(e)
                
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "已删除此日期及之后的所有重复")


class EventInstanceEditDialog(tk.Toplevel):
    """事件实例编辑对话框"""
    
    def __init__(self, parent, controller, event, year, month, day):
        super().__init__(parent)
        self.controller = controller
        self.event = event
        self.year = year
        self.month = month
        self.day = day
        
        self.title("编辑事件")
        self.geometry("500x550")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """关闭对话框时的处理"""
        self.grab_release()
        self.destroy()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 提示信息
        info_label = ttk.Label(
            main_frame,
            text=f"编辑 {self.year}年{self.month}月{self.day}日的事件",
            font=('Times New Roman', 18, 'bold'),
        )
        info_label.pack(pady=10)
        
        # 事件名称
        ttk.Label(main_frame, text="事件名称:").pack(anchor='w', pady=5)
        self.name_var = tk.StringVar(value=self.event.name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=50)
        name_entry.pack(fill='x', pady=5)
        name_entry.bind('<FocusIn>', lambda e: e.widget.selection_range(0, tk.END))
        
        # 事件描述
        ttk.Label(main_frame, text="描述:").pack(anchor='w', pady=5)
        self.description_text = tk.Text(main_frame, height=5, width=50)
        self.description_text.insert('1.0', self.event.description or '')
        self.description_text.pack(fill='x', pady=5)
        
        # 星标
        self.starred_var = tk.BooleanVar(value=self.event.starred)
        ttk.Checkbutton(
            main_frame,
            text="⭐ 标记为重要",
            variable=self.starred_var
        ).pack(anchor='w', pady=10)
        
        # 修改范围选择
        ttk.Label(main_frame, text="修改范围:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)
        
        self.scope_var = tk.StringVar(value="all")
        
        ttk.Radiobutton(
            main_frame,
            text="修改整个事件系列",
            variable=self.scope_var,
            value="all"
        ).pack(anchor='w', padx=20)
        
        from models.event import RepeatType
        if self.event.repeat_type != RepeatType.ONCE:
            ttk.Radiobutton(
                main_frame,
                text="仅修改此次事件",
                variable=self.scope_var,
                value="single"
            ).pack(anchor='w', padx=20)
        
        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(
            btn_frame,
            text="保存",
            command=self.save_changes,
            width=15
        ).pack(side='left', padx=10)
        
        ttk.Button(
            btn_frame,
            text="取消",
            command=self.on_closing,
            width=15
        ).pack(side='left', padx=10)
    
    def save_changes(self):
        """保存修改"""
        # 验证输入
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("输入错误", "事件名称不能为空")
            return
        
        if len(name) > 100:
            messagebox.showerror("输入错误", "事件名称不能超过100个字符")
            return
        
        description = self.description_text.get('1.0', 'end').strip()
        if len(description) > 500:
            messagebox.showerror("输入错误", "事件描述不能超过500个字符")
            return
        
        starred = self.starred_var.get()
        scope = self.scope_var.get()
        
        try:
            if scope == "all":
                new_events = []
                event_found = False
                
                for e in self.controller.events:
                    if e.id == self.event.id:
                        e.name = name
                        e.description = description
                        e.starred = starred
                        event_found = True
                    new_events.append(e)
                
                if not event_found:
                    messagebox.showerror("错误", "该事件已被删除或修改，无法更新")
                    self.on_closing()
                    return
                
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件系列已更新")
            else:
                # 仅修改此次
                new_id = lambda: int(time.time() * 1000000)
                before, current, after = self.event.split_at_date(
                    self.year, self.month, self.day, new_id
                )
                
                current.name = name
                current.description = description
                current.starred = starred

                new_events = [e for e in self.controller.events if e.id != self.event.id]
                
                if before:
                    new_events.append(before)
                new_events.append(current)
                if after:
                    new_events.append(after)
                
                self.controller.apply_events_change(new_events)
                messagebox.showinfo("成功", "事件已分裂并更新")
            
            self.on_closing()
        
        except Exception as e:
            messagebox.showerror("保存失败", f"保存事件时发生错误：{str(e)}")