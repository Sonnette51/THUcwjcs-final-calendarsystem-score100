"""
事件存储管理
"""
import json
import os
from models.event import Event

class EventStorage:
    """事件存储管理类"""
    
    def __init__(self, data_file='data/events.json'):
        """
        初始化
        """
        self.data_file = data_file
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """确保数据目录存在"""
        directory = os.path.dirname(self.data_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_events(self, events):
        """
        保存事件列表到文件 
        """
        try:
            data = [event.to_dict() for event in events]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存事件失败: {e}")
            return False
    
    def load_events(self):
        """
        从文件加载事件列表
        """
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            events = [Event.from_dict(item) for item in data]
            return events
        except Exception as e:
            print(f"加载事件失败: {e}")
            return []
    
    def add_event(self, events, event):
        """
        添加事件并保存
        events: 当前事件列表
        event: 要添加的事件
        """
        events.append(event)
        self.save_events(events)
        return events
    
    def delete_event(self, events, event_id):
        """
        删除事件并保存
        events: 当前事件列表
        event_id: 要删除的事件ID
        """
        events = [e for e in events if e.id != event_id]
        self.save_events(events)
        return events
    
    def update_event(self, events, event_id, updates):
        """
        更新事件并保存
        events: 当前事件列表
        event_id: 要更新的事件ID
        updates: 更新的属性字典
        """
        for event in events:
            if event.id == event_id:
                for key, value in updates.items():
                    if hasattr(event, key):
                        setattr(event, key, value)
                break
        self.save_events(events)
        return events
    
    def get_events_for_date(self, events, year, month, day):
        """
        获取指定日期的所有事件
        """
        return [event for event in events if event.occurs_on_date(year, month, day)]

    def search_events(self, events, keyword):
        """
        搜索事件
        events: 事件列表
        keyword: 搜索关键词
        """
        if not keyword:
            return events
        
        keyword = keyword.lower()
        return [
            event for event in events
            if keyword in event.name.lower() or 
               (event.description and keyword in event.description.lower())
        ]