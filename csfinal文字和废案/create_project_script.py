"""
自动创建日历事件管理系统项目结构和文件
运行此脚本将在当前目录创建完整的项目

使用方法:
python create_project.py
"""

import os

# 项目结构
STRUCTURE = {
    'models': ['__init__.py', 'event.py', 'date_utils.py'],
    'storage': ['__init__.py', 'event_storage.py'],
    'ui': ['__init__.py', 'main_window.py', 'menu_view.py', 'calendar_view.py', 
           'date_query_view.py', 'event_manage_view.py'],
    'data': []
}

def create_directory_structure():
    """创建目录结构"""
    print("📁 创建项目目录结构...")
    
    for directory in STRUCTURE.keys():
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ 创建目录: {directory}/")
    
    print("\n✅ 目录结构创建完成！\n")


def create_requirements_txt():
    """创建 requirements.txt"""
    content = """lunarcalendar==0.0.9
tkcalendar==1.6.1
"""
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 创建文件: requirements.txt")


def create_readme():
    """创建 README.md"""
    content = """# 日历事件管理系统

## 功能特点

1. **月历打印**: 显示指定年月的日历，标记有事件的日期
2. **日期信息查询**: 查询任意日期的星期、农历、事件列表
3. **事件管理**: 添加、编辑、删除、搜索事件

## 支持的重复类型

- 单次事件
- 每日重复
- 每周重复
- 每月重复
- 每年重复
- 自定义间隔（每X天）

## 快速开始

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 运行程序:
```bash
python main.py
```

## 技术特点

- **高性能**: O(1)时间复杂度的事件查询算法
- **支持范围**: 公元1年到9999年
- **数据持久化**: JSON格式存储
- **模块化设计**: 易于维护和扩展

## 项目结构

```
calendar_system/
├── models/          # 数据模型
├── storage/         # 数据存储
├── ui/              # 用户界面
├── data/            # 数据文件
└── main.py          # 程序入口
```

## 系统要求

- Python 3.7+
- tkinter (通常随Python安装)
- 屏幕分辨率: 最小 1024x768

## 许可证

MIT License
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 创建文件: README.md")


def create_gitignore():
    """创建 .gitignore"""
    content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# 数据文件
data/*.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 系统文件
.DS_Store
Thumbs.db
"""
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 创建文件: .gitignore")


def create_placeholder_files():
    """创建占位文件"""
    print("\n📝 创建Python文件占位符...")
    
    for directory, files in STRUCTURE.items():
        for filename in files:
            filepath = os.path.join(directory, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f'"""\n{filename} - 待实现\n"""\n')
                print(f"  ✓ 创建文件: {filepath}")
    
    # 创建 main.py
    if not os.path.exists('main.py'):
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write('"""\nmain.py - 程序入口\n"""\n')
        print("  ✓ 创建文件: main.py")
    
    print("\n✅ 占位文件创建完成！")


def print_next_steps():
    """打印后续步骤"""
    print("\n" + "="*60)
    print("🎉 项目结构创建成功！")
    print("="*60)
    print("\n📋 后续步骤:\n")
    print("1. 从提供的代码artifacts中复制各个文件的完整代码")
    print("2. 创建虚拟环境:")
    print("   python -m venv venv")
    print("\n3. 激活虚拟环境:")
    print("   Windows: venv\\Scripts\\activate")
    print("   Mac/Linux: source venv/bin/activate")
    print("\n4. 安装依赖:")
    print("   pip install -r requirements.txt")
    print("\n5. 运行程序:")
    print("   python main.py")
    print("\n" + "="*60)
    print("\n📚 需要复制代码的文件列表:\n")
    
    files_to_copy = [
        "main.py",
        "models/__init__.py",
        "models/date_utils.py",
        "models/event.py",
        "storage/__init__.py",
        "storage/event_storage.py",
        "ui/__init__.py",
        "ui/main_window.py",
        "ui/menu_view.py",
        "ui/calendar_view.py",
        "ui/date_query_view.py",
        "ui/event_manage_view.py"
    ]
    
    for file in files_to_copy:
        print(f"  [ ] {file}")
    
    print("\n💡 提示: 可以在VS Code中直接打开这些文件进行编辑")
    print("="*60 + "\n")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  日历事件管理系统 - 项目创建工具")
    print("="*60 + "\n")
    
    # 创建目录结构
    create_directory_structure()
    
    # 创建配置文件
    print("📄 创建配置文件...\n")
    create_requirements_txt()
    create_readme()
    create_gitignore()
    
    # 创建占位文件
    create_placeholder_files()
    
    # 打印后续步骤
    print_next_steps()


if __name__ == "__main__":
    main()