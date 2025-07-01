import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 设置中文字体，确保中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 读取数据
file_path = r"C:\Users\Administrator\Desktop\合并后的城市数据.csv"
df = pd.read_csv(file_path, encoding='utf-8')



# 任务1: 绘制2015-2017年各城市GDP柱状图
plt.figure(figsize=(18, 10), dpi=100)

# 创建年份筛选器
years = [2015, 2016, 2017]
filtered_df = df[df['年份'].isin(years)]

# 创建分组柱状图
pivot_df = filtered_df.pivot(index='地区', columns='年份', values='国内生产总值')
ax = pivot_df.plot(kind='bar', width=0.8, figsize=(18, 10))

# 设置图表格式
plt.title('2015-2017年各城市国内生产总值对比', fontsize=18)
plt.xlabel('城市', fontsize=14)
plt.ylabel('国内生产总值 (亿元)', fontsize=14)
plt.xticks(rotation=75, ha='right', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 设置Y轴格式 - 千分位分隔符
formatter = FuncFormatter(lambda x, p: format(int(x), ','))
ax.yaxis.set_major_formatter(formatter)

# 添加图例
plt.legend(title='年份', bbox_to_anchor=(1.02, 1), loc='upper left')

# 自动调整布局
plt.tight_layout()
plt.savefig('城市GDP柱状图.png', dpi=300, bbox_inches='tight')
plt.show()

# 提取2015年数据并按GDP降序排序
df_2015 = df[df['年份'] == 2015].sort_values('国内生产总值', ascending=False)

# 确保城市名是字符串类型
df_2015['地区'] = df_2015['地区'].astype(str)

# 创建饼图
plt.figure(figsize=(14, 12), dpi=100)  # 设置合适的大小

# 绘制标准饼图（无中心空白）
wedges, texts, autotexts = plt.pie(
    df_2015['国内生产总值'],
    labels=df_2015['地区'],
    autopct=lambda p: f'{p:.1f}%',
    startangle=140,
    pctdistance=0.8,
    textprops={'fontsize': 8}
)

# 设置标题
plt.title('2015年各城市国内生产总值分布', fontsize=16)

# 设置标签和百分比文字的样式
plt.setp(texts, fontsize=9)
plt.setp(autotexts, size=8, weight='bold', color='white')

# 添加图例显示GDP值（可选，如果不想要可以删除这部分）
legend_labels = [f'{region} ({gdp:.0f}亿)'
                for region, gdp in zip(df_2015['地区'], df_2015['国内生产总值'])]
plt.legend(wedges, legend_labels,
           title="城市GDP (亿元)",
           loc="center left",
           bbox_to_anchor=(1, 0, 0.5, 1),
           fontsize=8,
           title_fontsize=9)

# 调整布局确保所有元素可见
plt.tight_layout()

# 保存为JPG格式
plt.savefig('2015年各城市GDP饼图.jpg', format='jpg', dpi=300, bbox_inches='tight')
print("饼图已保存为：2015年各城市GDP饼图.jpg")

# 显示图表
plt.show()