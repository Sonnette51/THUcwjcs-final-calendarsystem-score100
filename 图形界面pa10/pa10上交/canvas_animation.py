import tkinter as tk

root = tk.Tk()
root.title("Canvas动画作业")
root.geometry("600x400")

# 创建画布
canvas = tk.Canvas(root, width=600, height=400, bg="lightblue")
canvas.pack()

# 绘制静态背景
# 地面
canvas.create_rectangle(0, 300, 600, 400, fill="#639681", outline="")

# 太阳
canvas.create_oval(450, 50, 520, 120, fill="#DEDA5C", outline="#ED9507", width=2)

# 房子
canvas.create_rectangle(80, 220, 180, 300, fill="#5555F0", outline="#0E2F76")
canvas.create_polygon(80, 220, 130, 180, 180, 220, fill="#EA85DD", outline="#A42172")

# 树
canvas.create_rectangle(500, 250, 520, 300, fill="#884E1E", outline="")
canvas.create_oval(480, 210, 540, 260, fill="#1B6444", outline="")

# 学号和姓名
canvas.create_text(300, 30, text="学号：2025013092  姓名：楼诗雨", 
                   font=("Times New Roman", 12), fill="#2F1D67")

# 绘制小汽车
# 车身
car_body = canvas.create_rectangle(50, 250, 120, 280, fill="#12412D", outline="black")

# 车顶
car_roof = canvas.create_rectangle(65, 230, 105, 250, fill="#39CC8F", outline="#1E4E3A")

# 左轮
left_wheel = canvas.create_oval(60, 275, 80, 295, fill="#E0EBE6", outline="gray")

# 右轮
right_wheel = canvas.create_oval(90, 275, 110, 295, fill="#99D8BE", outline="gray")

car_parts = [car_body, car_roof, left_wheel, right_wheel]

# 汽车移动方向
car_direction = 1

# 绘制云朵
# 云朵1
cloud1_parts = []
cloud1_parts.append(canvas.create_oval(100, 80, 140, 110, fill="white", outline="lightgray"))
cloud1_parts.append(canvas.create_oval(120, 70, 160, 100, fill="white", outline="lightgray"))
cloud1_parts.append(canvas.create_oval(140, 80, 180, 110, fill="white", outline="lightgray"))

# 云朵2
cloud2_parts = []
cloud2_parts.append(canvas.create_oval(300, 100, 340, 130, fill="white", outline="lightgray"))
cloud2_parts.append(canvas.create_oval(320, 90, 360, 120, fill="white", outline="lightgray"))
cloud2_parts.append(canvas.create_oval(340, 100, 380, 130, fill="white", outline="lightgray"))

# 汽车动画函数（带往返运动）
def move_car():
    global car_direction
    
    coords = canvas.coords(car_body)
    x1 = coords[0]  # 左边界
    x2 = coords[2]  # 右边界
    
    # 检查是否到达边界
    if x2 >= 600:  
        car_direction = -1
    elif x1 <= 0: 
        car_direction = 1
    
    # 移动
    for part in car_parts:
        canvas.move(part, 5 * car_direction, 0)
    
    # 动画
    root.after(50, move_car)

# 云朵动画函数
def move_clouds():
    coords1 = canvas.coords(cloud1_parts[0])
    if coords1[2] < 600:  # 如果云朵还在画布内
        for part in cloud1_parts:
            canvas.move(part, 0.5, 0) 
    else:  # 云朵移出画布，重新从左侧开始
        for part in cloud1_parts:
            canvas.move(part, -700, 0)
    
    coords2 = canvas.coords(cloud2_parts[0])
    if coords2[2] < 600:
        for part in cloud2_parts:
            canvas.move(part, 0.3, 0)  
    else:
        for part in cloud2_parts:
            canvas.move(part, -700, 0)
    
    root.after(100, move_clouds)

# 鼠标点击事件（点击画布，汽车瞬移到鼠标位置）
def on_click(event):
    current_coords = canvas.coords(car_body)
    current_x = current_coords[0]
    current_y = current_coords[1]
    
    # 计算移动距离：车中心点移动到鼠标
    dx = event.x - current_x - 35  
    dy = event.y - current_y - 15  
    
    # 移动
    for part in car_parts:
        canvas.move(part, dx, dy)

canvas.bind("<Button-1>", on_click)


move_car()
move_clouds()
root.mainloop()