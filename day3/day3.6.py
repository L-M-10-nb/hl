import pandas as pd
import numpy as np

# 1. 创建CSV文件
# 创建包含指定列的DataFrame
data = {
    'Student_ID': [101, 102, 103, 104, 105, 106],
    'Name': ['Alice', 'Bob', 'Charlie', None, 'Eva', 'Frank'],
    'Score': [92, 85, None, 78, 90, 88],
    'Grade': ['A', 'B', 'C', 'C', 'A', 'B']
}

# 创建DataFrame
students_df = pd.DataFrame(data)

# 保存为CSV文件（创建原始数据文件）
students_df.to_csv('students.csv', index=False)
print("1. 已创建原始数据文件: students.csv")

# 2. 读取CSV文件并打印前3行
students = pd.read_csv('students.csv')
print("\n2. 前3行数据:")
print(students.head(3))

# 3. 填充缺失值
# 3.1 填充Score列缺失值为平均分
score_mean = students['Score'].mean()
students['Score'].fillna(score_mean, inplace=True)

# 3.2 填充Name列缺失值为"Unknown"
students['Name'].fillna("Unknown", inplace=True)

print("\n3. 填充缺失值后的数据:")
print(students)

# 4. 保存处理后的数据
students.to_csv('students_cleaned.csv', index=False)
print("\n4. 已保存清洗后数据: students_cleaned.csv")

# 5. 验证结果
print("\n最终数据统计:")
print(f"数据集行数: {len(students)}")
print(f"Score列缺失值: {students['Score'].isna().sum()}")
print(f"Name列缺失值: {students['Name'].isna().sum()}")
print(f"Score平均值: {score_mean:.2f}")