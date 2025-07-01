import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常

# 读取数据
file_path = r"C:\Users\Administrator\Desktop\train.csv"
df = pd.read_csv(file_path)

# 乘客等级对生还率的影响（保留图片中的代码，改为中文显示）
plt.figure(figsize=(10, 6))

# 提取生还和遇难的乘客等级数据
df_sex1 = df['Pclass'][df['Survived'] == 1]  # 生还
df_sex0 = df['Pclass'][df['Survived'] == 0]  # 遇难

# 绘制堆叠直方图
plt.hist([df_sex1, df_sex0],
         stacked=True,
         bins=[0.5, 1.5, 2.5, 3.5],
         label=['获救', '未获救'],
         color=['#64B5CD', '#F4A460'])

# 计算每个仓位的生还率
for pclass in [1, 2, 3]:
    total = len(df[df['Pclass'] == pclass])
    survived = len(df[(df['Pclass'] == pclass) & (df['Survived'] == 1)])
    survival_rate = survived / total * 100

    # 在柱子上方添加生还率标注
    plt.text(pclass, total + 10, f'{survival_rate:.1f}%',
             ha='center', va='bottom', fontweight='bold')

# 设置轴标签和标题
plt.xticks([1, 2, 3], ['一等舱', '二等舱', '三等舱'])
plt.xlabel('乘客等级')
plt.ylabel('乘客数量')
plt.title('乘客等级对生还率的影响')
plt.legend()

plt.tight_layout()
plt.show()

# 分析哪个年龄段的生还率最高
plt.figure(figsize=(10, 6))

# 处理缺失值 - 用均值填充
mean_age = df['Age'].mean()
df['Age'] = df['Age'].fillna(mean_age)

# 划分年龄段
bins = [0, 18, 35, 60, 100]
labels = ['儿童少年(0-18)', '青年(19-35)', '中年(36-60)', '老年(60+)']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

# 按年龄段和生还情况分组统计人数
age_group_survived_counts = df.groupby(['AgeGroup', 'Survived']).size().unstack(fill_value=0)

# 计算每个年龄段的生还率
age_group_survived_counts['生还率'] = age_group_survived_counts[1] / (
            age_group_survived_counts[0] + age_group_survived_counts[1]) * 100

# 找出生还率最高的年龄段
highest_survival_rate_age_group = age_group_survived_counts['生还率'].idxmax()
highest_survival_rate = age_group_survived_counts.loc[highest_survival_rate_age_group, '生还率']

# 绘制年龄段生还率直方图（柱状图）
age_group_survived_counts['生还率'].plot(kind='bar',
                                         color='#4E96A9',
                                         alpha=0.8,
                                         edgecolor='black',
                                         width=0.7)

# 添加数据和结论
for i, rate in enumerate(age_group_survived_counts['生还率']):
    plt.text(i, rate + 2, f'{rate:.1f}%', ha='center', va='bottom', fontsize=10)

# 在顶部添加结论
plt.text(1.5, 70,
         f"生还率最高的年龄段: {highest_survival_rate_age_group} ({highest_survival_rate:.1f}%)",
         ha='center', fontsize=12, fontweight='bold',
         bbox=dict(facecolor='yellow', alpha=0.3, edgecolor='gray'))

# 设置标签和标题
plt.xlabel('年龄段')
plt.ylabel('生还率 (%)')
plt.title('不同年龄段乘客的生还率')
plt.xticks(rotation=0)  # 水平显示标签
plt.ylim(0, 80)  # 设置Y轴范围

plt.tight_layout()
plt.show()

# 输出各年龄段生还率
print("\n各年龄段生还率统计:")
print(age_group_survived_counts[['生还率']])
print(f"\n生还率最高的年龄段: {highest_survival_rate_age_group} ({highest_survival_rate:.1f}%)")