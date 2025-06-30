import pandas as pd

# 读取数据
data_path = r"C:\Users\Administrator\Desktop\drinks.csv"
df = pd.read_csv(data_path)

# 任务1：平均啤酒消耗最多的大洲
avg_beer = df.groupby('continent')['beer_servings'].mean().sort_values(ascending=False)
max_beer_continent = avg_beer.idxmax()
max_beer_value = avg_beer.max()

# 任务2：各洲红酒消耗描述性统计
wine_stats = df.groupby('continent')['wine_servings'].describe()

# 任务3：各洲每种酒的平均消耗
avg_consumption = df.groupby('continent').agg({
    'beer_servings': 'mean',
    'spirit_servings': 'mean',
    'wine_servings': 'mean'
}).round(2)

# 任务4：各洲每种酒的中位数消耗
median_consumption = df.groupby('continent').agg({
    'beer_servings': 'median',
    'spirit_servings': 'median',
    'wine_servings': 'median'
}).round(2)

# 输出结果
print("===== 数据分析结果 =====")
print("\n任务1：平均消耗啤酒最多的大洲")
print(f"大洲：{max_beer_continent}，平均消耗：{max_beer_value:.2f} 升/人")

print("\n任务2：各洲红酒消耗描述性统计")
print(wine_stats)

print("\n任务3：各洲每种酒的平均消耗量（升/人）")
print(avg_consumption)

print("\n任务4：各洲每种酒的中位数消耗量（升/人）")
print(median_consumption)