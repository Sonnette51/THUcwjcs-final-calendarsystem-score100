"""
事件相关的东西
"""
from datetime import datetime
from models.date_utils import date_diff_days, get_days_in_month

class RepeatType:
    """事件重复类型"""
    ONCE = 'once'    
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    CUSTOM = 'custom'

class Event:
    """事件类"""
    
    def __init__(self, event_id, name, description, start_year, start_month, start_day,
                 repeat_type=RepeatType.ONCE, custom_interval=1, repeat_count=None, 
                 starred=False, end_year=None, end_month=None, end_day=None,
                 excluded_dates=None):
        """
        初始化事件
        """
        self.id = event_id
        self.name = name
        self.description = description
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.repeat_type = repeat_type
        self.custom_interval = custom_interval
        self.repeat_count = repeat_count
        self.starred = starred
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.excluded_dates = excluded_dates or []
    
    def occurs_on_date(self, target_year, target_month, target_day):
        """
        判断事件是否在指定日期发生
        """
        # 排除否？
        if (target_year, target_month, target_day) in self.excluded_dates:
            return False
    
        # 结束否？
        if self.end_year is not None:
            target_date_num = target_year * 10000 + target_month * 100 + target_day
            end_date_num = self.end_year * 10000 + self.end_month * 100 + self.end_day
            if target_date_num > end_date_num:
                return False
        
        # 天数差
        days_diff = date_diff_days(self.start_year, self.start_month, self.start_day,
                                   target_year, target_month, target_day)
        
        # 目标日期早于开始日期
        if days_diff < 0:
            return False
        
        # 单次事件
        if self.repeat_type == RepeatType.ONCE:
            return (self.start_year == target_year and 
                   self.start_month == target_month and 
                   self.start_day == target_day)
        
        # 每日重复
        elif self.repeat_type == RepeatType.DAILY:
            if self.repeat_count and days_diff >= self.repeat_count:
                return False
            return True
        
        # 每周重复
        elif self.repeat_type == RepeatType.WEEKLY:
            if days_diff % 7 != 0:
                return False
            week_occurrence = days_diff // 7
            if self.repeat_count and week_occurrence >= self.repeat_count:
                return False
            return True
        
        # 每月重复
        elif self.repeat_type == RepeatType.MONTHLY:
            months_diff = (target_year - self.start_year) * 12 + (target_month - self.start_month)
            if months_diff < 0:
                return False
            if self.repeat_count and months_diff >= self.repeat_count:
                return False
            
            # 如果开始日期大于目标月最大天数
            target_max_day = get_days_in_month(target_year, target_month)
            adjusted_day = min(self.start_day, target_max_day)
            return target_day == adjusted_day
        
        # 每年重复
        elif self.repeat_type == RepeatType.YEARLY:
            years_diff = target_year - self.start_year
            if years_diff < 0:
                return False
            if self.repeat_count and years_diff >= self.repeat_count:
                return False
            
            if target_month != self.start_month:
                return False
            
            # 闰年2月29日
            if self.start_month == 2 and self.start_day == 29:
                max_day = get_days_in_month(target_year, 2)
                return target_day == max_day
            
            return target_day == self.start_day
        
        # 自定义间隔
        elif self.repeat_type == RepeatType.CUSTOM:
            if days_diff % self.custom_interval != 0:
                return False
            custom_occurrence = days_diff // self.custom_interval
            if self.repeat_count and custom_occurrence >= self.repeat_count:
                return False
            return True
        
        return False
    
    def split_at_date(self, split_year, split_month, split_day, new_id_func):
        """
        在指定日期分裂事件为三个部分
        返回: (before_event, current_event, after_event)
        """
        if self.repeat_type == RepeatType.ONCE:
            # 单次事件不分裂
            return None, self, None
        
        # 之前的
        before_event = Event(
            event_id=self.id, 
            name=self.name,
            description=self.description,
            start_year=self.start_year,
            start_month=self.start_month,
            start_day=self.start_day,
            repeat_type=self.repeat_type,
            custom_interval=self.custom_interval,
            repeat_count=None, 
            starred=self.starred,
            end_year=split_year,
            end_month=split_month,
            end_day=split_day,
            excluded_dates=self.excluded_dates.copy()
        )
        # 排除当天
        before_event.excluded_dates.append((split_year, split_month, split_day))
        
        # 当天的
        current_event = Event(
            event_id=new_id_func(),
            name=self.name,
            description=self.description,
            start_year=split_year,
            start_month=split_month,
            start_day=split_day,
            repeat_type=RepeatType.ONCE,
            starred=self.starred
        )
        
        # 之后的
        next_date = self._get_next_occurrence(split_year, split_month, split_day)
        
        if next_date:
            next_year, next_month, next_day = next_date
            after_event = Event(
                event_id=new_id_func(),
                name=self.name,
                description=self.description,
                start_year=next_year,
                start_month=next_month,
                start_day=next_day,
                repeat_type=self.repeat_type,
                custom_interval=self.custom_interval,
                repeat_count=self._adjust_repeat_count(split_year, split_month, split_day),
                starred=self.starred,
                end_year=self.end_year,
                end_month=self.end_month,
                end_day=self.end_day
            )
        else:
            after_event = None
        
        return before_event, current_event, after_event
    
    def _get_next_occurrence(self, from_year, from_month, from_day):
        """获取指定日期之后的下一次发生日期"""
        from datetime import datetime, timedelta
        
        if self.repeat_type == RepeatType.DAILY:
            date = datetime(from_year, from_month, from_day) + timedelta(days=1)
            return (date.year, date.month, date.day)
        
        elif self.repeat_type == RepeatType.WEEKLY:
            date = datetime(from_year, from_month, from_day) + timedelta(days=7)
            return (date.year, date.month, date.day)
        
        elif self.repeat_type == RepeatType.MONTHLY:
            next_month = from_month + 1
            next_year = from_year
            if next_month > 12:
                next_month = 1
                next_year += 1
            # 日期边界
            max_day = get_days_in_month(next_year, next_month)
            next_day = min(self.start_day, max_day)
            return (next_year, next_month, next_day)
        
        elif self.repeat_type == RepeatType.YEARLY:
            next_year = from_year + 1
            # 闰年2月29日
            if self.start_month == 2 and self.start_day == 29:
                max_day = get_days_in_month(next_year, 2)
                return (next_year, 2, max_day)
            return (next_year, self.start_month, self.start_day)
        
        elif self.repeat_type == RepeatType.CUSTOM:
            date = datetime(from_year, from_month, from_day) + timedelta(days=self.custom_interval)
            return (date.year, date.month, date.day)
        
        return None
    
    def _adjust_repeat_count(self, split_year, split_month, split_day):
        """调整分裂后的重复次数"""
        if self.repeat_count is None:
            return None
        
        # 计算已经发生的次数
        days_diff = date_diff_days(self.start_year, self.start_month, self.start_day,
                                   split_year, split_month, split_day)
        
        if self.repeat_type == RepeatType.DAILY:
            occurred = days_diff
        elif self.repeat_type == RepeatType.WEEKLY:
            occurred = days_diff // 7
        elif self.repeat_type == RepeatType.MONTHLY:
            occurred = (split_year - self.start_year) * 12 + (split_month - self.start_month)
        elif self.repeat_type == RepeatType.YEARLY:
            occurred = split_year - self.start_year
        elif self.repeat_type == RepeatType.CUSTOM:
            occurred = days_diff // self.custom_interval
        else:
            occurred = 0
        
        remaining = self.repeat_count - occurred - 1 
        return max(0, remaining)
    
    def delete_from_date(self, delete_year, delete_month, delete_day):
        """
        从指定日期开始删除（包含当天）
        返回修改后的事件,如果完全删除返回None
        """
        if self.repeat_type == RepeatType.ONCE:
            # 单次事件直接删
            return None
        
        # 删除日期在事件范围内否？
        if not self.occurs_on_date(delete_year, delete_month, delete_day):
            return self
        
        # 设置结束日期为删除日期前一次发生的时候
        self.end_year = delete_year
        self.end_month = delete_month
        self.end_day = delete_day
        
        # 将删除日期加入排除列表
        if (delete_year, delete_month, delete_day) not in self.excluded_dates:
            self.excluded_dates.append((delete_year, delete_month, delete_day))
        
        # 如果开始日期是重复事件的第一次，则完全删除
        if (self.start_year == delete_year and 
            self.start_month == delete_month and 
            self.start_day == delete_day):
            return None
        
        return self
    
    def delete_single_date(self, delete_year, delete_month, delete_day, new_id_func):
        """
        删除单个日期的事件实例
        返回: (before_event, after_event)
        """
        if self.repeat_type == RepeatType.ONCE:
            # 单次事件直接删
            return None, None
        
        #之前的
        before_event = Event(
            event_id=self.id,
            name=self.name,
            description=self.description,
            start_year=self.start_year,
            start_month=self.start_month,
            start_day=self.start_day,
            repeat_type=self.repeat_type,
            custom_interval=self.custom_interval,
            repeat_count=None,
            starred=self.starred,
            end_year=delete_year,
            end_month=delete_month,
            end_day=delete_day,
            excluded_dates=self.excluded_dates.copy()
        )
        before_event.excluded_dates.append((delete_year, delete_month, delete_day))
        
        # 之后的
        next_date = self._get_next_occurrence(delete_year, delete_month, delete_day)
        
        if next_date:
            next_year, next_month, next_day = next_date
            after_event = Event(
                event_id=new_id_func(),
                name=self.name,
                description=self.description,
                start_year=next_year,
                start_month=next_month,
                start_day=next_day,
                repeat_type=self.repeat_type,
                custom_interval=self.custom_interval,
                repeat_count=self._adjust_repeat_count(delete_year, delete_month, delete_day),
                starred=self.starred,
                end_year=self.end_year,
                end_month=self.end_month,
                end_day=self.end_day
            )
        else:
            after_event = None
        
        return before_event, after_event
    
    def to_dict(self):
        """转为字典（序列化）"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_year': self.start_year,
            'start_month': self.start_month,
            'start_day': self.start_day,
            'repeat_type': self.repeat_type,
            'custom_interval': self.custom_interval,
            'repeat_count': self.repeat_count,
            'starred': self.starred,
            'end_year': self.end_year,
            'end_month': self.end_month,
            'end_day': self.end_day,
            'excluded_dates': self.excluded_dates,
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建事件对象"""
        event = Event(
            event_id=data['id'],
            name=data['name'],
            description=data['description'],
            start_year=data['start_year'],
            start_month=data['start_month'],
            start_day=data['start_day'],
            repeat_type=data.get('repeat_type', RepeatType.ONCE),
            custom_interval=data.get('custom_interval', 1),
            repeat_count=data.get('repeat_count'),
            starred=data.get('starred', False),
            end_year=data.get('end_year'),
            end_month=data.get('end_month'),
            end_day=data.get('end_day'),
            excluded_dates=data.get('excluded_dates', [])
        )
        return event
    
    def get_repeat_type_name(self):
        """获取重复类型的中文名称"""
        names = {
            RepeatType.ONCE: '单次',
            RepeatType.DAILY: '每日',
            RepeatType.WEEKLY: '每周',
            RepeatType.MONTHLY: '每月',
            RepeatType.YEARLY: '每年',
            RepeatType.CUSTOM: f'每{self.custom_interval}天'
        }
        return names.get(self.repeat_type, '未知')
    
    def total_occurrences(self):
        """
        计算事件总共的发生次数
        返回次数或 None 表示无限/未知
        """
        # 单次事件
        if self.repeat_type == RepeatType.ONCE:
            return 1
        
        # 有的repeat_count，但无end_date和excluded_dates
        if self.repeat_count is not None and self.end_year is None and not self.excluded_dates:
            return int(self.repeat_count)
        
        # 无repeat_count无有end_date
        if self.repeat_count is None and self.end_year is None:
            return None
        
        # 需要通过模拟来计算实际发生次数
        count = 0
        current_year, current_month, current_day = self.start_year, self.start_month, self.start_day
        
        # 设置最大迭代次数防止死循环
        MAX_ITERATIONS = 100000
        iterations = 0
        
        while iterations < MAX_ITERATIONS:
            iterations += 1
            
            # 当前日期在范围内否？
            if self.end_year is not None:
                current_date_num = current_year * 10000 + current_month * 100 + current_day
                end_date_num = self.end_year * 10000 + self.end_month * 100 + self.end_day
                if current_date_num > end_date_num:
                    break
            
            # 被排除否？
            if (current_year, current_month, current_day) not in self.excluded_dates:
                count += 1
            
            # 达到repeat_count限制否？
            if self.repeat_count is not None and count >= self.repeat_count:
                break
            
            # 下一次发生
            next_occurrence = self._get_next_occurrence(current_year, current_month, current_day)
            if next_occurrence is None:
                break
            
            current_year, current_month, current_day = next_occurrence
        
        # 如果达到最大迭代次数，返回None表示无法确定
        if iterations >= MAX_ITERATIONS:
            return None
        
        return count
    
