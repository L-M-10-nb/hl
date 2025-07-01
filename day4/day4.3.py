import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 从CSV文件读取数据
file_path = r"C:\Users\Administrator\Desktop\train.csv"
df = pd.read_csv(file_path)

# 筛选数据 - 使用与图片相同的逻辑
df_sex1 = df['Pclass'][df['Survived'] == 1]  # 生还
df_sex0 = df['Pclass'][df['Survived'] == 0]  # 遇难

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制堆叠直方图 - 严格按照图片中的样式
plt.hist([df_sex1, df_sex0],
         stacked=True,
         bins=[0.5, 1.5, 2.5, 3.5],  # 精确控制每个仓位的分界
         label=['Rescued', 'Not saved'],
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
plt.xticks([1, 2, 3], ['Upper (1st)', 'Middle (2nd)', 'Lower (3rd)'], fontsize=12)
plt.yticks(np.arange(0, 501, 50))
plt.xlabel('Passenger Class', fontsize=12)
plt.ylabel('Number of Passengers', fontsize=12)
plt.title('Survival Rate by Passenger Class', fontsize=14, fontweight='bold')

# 添加网格和图例
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.legend(loc='upper right')

# 添加数据标签说明
plt.text(1.5, 480,
         "1st Class Survival Rate: 63.0%\n2nd Class Survival Rate: 47.3%\n3rd Class Survival Rate: 24.2%",
         ha='center', fontsize=11, bbox=dict(facecolor='white', alpha=0.8))

# 调整布局
plt.tight_layout()
plt.savefig('titanic_survival_by_class_improved.png', dpi=120)
plt.show()

# 打印统计数据
print("\nPassenger Class Survival Statistics:")
print(f"1st Class: {len(df_sex1[df_sex1 == 1])}/{len(df[df['Pclass'] == 1])} survived (63.0%)")
print(f"2nd Class: {len(df_sex1[df_sex1 == 2])}/{len(df[df['Pclass'] == 2])} survived (47.3%)")
print(f"3rd Class: {len(df_sex1[df_sex1 == 3])}/{len(df[df['Pclass'] == 3])} survived (24.2%)")