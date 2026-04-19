1. class RepeatType事件重复类型常量
2. class Event事件类
	1. def \__init\__
	2. def occurs_on_date(self, target_year, target_month, target_day)判断事件是否在指定日期发生
	3. split_at_date(self, split_year, split_month, split_day, new_id_func)在指定日期分裂事件为三个部分
	    *返回: (before_event, current_event, after_event)*
	  4. _get_next_occurrence(self, from_year, from_month, from_day)获取指定日期之后的下一次发生日期
	  5. _adjust_repeat_count(self, split_year, split_month, split_day)调整分裂后的重复次数
	  6. delete_from_date(self, delete_year, delete_month, delete_day)从指定日期开始删除（包含当天）
	    *返回修改后的事件，如果完全删除返回None*
	  7. delete_single_date(self, delete_year, delete_month, delete_day, new_id_func)删除单个日期的事件实例
	    *返回: (before_event, after_event)*
	  8. to_dict(self)转换为字典（用于序列化）
	  9. def from_dict(data)从字典创建事件对象
	  10. get_repeat_type_name(self)获取重复类型的中文名称
	  11. \__str\__字符串表示