import pandas as pd
import os
import glob
import chardet
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 设置文件路径
base_dir = r"C:\Users\Administrator\Desktop"
files = glob.glob(os.path.join(base_dir, "*国内主要城市年度数据*.csv"))

# 1. 检测文件编码并读取数据
dfs = []
for file in files:
    try:
        # 检测文件编码
        with open(file, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        # 读取文件
        df = pd.read_csv(file, encoding=encoding)
        print(f"成功读取 {os.path.basename(file)}，编码: {encoding}")
        print(f"列名: {list(df.columns)}")
        dfs.append(df)
    except Exception as e:
        print(f"读取 {os.path.basename(file)} 时出错: {str(e)}")

# 2. 合并数据
if not dfs:
    print("没有读取到任何数据文件，请检查路径和文件格式")
    exit()

# 纵向连接数据
combined = pd.concat(dfs, ignore_index=True)

# 3. 标准化列名
# 寻找可能的年份列
possible_year_cols = [col for col in combined.columns if '年份' in col or '年' in col or '时间' in col]
# 寻找可能的GDP列
possible_gdp_cols = [col for col in combined.columns if '国内生产总值' in col or 'GDP' in col or '生产总值' in col]
# 寻找可能的社会商品零售总额列
possible_retail_cols = [col for col in combined.columns if
                        '社会商品零售总额' in col or '零售总额' in col or '消费品零售' in col]
# 寻找可能的医院/卫生院列
possible_hospital_cols = [col for col in combined.columns if '医院' in col or '卫生院' in col or '医疗' in col]

# 如果找到匹配的列，则重命名
if possible_year_cols:
    combined.rename(columns={possible_year_cols[0]: "年份"}, inplace=True)
if possible_gdp_cols:
    combined.rename(columns={possible_gdp_cols[0]: "国内生产总值"}, inplace=True)
if possible_retail_cols:
    combined.rename(columns={possible_retail_cols[0]: "社会商品零售总额"}, inplace=True)
if possible_hospital_cols:
    combined.rename(columns={possible_hospital_cols[0]: "医院卫生院数"}, inplace=True)

# 4. 处理年份列（如果存在）
if "年份" in combined.columns:
    # 确保年份是数值类型
    combined["年份"] = pd.to_numeric(combined["年份"], errors='coerce')
    # 填充缺失值
    combined["年份"].fillna(combined["年份"].mode()[0], inplace=True)
    combined["年份"] = combined["年份"].astype(int)
else:
    print("警告：未找到年份列，创建占位列")
    combined["年份"] = 0

# 5. 处理GDP列（如果存在）
if "国内生产总值" in combined.columns:
    # 确保GDP是数值类型
    combined["国内生产总值"] = pd.to_numeric(combined["国内生产总值"], errors='coerce')
    # 填充缺失值
    combined["国内生产总值"].fillna(0, inplace=True)
    # 处理可能的单位问题
    if combined["国内生产总值"].dtype == 'object':
        combined["国内生产总值"] = combined["国内生产总值"].str.replace(r'[亿元|万]', '', regex=True)
        combined["国内生产总值"] = pd.to_numeric(combined["国内生产总值"], errors='coerce').fillna(0)
else:
    print("警告：未找到GDP列，创建占位列")
    combined["国内生产总值"] = 0

# 6. 处理社会商品零售总额列（如果存在）
if "社会商品零售总额" in combined.columns:
    # 确保数值类型
    combined["社会商品零售总额"] = pd.to_numeric(combined["社会商品零售总额"], errors='coerce')
    combined["社会商品零售总额"].fillna(0, inplace=True)
    if combined["社会商品零售总额"].dtype == 'object':
        combined["社会商品零售总额"] = combined["社会商品零售总额"].str.replace(r'[亿元|万]', '', regex=True)
        combined["社会商品零售总额"] = pd.to_numeric(combined["社会商品零售总额"], errors='coerce').fillna(0)
else:
    print("警告：未找到社会商品零售总额列，创建占位列")
    combined["社会商品零售总额"] = 0

# 7. 处理医院卫生院数列（如果存在）
if "医院卫生院数" in combined.columns:
    # 确保数值类型
    combined["医院卫生院数"] = pd.to_numeric(combined["医院卫生院数"], errors='coerce')
    combined["医院卫生院数"].fillna(0, inplace=True)
    if combined["医院卫生院数"].dtype == 'object':
        combined["医院卫生院数"] = combined["医院卫生院数"].str.replace(r'[个|所]', '', regex=True)
        combined["医院卫生院数"] = pd.to_numeric(combined["医院卫生院数"], errors='coerce').fillna(0)
else:
    print("警告：未找到医院卫生院数列，创建占位列")
    combined["医院卫生院数"] = 0

# 8. 填充所有缺失值为0
combined.fillna(0, inplace=True)

# 9. 按年份聚合求生产总值
if "年份" in combined.columns and "国内生产总值" in combined.columns:
    # 按年份分组求总值
    annual_gdp = combined.groupby("年份")["国内生产总值"].sum().reset_index()
    # 按年份排序
    annual_gdp = annual_gdp.sort_values("年份")

    print("\n年度GDP汇总结果:")
    print(annual_gdp)
else:
    print("\n无法计算年度GDP，关键列缺失")

# 10. 保存基础结果
output_path = os.path.join(base_dir, "合并后的城市数据.csv")
combined.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n已保存合并数据到: {output_path}")

# ================== 新增功能 ================== #

# 功能5：计算每个城市GDP年均增长率，找出最高和最低的五个城市
if "年份" in combined.columns and "国内生产总值" in combined.columns and "地区" in combined.columns:
    # 按城市和年份分组
    city_gdp = combined.pivot_table(index="地区", columns="年份", values="国内生产总值", aggfunc='sum')

    # 仅保留2015和2017年的数据
    years = sorted(combined["年份"].unique())
    if 2015 in years and 2017 in years:
        # 计算年均增长率 = (2017年GDP / 2015年GDP)^(1/2) - 1
        city_gdp["增长率"] = ((city_gdp[2017] / city_gdp[2015]) ** (1 / 2)) - 1

        # 处理无穷值和缺失值
        city_gdp.replace([np.inf, -np.inf], np.nan, inplace=True)
        city_gdp["增长率"].fillna(0, inplace=True)

        # 按增长率排序
        top_growth = city_gdp.nlargest(5, "增长率")
        bottom_growth = city_gdp.nsmallest(5, "增长率")

        print("\nGDP增长率最高5个城市:")
        print(top_growth[["增长率"]])

        print("\nGDP增长率最低5个城市:")
        print(bottom_growth[["增长率"]])

        # 保存结果
        growth_path = os.path.join(base_dir, "城市GDP增长率.csv")
        city_gdp.to_csv(growth_path, encoding='utf-8-sig')
        print(f"已保存城市GDP增长率数据到: {growth_path}")
    else:
        print("缺少2015或2017年数据，无法计算年均增长率")
else:
    print("缺少地区、年份或GDP数据，无法计算城市增长率")

# 功能6：医院卫生院数Min-Max归一化处理
if "年份" in combined.columns and "医院卫生院数" in combined.columns and "地区" in combined.columns:
    # 按年份处理
    scaler = MinMaxScaler()
    normalized_hospitals = combined.copy()

    # 分组按年份进行归一化
    for year in sorted(combined["年份"].unique()):
        year_mask = combined["年份"] == year
        hospitals = combined.loc[year_mask, "医院卫生院数"].values.reshape(-1, 1)

        # 仅在有数据时进行归一化
        if len(hospitals) > 1:
            normalized = scaler.fit_transform(hospitals)
            normalized_hospitals.loc[year_mask, "医院卫生院数_归一化"] = normalized

    print("\n归一化后的医院卫生院数示例:")
    print(normalized_hospitals[["地区", "年份", "医院卫生院数", "医院卫生院数_归一化"]].head(10))

    # 保存结果
    hospital_path = os.path.join(base_dir, "医疗资源归一化.csv")
    normalized_hospitals.to_csv(hospital_path, index=False, encoding='utf-8-sig')
    print(f"已保存归一化医疗资源数据到: {hospital_path}")
else:
    print("缺少年份或医院卫生院数数据，无法进行归一化")

# 功能7：提取四个城市的关键数据
if "年份" in combined.columns and "国内生产总值" in combined.columns and "社会商品零售总额" in combined.columns and "地区" in combined.columns:
    # 目标城市列表
    target_cities = ["北京", "上海", "广州", "深圳"]

    # 提取数据
    city_data = combined[
        combined["地区"].isin(target_cities) &
        combined["年份"].isin([2015, 2016, 2017])
        ][["地区", "年份", "国内生产总值", "社会商品零售总额"]]

    # 按城市和年份排序
    city_data = city_data.sort_values(["地区", "年份"])

    # 处理可能的城市名称不一致
    found_cities = city_data["地区"].unique()
    missing = set(target_cities) - set(found_cities)
    if missing:
        print(f"\n警告：未找到城市: {', '.join(missing)}")

    # 保存结果
    city_path = os.path.join(base_dir, "重点城市经济数据.csv")
    city_data.to_csv(city_path, index=False, encoding='utf-8-sig')
    print(f"\n已保存重点城市数据到: {city_path}")
    print("提取的数据:")
    print(city_data)
else:
    print("缺少关键列，无法提取重点城市数据")

# 数据报告
print("\n数据处理结果报告:")
print(f"合并文件数: {len(files)}")
print(f"数据记录总数: {len(combined)}")
print(f"数据年份范围: {combined['年份'].min()}-{combined['年份'].max()}") if "年份" in combined.columns else ""
print(f"涵盖城市数量: {combined['地区'].nunique()}") if "地区" in combined.columns else ""
print(f"GDP总量: {combined['国内生产总值'].sum():,.2f}") if "国内生产总值" in combined.columns else ""
print(f"平均医院卫生院数: {combined['医院卫生院数'].mean():.1f}") if "医院卫生院数" in combined.columns else ""