import numpy as np
import matplotlib.pyplot as plt

# 国家数据
countries = ['挪威', '德国', '中国', '美国', '瑞典']

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 奖牌数据
gold_medal = np.array([16, 12, 9, 8, 8])
silver_medal = np.array([8, 10, 4, 10, 5])
bronze_medal = np.array([13, 5, 2, 7, 5])

# 设置画布
plt.figure(figsize=(10, 6), dpi=100)

# 生成坐标位置
x = np.arange(len(countries))
plt.xticks(x, countries)

# 绘制分组柱状图（修正参数名称，添加label）
plt.bar(x - 0.2, gold_medal, width=0.2, color="gold", label="金牌")
plt.bar(x, silver_medal, width=0.2, color="silver", label="银牌")
plt.bar(x + 0.2, bronze_medal, width=0.2, color="saddlebrown", label="铜牌")

# 添加数据标签
for i in range(len(countries)):
    # 金牌标签（修正坐标位置）
    plt.text(i - 0.2, gold_medal[i] + 0.2, str(gold_medal[i]),
             va='bottom', ha='center', fontsize=9)
    # 银牌标签
    plt.text(i, silver_medal[i] + 0.2, str(silver_medal[i]),
             va='bottom', ha='center', fontsize=9)
    # 铜牌标签
    plt.text(i + 0.2, bronze_medal[i] + 0.2, str(bronze_medal[i]),
             va='bottom', ha='center', fontsize=9)

# 添加标题和标签（原图缺失，补充必要信息）
plt.title("2022冬奥会奖牌统计", fontsize=14)
plt.xlabel("参赛国家", fontsize=12)
plt.ylabel("奖牌数量", fontsize=12)
plt.legend(loc='upper right')  # 添加图例

# 优化布局
plt.tight_layout()
plt.grid(axis='y', alpha=0.4)  # 添加横向网格线

# 显示图表
plt.show()