def is_palindrome(num):
    num_str = str(num)
    return num_str == num_str[::-1]

print("练习题1: 回文数判断")
print(f"121 是回文数吗? {is_palindrome(121)}")
print(f"123 是回文数吗? {is_palindrome(123)}")
print(f"1221 是回文数吗? {is_palindrome(1221)}")



def average(*args):
    if not args:
        return 0
    return sum(args) / len(args)


print("\n练习题2: 计算平均值")
print(f"1, 2, 3的平均值: {average(1, 2, 3):.2f}")
print(f"10, 20, 30, 40的平均值: {average(10, 20, 30, 40):.2f}")
print(f"空参数的平均值: {average()}")




def longest_string(*strings):
    if not strings:
        return ""
    return max(strings, key=len)


print("\n练习题3: 最长字符串")
print(f"最长的字符串是: {longest_string('apple', 'banana', 'cherry')}")
print(f"最长的字符串是: {longest_string('Python', 'is', 'awesome')}")
print(f"最长的字符串是: {longest_string('a', 'bb', 'ccc', 'dddd')}")



from rectangle import rectangle_area, rectangle_perimeter

try:
    length = float(input("请输入矩形的长度: "))
    width = float(input("请输入矩形的宽度: "))

    # 使用模块中的函数进行计算
    area = rectangle_area(length, width)
    perimeter = rectangle_perimeter(length, width)

    # 输出结果
    print("\n计算结果:")
    print(f"长度: {length}, 宽度: {width}")
    print(f"面积: {area}")
    print(f"周长: {perimeter}")

except ValueError:
    print("错误: 请输入有效的数字!")