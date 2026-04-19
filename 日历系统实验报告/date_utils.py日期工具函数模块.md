1. is_run_year(year)判断是否为闰年
2. get_days_in_month(year, month)获取指定年月的天数
3. get_weekday(year, month, day)计算星期几
    *返回: 0=周日, 1=周一, ..., 6=周六*
    **蔡勒公式** 时间复杂度为O(1)
4. get_weekday_name(year, month, day)获取星期几的中文名称
5. get_lunar_date(year, month, day)获取农历日期
    *返回: 农历日期字符串，如 "正月初一"*
6. date_diff_days(year1, month1, day1, year2, month2, day2)计算两个日期之间的天数差
7. validate_date(year, month, day)验证日期是否合法
    *返回: (is_valid, error_message)*
 8. get_month_calendar(year, month)生成指定年月的日历数据
    *返回: 二维列表，每行代表一周*

