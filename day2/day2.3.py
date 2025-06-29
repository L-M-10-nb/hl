import os
import re


def natural_sort_key(s):
    """
    实现特定排序规则：数字按自然排序，但带前导零的数字排在相同值的数字之前
    """

    def convert(text):
        if text.isdigit():
            num_val = int(text)
            # 如果是以0开头的数字，返回一个特殊的元组使其排在普通数字之前
            if text.startswith('0') and len(text) > 1:
                return (num_val - 0.5, text)  # 减去0.5使其小于普通整数
            return (num_val, text)
        return text.lower()

    return [convert(p) for p in re.split('([0-9]+)', s)]


def rename_images():
    # 定义路径
    txt_path = r"C:\Users\Administrator\Desktop\新建文本文档.txt"
    image_folder = r"C:\Users\Administrator\Desktop\新建文件夹"

    # 读取文本名称
    with open(txt_path, 'r', encoding='utf-8') as f:
        names = [name.strip() for name in f.readlines() if name.strip()]

    # 获取所有图片文件
    files = os.listdir(image_folder)

    # 过滤图片文件并应用特殊排序规则
    image_files = [f for f in files if os.path.isfile(os.path.join(image_folder, f))
                   and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 使用自定义排序键进行排序
    image_files.sort(key=natural_sort_key)

    # 显示排序结果（调试用）
    print("\n文件排序结果：")
    for i, f in enumerate(image_files):
        print(f"{i + 1:2d}. {f}")

    # 重命名图片文件
    for i, name in enumerate(names):
        if i >= len(image_files):
            print(f"警告: 只有{len(image_files)}个图片，但文本有{len(names)}个名称")
            break

        old_filename = image_files[i]
        extension = os.path.splitext(old_filename)[1]

        old_path = os.path.join(image_folder, old_filename)
        new_path = os.path.join(image_folder, f"{name}{extension}")

        os.rename(old_path, new_path)
        print(f"已重命名: {i + 1:2d} - {old_filename} → {name}{extension}")


# 运行主函数
if __name__ == "__main__":
    print("高级自然排序图片重命名工具")
    print("特殊排序规则: 带前导零的数字排在相同值的普通数字之前")

    try:
        rename_images()
        print("\n重命名操作成功完成!")
    except Exception as e:
        print(f"发生错误: {e}")