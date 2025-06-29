import numpy as np

# 第一题  创建3x4的二维数组，元素为1-12的整数
print("第一题：")
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])
# 任务1: 打印数组形状、维度和数据类型
print("数组形状:", arr.shape)
print("数组维度:", arr.ndim)
print("数据类型:", arr.dtype)
# 任务2: 数组元素乘以2并打印结果
doubled_arr = arr * 2
print("\n乘以2后的数组:")
print(doubled_arr)
# 任务3: 重塑为4x3的形状并打印新数组
reshaped_arr = arr.reshape(4, 3)
print("\n重塑后的数组(4x3):")
print(reshaped_arr)





#第二题
# 创建给定的4x4数组
print("第二题：")
array = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]])
print("原始数组:")
print(array)
# 任务1: 提取第2行所有元素（索引为1）
row_2 = array[1, :]
print("\n任务1: 第2行所有元素:")
print(row_2)
# 任务2: 提取第3列所有元素（索引为2）
col_3 = array[:, 2]
print("\n任务2: 第3列所有元素:")
print(col_3)
# 任务3: 提取子数组（包含第1、2行和第2、3列）
sub_array = array[0:2, 1:3]
print("\n任务3: 子数组（第1、2行和第2、3列）:")
print(sub_array)
# 任务4: 将大于10的元素替换为0
modified_array = array.copy()  # 创建副本以避免修改原始数组
modified_array[modified_array > 10] = 0
print("\n任务4: 修改后的数组（大于10的元素替换为0）:")
print(modified_array)



#第三题
# 创建数组A：3x2二维数组，元素为1-6
print("第三题：")
A = np.array([[1, 2],
              [3, 4],
              [5, 6]])

# 创建数组B：一维数组[10, 20]
B = np.array([10, 20])
print("数组A:")
print(A)
print("\n数组B:")
print(B)
# 任务1: 计算A和B的逐元素相加（利用广播）
result_add = A + B
print("\n任务1: A + B (广播相加):")
print(result_add)
# 任务2: 计算A和B的逐元素相乘（利用广播）
result_multiply = A * B
print("\n任务2: A * B (广播相乘):")
print(result_multiply)
# 任务3: 计算A的每一行与B的点积
dot_products = np.dot(A, B)
print("\n任务3: A的每一行与B的点积:")
print(dot_products)