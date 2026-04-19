# 日历事件管理系统 - 完整设置指南

## 📁 项目结构

```
calendar_system/
│
├── main.py                    # 主程序入口
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目说明
│
├── models/                    # 数据模型层
│   ├── __init__.py
│   ├── event.py              # 事件类定义
│   └── date_utils.py         # 日期工具函数
│
├── storage/                   # 数据持久化层
│   ├── __init__.py
│   └── event_storage.py      # 事件存储管理
│
├── ui/                        # 界面层
│   ├── __init__.py
│   ├── main_window.py        # 主窗口
│   ├── menu_view.py          # 主菜单视图
│   ├── calendar_view.py      # 月历打印视图
│   ├── date_query_view.py    # 日期查询视图
│   └── event_manage_view.py  # 事件管理视图
│
└── data/                      # 数据文件目录
    └── events.json           # 事件数据文件（自动生成）
```

## 🚀 快速开始

### 1. 创建项目目录

```bash
# Windows
mkdir calendar_system
cd calendar_system

# Mac/Linux
mkdir calendar_system
cd calendar_system
```

### 2. 创建子目录

```bash
# Windows
mkdir models storage ui data

# Mac/Linux
mkdir models storage ui data
```

### 3. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. 创建 requirements.txt

在项目根目录创建 `requirements.txt` 文件，内容：

```
lunarcalendar==0.0.9
tkcalendar==1.6.1
```

### 5. 安装依赖

```bash
pip install -r requirements.txt
```

### 6. 创建所有Python文件

按照以下顺序创建文件（可以从我提供的代码artifacts中复制）：

#### 6.1 models/ 目录
- `models/__init__.py`
- `models/date_utils.py`
- `models/event.py`

#### 6.2 storage/ 目录
- `storage/__init__.py`
- `storage/event_storage.py`

#### 6.3 ui/ 目录
- `ui/__init__.py`
- `ui/main_window.py`
- `ui/menu_view.py`
- `ui/calendar_view.py`
- `ui/date_query_view.py`
- `ui/event_manage_view.py`

#### 6.4 根目录
- `main.py`

### 7. 运行程序

```bash
python main.py
```

## 💻 在VS Code中设置

### 1. 打开项目

```
File -> Open Folder -> 选择 calendar_system 文件夹
```

### 2. 选择Python解释器

```
Ctrl+Shift+P (Windows/Linux) 或 Cmd+Shift+P (Mac)
输入: Python: Select Interpreter
选择: calendar_system/venv/bin/python (或 venv\Scripts\python.exe)
```

### 3. 安装推荐扩展

- Python (Microsoft)
- Python Debugger
- Pylance

### 4. 创建launch.json（调试配置）

在 `.vscode/launch.json` 中添加：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Run Calendar System",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### 5. 运行和调试

- 运行: 按 `F5` 或点击 "Run and Debug"
- 设置断点: 点击行号左侧
- 查看变量: 调试时在 "Variables" 面板查看

## 📝 使用说明

### 功能1: 月历打印

1. 在主菜单点击 "📅 月历打印"
2. 输入年份和月份
3. 查看日历（有事件的日期会标记 ●）
4. 点击任意日期可跳转到日期查询

### 功能2: 日期信息查询

1. 在主菜单点击 "🔍 日期信息查询"
2. 输入年、月、日
3. 点击 "查询" 查看：
   - 星期几
   - 农历日期
   - 当天所有事件
4. 可以直接编辑或删除事件

### 功能3: 事件管理

1. 在主菜单点击 "📝 事件管理"
2. 点击 "➕ 添加事件" 创建新事件：
   - 填写事件名称（必填）
   - 填写描述（可选）
   - 选择开始日期
   - 选择重复类型：
     - 单次事件
     - 每日重复
     - 每周重复
     - 每月重复
     - 每年重复
     - 自定义间隔（每X天）
   - 设置重复次数或选择无限重复
   - 可以标星标记重要事件
3. 双击事件可编辑
4. 右键事件显示更多操作
5. 使用搜索框查找事件

## 🔧 常见问题

### Q: 提示找不到模块？
A: 确保虚拟环境已激活，并且运行了 `pip install -r requirements.txt`

### Q: 农历转换不准确？
A: 当前使用简化算法，建议使用 lunarcalendar 库（已包含在依赖中）

### Q: 窗口显示不正常？
A: 检查屏幕分辨率，建议最小 1024x768

### Q: 数据保存在哪里？
A: 保存在 `data/events.json` 文件中

### Q: 如何备份数据？
A: 复制 `data/events.json` 文件即可

## 🎯 性能测试

测试添加以下事件类型：

1. **单次事件**: 100个
2. **每日重复**: 重复10000次
3. **每年重复**: 跨越5000年

查询任意日期，响应时间应该 < 100ms

## 📊 项目特点

### 1. 高性能算法

```python
# O(1) 时间复杂度判断事件是否发生
def occurs_on_date(self, target_year, target_month, target_day):
    days_diff = date_diff_days(...)  # 直接计算天数差
    
    if self.repeat_type == RepeatType.WEEKLY:
        return days_diff % 7 == 0  # 数学计算，不遍历
```

### 2. 边界情况处理

- 每月重复：1月31日 → 2月28/29日
- 每年重复：闰年2月29日 → 平年2月28日

### 3. 模块化设计

- **models**: 数据模型和业务逻辑
- **storage**: 数据持久化
- **ui**: 用户界面
- 低耦合，易维护

### 4. 数据持久化

- JSON格式存储
- 自动保存
- 易于备份和迁移

## 🎓 代码学习要点

### 1. 蔡勒公式（计算星期几）

```python
def get_weekday(year, month, day):
    # 1月和2月看作上一年的13月和14月
    if month < 3:
        month += 12
        year -= 1
    
    c = year // 100
    yy = year % 100
    w = (yy + yy // 4 + c // 4 - 2 * c + 
         (26 * (month + 1)) // 10 + day - 1) % 7
    return (w + 7) % 7
```

### 2. 事件重复算法

```python
# 每周重复：判断天数差是否是7的倍数
if days_diff % 7 != 0:
    return False

# 每月重复：计算月份差
months_diff = (target_year - start_year) * 12 + (target_month - start_month)
```

### 3. Tkinter界面设计

```python
# 使用多视图管理
self.views = {
    'menu': MenuView(...),
    'calendar': CalendarView(...),
    # ...
}

# 切换视图
def show_view(self, name):
    self.views[name].lift()
```

## 📚 扩展建议

1. **导出功能**: 导出事件为iCal格式
2. **提醒功能**: 添加事件提醒通知
3. **节假日**: 集成中国法定节假日
4. **主题**: 支持深色/浅色主题切换
5. **云同步**: 支持多设备同步

## 🐛 调试技巧

### 1. 打印调试信息

```python
print(f"Debug: year={year}, month={month}, day={day}")
```

### 2. 使用logging模块

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("事件查询开始")
```

### 3. VS Code断点调试

- F9: 设置/取消断点
- F5: 开始调试
- F10: 单步跳过
- F11: 单步进入

## 📄 许可证

MIT License

## 👨‍💻 联系方式

如有问题，请联系开发者。

---

**祝你使用愉快！** 🎉