# 📋 文件复制清单和操作步骤

## 第一步：创建项目结构

### 选项A：使用自动脚本（推荐）

1. 复制 `create_project.py` 脚本到你想创建项目的目录
2. 运行脚本：
   ```bash
   python create_project.py
   ```
3. 脚本会自动创建所有目录和占位文件

### 选项B：手动创建

在你的工作目录中手动创建以下结构：

```
calendar_system/
├── models/
├── storage/
├── ui/
└── data/
```

---

## 第二步：复制文件内容

按照以下顺序复制代码（每个文件对应一个artifact）：

### ✅ 配置文件

- [ ] **requirements.txt**
  - 内容：lunarcalendar和tkcalendar
  - 用途：Python依赖包列表

---

### ✅ models/ 目录（数据模型层）

- [ ] **models/\_\_init\_\_.py**
  - 从 artifact "\_\_init\_\_.py 文件集合" 中复制

- [ ] **models/date_utils.py**
  - 从 artifact "models/date_utils.py - 日期工具函数" 中复制
  - 包含：
    - 闰年判断
    - 蔡勒公式（计算星期几）
    - 农历转换
    - 日期验证
    - 月历生成

- [ ] **models/event.py**
  - 从 artifact "models/event.py - 事件类定义" 中复制
  - 包含：
    - Event类定义
    - RepeatType常量
    - **核心算法**: `occurs_on_date()` 方法

---

### ✅ storage/ 目录（数据持久化层）

- [ ] **storage/\_\_init\_\_.py**
  - 从 artifact "\_\_init\_\_.py 文件集合" 中复制

- [ ] **storage/event_storage.py**
  - 从 artifact "storage/event_storage.py - 事件存储管理" 中复制
  - 包含：
    - EventStorage类
    - JSON读写
    - 事件CRUD操作

---

### ✅ ui/ 目录（用户界面层）

- [ ] **ui/\_\_init\_\_.py**
  - 从 artifact "\_\_init\_\_.py 文件集合" 中复制

- [ ] **ui/main_window.py**
  - 从 artifact "ui/main_window.py - 主窗口" 中复制
  - 包含：
    - MainWindow类（主控制器）
    - 视图管理
    - 样式设置

- [ ] **ui/menu_view.py**
  - 从 artifact "ui/menu_view.py - 主菜单视图" 中复制
  - 包含：主菜单界面

- [ ] **ui/calendar_view.py**
  - 从 artifact "ui/calendar_view.py - 月历打印视图" 中复制
  - 包含：
    - 月历显示
    - 月份切换
    - 事件标记

- [ ] **ui/date_query_view.py**
  - 从 artifact "ui/date_query_view.py - 日期查询视图" 中复制
  - 包含：
    - 日期查询
    - 星期/农历显示
    - 事件列表

- [ ] **ui/event_manage_view.py**
  - 从 artifact "ui/event_manage_view.py - 事件管理视图" 中复制
  - 包含：
    - 事件列表（Treeview）
    - 添加/编辑对话框
    - 搜索功能

---

### ✅ 根目录

- [ ] **main.py**
  - 从 artifact "main.py - 程序入口" 中复制
  - 包含：程序入口点

---

## 第三步：设置Python环境

### 1. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

如果遇到问题，可以单独安装：

```bash
pip install lunarcalendar
pip install tkcalendar
```

---

## 第四步：在VS Code中打开项目

### 1. 打开文件夹

```
File -> Open Folder -> 选择 calendar_system
```

### 2. 选择Python解释器

```
Ctrl+Shift+P (Windows) 或 Cmd+Shift+P (Mac)
输入: Python: Select Interpreter
选择: ./venv/bin/python
```

### 3. 验证项目结构

在VS Code的资源管理器中，应该看到：

```
CALENDAR_SYSTEM
├── 📁 models
│   ├── __init__.py
│   ├── date_utils.py
│   └── event.py
├── 📁 storage
│   ├── __init__.py
│   └── event_storage.py
├── 📁 ui
│   ├── __init__.py
│   ├── main_window.py
│   ├── menu_view.py
│   ├── calendar_view.py
│   ├── date_query_view.py
│   └── event_manage_view.py
├── 📁 data (空目录)
├── 📁 venv (虚拟环境)
├── main.py
└── requirements.txt
```

---

## 第五步：运行程序

### 方法1：命令行运行

```bash
python main.py
```

### 方法2：VS Code运行

1. 打开 `main.py`
2. 按 `F5` 或点击右上角的运行按钮
3. 选择 "Python File"

### 方法3：创建启动配置

创建 `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "运行日历系统",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

---

## 🧪 测试项目

### 1. 基本功能测试

- [ ] 启动程序，显示主菜单
- [ ] 进入月历打印，显示当前月份日历
- [ ] 切换到不同年月
- [ ] 进入日期查询，输入日期查看信息
- [ ] 进入事件管理，添加测试事件

### 2. 事件测试

添加以下测试事件：

- [ ] 单次事件：2025年1月1日
- [ ] 每日重复：从今天开始，重复7次
- [ ] 每周重复：每周一，无限重复
- [ ] 每月重复：每月15日，重复12次
- [ ] 每年重复：每年5月20日
- [ ] 自定义：每3天重复一次

### 3. 边界测试

- [ ] 测试闰年：2024年2月29日
- [ ] 测试月末：1月31日的月重复（查看2月是否显示在28/29日）
- [ ] 测试极端日期：公元1年1月1日、9999年12月31日

### 4. 性能测试

- [ ] 添加100个基础事件
- [ ] 添加重复10000次的事件
- [ ] 查询任意日期，检查响应速度（应该<100ms）

---

## 🐛 常见问题排查

### 问题1：ModuleNotFoundError

**症状**：`ModuleNotFoundError: No module named 'lunarcalendar'`

**解决**：
```bash
# 确保虚拟环境已激活
pip install lunarcalendar tkcalendar
```

### 问题2：tkinter未安装

**症状**：`ImportError: No module named '_tkinter'`

**解决**：
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/Fedora
sudo yum install python3-tkinter

# Mac (通常已安装)
brew install python-tk
```

### 问题3：文件编码问题

**症状**：中文显示乱码

**解决**：确保所有Python文件使用UTF-8编码

在VS Code中：
- 右下角点击编码
- 选择 "UTF-8"
- 选择 "Save with Encoding"

### 问题4：相对导入错误

**症状**：`ImportError: attempted relative import with no known parent package`

**解决**：确保从项目根目录运行：
```bash
cd calendar_system
python main.py
```

---

## 📚 额外资源

### 代码说明文档

参考 artifact "项目设置和运行指南" 了解：
- 详细功能说明
- 算法实现原理
- 代码学习要点

### 性能优化说明

核心算法在 `models/event.py` 的 `occurs_on_date()` 方法中：
- 使用数学计算代替循环遍历
- O(1)时间复杂度
- 支持跨越数千年的重复事件

### 扩展开发建议

1. **导出功能**：添加iCal格式导出
2. **通知提醒**：集成系统通知
3. **主题切换**：深色/浅色模式
4. **云同步**：连接云存储服务
5. **移动端**：使用Kivy开发移动版本

---

## ✅ 完成检查清单

- [ ] 所有12个Python文件已创建并复制代码
- [ ] requirements.txt已创建
- [ ] 虚拟环境已创建并激活
- [ ] 依赖包已安装
- [ ] 程序可以正常启动
- [ ] 三大功能（月历、查询、管理）都可以使用
- [ ] 可以添加、编辑、删除事件
- [ ] 数据可以保存和加载

---

## 🎉 祝贺！

如果以上所有步骤都完成，你现在拥有一个完全功能的日历事件管理系统！

开始使用并享受高效的日程管理吧！