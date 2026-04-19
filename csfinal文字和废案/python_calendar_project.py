# 项目结构说明
"""
calendar_system/
│
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
│
├── models/                 # 数据模型层
│   ├── __init__.py
│   ├── event.py           # 事件类定义
│   └── date_utils.py      # 日期工具函数
│
├── storage/               # 数据持久化层
│   ├── __init__.py
│   └── event_storage.py   # 事件存储管理
│
├── ui/                    # 界面层
│   ├── __init__.py
│   ├── main_window.py     # 主窗口
│   ├── menu_view.py       # 主菜单视图
│   ├── calendar_view.py   # 月历打印视图
│   ├── date_query_view.py # 日期查询视图
│   └── event_manage_view.py # 事件管理视图
│
└── data/                  # 数据文件目录
    └── events.json        # 事件数据文件（自动生成）

"""

# 在VS Code中的设置步骤：
"""
1. 创建项目文件夹：
   mkdir calendar_system
   cd calendar_system

2. 创建虚拟环境：
   python -m venv venv
   
3. 激活虚拟环境：
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

4. 安装依赖：
   pip install -r requirements.txt

5. 运行程序：
   python main.py

6. VS Code设置：
   - 打开文件夹: File -> Open Folder -> 选择 calendar_system
   - 选择Python解释器: Ctrl+Shift+P -> Python: Select Interpreter -> 选择 venv
   - 安装Python扩展: 搜索 "Python" by Microsoft
"""