year = int(input())
def is_runyear(y):
    return (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0)
base_weekday = 0

def days_before_year(y):
    d = 0
    for yy in range(1998, y):
        d += 366 if is_runyear(yy) else 365
    return d

monthday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

count = 0
base_days = days_before_year(year)
for m in range(1, 13):
    md = monthday[:]
    if is_runyear(year):
        md[1] = 29
    days_from_year_start = sum(md[:m-1]) + (13 - 1)
    total_days = base_days + days_from_year_start
    weekday = (base_weekday + total_days) % 7
    if weekday == 1:
        count += 1
print(count)


