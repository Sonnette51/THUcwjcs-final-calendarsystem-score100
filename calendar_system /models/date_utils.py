"""
日期工具
"""
from datetime import datetime
from lunarcalendar import Converter, Solar

def is_run_year(year):
    """判断是否为闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_days_in_month(year, month):
    """获取指定年月的天数"""
    days_in_month = [31, 29 if is_run_year(year) else 28, 31, 30, 31, 30,31, 31, 30, 31, 30, 31]
    return days_in_month[month - 1]

def get_weekday(year, month, day):
    """
    计算星期几
    返回: 0=周日, 1=周一, ..., 6=周六
    """
    y, m = year, month
    if m < 3:
        m += 12
        y -= 1
    
    c = y // 100
    yy = y % 100
    
    w = (yy + yy // 4 + c // 4 - 2 * c + (26 * (m + 1)) // 10 + day - 1) % 7
    return (w + 7) % 7

def get_weekday_name(year, month, day):
    """获取星期几的中文名称"""
    weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
    return weekdays[get_weekday(year, month, day)]

def get_lunar_date(year, month, day):
    """
    获取农历日期
    """
    try:
        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)
        
        lunar_months = ['正月', '二月', '三月', '四月', '五月', '六月',
                       '七月', '八月', '九月', '十月', '冬月', '腊月']
        lunar_days = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                     '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                     '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
        
        month_str = lunar_months[lunar.month - 1]
        day_str = lunar_days[lunar.day - 1]
        
        if lunar.isleap:
            return f"闰{month_str}{day_str}"
        return f"{month_str}{day_str}"
    except Exception:
        return "农历转换失败"

def date_diff_days(year1, month1, day1, year2, month2, day2):
    """
    计算两个日期之间的天数差
    """
    date1 = datetime(year1, month1, day1)
    date2 = datetime(year2, month2, day2)
    return (date2 - date1).days

def validate_date(year, month, day):
    """
    验证日期是否合法
    """
    if not (1 <= year <= 9999):
        return False, "年份必须在1-9999之间"
    
    if not (1 <= month <= 12):
        return False, "月份必须在1-12之间"
    
    max_day = get_days_in_month(year, month)
    if not (1 <= day <= max_day):
        return False, f"该月的日期必须在1-{max_day}之间"
    
    return True, ""

def parse_and_validate_date(year_str, month_str, day_str):
    """
    日期解析和验证
    """
    if not year_str or not month_str or not day_str:
        return False, None, None, None, "年份、月份、日期都不能为空"
    
    year_str = str(year_str).strip()
    month_str = str(month_str).strip()
    day_str = str(day_str).strip()

    if not year_str or not month_str or not day_str:
        return False, None, None, None, "年份、月份、日期都不能为空"
 
    try:
        year = int(year_str)
        month = int(month_str)
        day = int(day_str)
    except ValueError:
        return False, None, None, None, "年份、月份、日期必须是整数"

    is_valid, error_msg = validate_date(year, month, day)
    if not is_valid:
        return False, None, None, None, error_msg
    
    return True, year, month, day, ""


def get_month_calendar(year, month):
    """
    生成指定年月的日历数据
    """
    first_day = get_weekday(year, month, 1)
    days_in_month = get_days_in_month(year, month)
    
    calendar = []
    week = []
    
    # 补第一周的空白
    for _ in range(first_day):
        week.append(0)
    
    # 主体
    for day in range(1, days_in_month + 1):
        week.append(day)
        if len(week) == 7:
            calendar.append(week)
            week = []
    
    # 补最后一周的空白
    if week:
        while len(week) < 7:
            week.append(0)
        calendar.append(week)
    
    return calendar