import numpy as np
import matplotlib.pyplot as plt

# 创建从 -10 到 10 的 x 值数组
x = np.linspace(-10, 10, 400)  # 400个点

# 计算 y = x^3
y = x**3

# 创建图形
plt.figure(figsize=(8, 6))  # 设置图形大小

# 绘制曲线
plt.plot(x, y, 'b-', linewidth=2)  # 蓝色实线，线宽为2

# 添加标题和坐标轴标签
plt.title('$y = x^3$', fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)

# 添加网格线
plt.grid(True)

# 显示图形
plt.show()