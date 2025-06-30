import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # 正确导入日期格式化模块
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import random

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
plt.grid(True)
plt.show()



# ================== 1. 生成随机销售数据 ================== #
np.random.seed(42)
random.seed(42)

# 生成2024年1月的数据
data_list = []
start_date = datetime(2024, 1, 1)

# 创建30天的销售数据
for i in range(30):
    # 考虑周末效应
    is_weekend = (start_date + timedelta(days=i)).weekday() in [5, 6]

    # 基础销售趋势 + 周末效应 + 随机波动
    base_sales = 100 + i * 5
    weekend_boost = 50 if is_weekend else 0
    noise = random.randint(-20, 20)

    sales = max(50, int(base_sales + weekend_boost + noise))

    data_list.append({
        'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
        'sales': sales
    })

# ================== 2. 创建DataFrame ================== #
sales_df = pd.DataFrame(data_list)
sales_df['date'] = pd.to_datetime(sales_df['date'])
sales_df.set_index('date', inplace=True)

# ================== 3. 可视化销售数据 ================== #
# 设置中文字体（Windows系统）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建图表
fig, ax = plt.subplots(figsize=(12, 6))

# 1. 绘制销量折线图
ax.plot(sales_df.index, sales_df['sales'],
        marker='o', markersize=6,
        linestyle='-', color='#1f77b4',
        linewidth=2, label='每日销量')

# 2. 添加7日移动平均线
sales_df['7d_avg'] = sales_df['sales'].rolling(window=7).mean()
ax.plot(sales_df.index, sales_df['7d_avg'],
        linestyle='--', color='#ff7f0e',
        linewidth=2.5, label='7日移动平均线')

# 3. 标记最高点和最低点
max_sales = sales_df['sales'].max()
min_sales = sales_df['sales'].min()
max_date = sales_df['sales'].idxmax()
min_date = sales_df['sales'].idxmin()

ax.scatter(max_date, max_sales,
           color='red', s=100,
           label=f'最高销量 ({max_sales})')
ax.scatter(min_date, min_sales,
           color='green', s=100,
           label=f'最低销量 ({min_sales})')

# 4. 设置日期刻度格式（修正部分）
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 正确使用mdates
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))  # 每周显示一个刻度

# 5. 设置其他图表元素
ax.set_title('2024年1月销售趋势分析', fontsize=16, pad=20)
ax.set_xlabel('日期', fontsize=12, labelpad=10)
ax.set_ylabel('销量', fontsize=12, labelpad=10)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.3)

# 6. 调整布局并保存
plt.tight_layout()
plt.savefig('sales_trend.png', dpi=300)
print("图表已保存为: sales_trend.png")

# 7. 显示图表
plt.show()

# 添加数据分析报告
print("\n销售数据分析报告:")
print(f"统计周期: {sales_df.index[0].strftime('%Y-%m-%d')} 至 {sales_df.index[-1].strftime('%Y-%m-%d')}")
print(f"总销量: {sales_df['sales'].sum()}")
print(f"平均日销量: {sales_df['sales'].mean():.1f} ± {sales_df['sales'].std():.1f}")
print(f"最高销量: {max_sales} (出现在 {max_date.strftime('%m-%d')})")
print(f"最低销量: {min_sales} (出现在 {min_date.strftime('%m-%d')})")