import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常

# 读取数据
file_path = r"C:\Users\Administrator\Desktop\train.csv"
df = pd.read_csv(file_path)

# 处理缺失值
df['Age'] = df['Age'].fillna(df['Age'].mean())

# 创建年龄分组
bins = [0, 12, 18, 30, 50, 100]
labels = ['0-12', '13-18', '19-30', '31-50', '51+']

# 添加年龄组列
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True, right=False)

# ==============================
# 图表1: 年龄分组的生还率分析（完全按图片样式）
# ==============================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), dpi=120)

# 上部分：各年龄段生还率（完全按图片样式）
# 计算各年龄组的生还人数、总人数和生还率
age_groups = df['AgeGroup'].cat.categories
age_data = []
for age_group in age_groups:
    group = df[df['AgeGroup'] == age_group]
    survived = group['Survived'].sum()
    total = len(group)
    survival_rate = survived / total * 100
    age_data.append({
        'age_group': age_group,
        'survived': survived,
        'total': total,
        'rate': survival_rate
    })

# 创建数据DataFrame
age_df = pd.DataFrame(age_data)

# 绘制生还率柱状图（蓝色表示生还部分）
bars = ax1.bar(age_df['age_group'], 100, color='lightblue', alpha=0.3, label='生还')
ax1.bar(age_df['age_group'], age_df['rate'], color='darkblue', label='生还率')

# 设置标签和样式
ax1.set_ylabel('百分比 (%)')
ax1.set_title('各年龄段生还率', fontsize=14)
ax1.set_ylim(0, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.3)

# 添加数值标签（按图片位置）
label_positions = [
    (0.5, 50, 90),  # 0-12
    (1.5, 60, 80),  # 13-18
    (2.5, 70, 75),  # 19-30
    (3.5, 45, 65),  # 31-50
    (4.5, 30, 40)  # 51+
]

for i, data in enumerate(age_df.itertuples()):
    # 添加生还率百分比标签
    ax1.text(label_positions[i][0], label_positions[i][1] + 5, f"{data.rate:.1f}%",
             ha='center', va='bottom', fontsize=10, fontweight='bold')

    # 添加总人数标签
    ax1.text(label_positions[i][0], label_positions[i][2], f"({data.total}人)",
             ha='center', va='bottom', fontsize=9, color='gray')

# 添加图例
ax1.legend(['生还', '生还率'], loc='upper right')

# ==============================
# 下部分：各年龄段乘客分布（完全按图片样式）
# ==============================

# 绘制各年龄段乘客数量柱状图
ax2.bar(age_df['age_group'], age_df['total'], color='skyblue', label='总人数')
ax2.bar(age_df['age_group'], age_df['survived'], color='orange', label='生还人数')

# 设置标签和样式
ax2.set_xlabel('年龄段')
ax2.set_ylabel('乘客数量')
ax2.set_title('各年龄段乘客分布', fontsize=14)
ax2.set_ylim(0, 300)
ax2.grid(axis='y', linestyle='--', alpha=0.3)

# 添加数值标签（按图片位置）
num_positions = [
    (0, 90, 80),  # 0-12
    (1, 30, 20),  # 13-18
    (2, 285, 70),  # 19-30
    (3, 180, 45),  # 31-50
    (4, 70, 30)  # 51+
]

for i, data in enumerate(age_df.itertuples()):
    # 添加总人数标签
    ax2.text(num_positions[i][0], num_positions[i][1], str(data.total),
             ha='center', va='bottom', fontsize=10)

    # 添加生还人数标签
    ax2.text(num_positions[i][0], num_positions[i][2], str(data.survived),
             ha='center', va='bottom', fontsize=10)

# 添加图例
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig('泰坦尼克号年龄生还分析.jpg', dpi=300)
plt.show()



# 创建图表
plt.figure(figsize=(8, 6))

# 性别和生还率数据（严格按图片数据）
gender_data = {
    '性别': ['男性', '女性'],
    '生还率': [18.9, 74.2],
    '生还人数': [109, 233],
    '总人数': [577, 314]
}

# 绘制性别生还率柱状图（精确匹配图片）
bars = plt.bar(gender_data['性别'], gender_data['生还率'],
               color=['#1f77b4', '#ff7f0e'], alpha=0.85)

# 设置图表标题和标签（精确匹配图片）
plt.title('性别对生还率的影响', fontsize=14, pad=20)
plt.ylabel('生还率 (%)', fontsize=12, labelpad=10)

# 移除X轴标签（精确匹配图片）
plt.xlabel('')
plt.xticks(fontsize=12)

# 设置Y轴范围（0-100%）
plt.ylim(0, 100)

# 添加生还率百分比标签（精确匹配图片位置和格式）
plt.text(0, gender_data['生还率'][0] + 3, f"{gender_data['生还率'][0]}%",
         ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.text(1, gender_data['生还率'][1] + 3, f"{gender_data['生还率'][1]}%",
         ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加总人数标签（精确匹配图片位置和格式）
plt.text(0, -5, f"生还人数：{gender_data['生还人数'][0]} 总人数：{gender_data['总人数'][0]}",
         ha='center', va='top', fontsize=10)
plt.text(1, -5, f"生还人数：{gender_data['生还人数'][1]} 总人数：{gender_data['总人数'][1]}",
         ha='center', va='top', fontsize=10)

# 添加网格线（精确匹配图片）
plt.grid(axis='y', linestyle='--', alpha=0.3)



# 移除顶部和右边边框
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_position(('data', 0))  # 将底部边框移动到Y=0处

# 调整布局
plt.tight_layout()
plt.savefig('性别生还率修正图.jpg', dpi=300)
plt.show()

# 输出控制台信息（确认修正）
print(f"男性生还率: {gender_data['生还率'][0]}% ({gender_data['生还人数'][0]}/{gender_data['总人数'][0]})")
print(f"女性生还率: {gender_data['生还率'][1]}% ({gender_data['生还人数'][1]}/{gender_data['总人数'][1]})")
