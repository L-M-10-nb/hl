import os
import re


# Windows自然排序键生成器
def windows_natural_sort_key(filename):
    convert = lambda text: text.zfill(8) if text.isdigit() else text.lower()
    return [convert(t) for t in re.split(r'(\d+)', filename)]


def rename_images():
    txt_path = r"C:\Users\Administrator\Desktop\新建文本文档.txt"
    image_folder = r"C:\Users\Administrator\Desktop\新建文件夹"

    # 步骤1: 读取文本文档中的名字
    with open(txt_path, 'r', encoding='utf-8') as f:
        names = [name.strip() for name in f.readlines() if name.strip()]

    # 步骤2: 获取图片文件列表
    files = os.listdir(image_folder)

    # 步骤3: Windows自然排序（按文件名中的数字顺序排列）
    # 使用Windows资源管理器式的自然排序算法
    files.sort(key=windows_natural_sort_key)

    # 步骤4: 只处理图片文件（保留原有扩展名）
    image_files = [f for f in files if os.path.isfile(os.path.join(image_folder, f))
                   and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 步骤5: 重命名图片文件
    for i, name in enumerate(names):
        # 确保索引在范围内
        if i >= len(image_files):
            break

        old_filename = image_files[i]
        # 获取原文件扩展名
        extension = os.path.splitext(old_filename)[1]

        # 构建完整路径
        old_path = os.path.join(image_folder, old_filename)
        new_path = os.path.join(image_folder, f"{name}{extension}")

        # 执行重命名
        os.rename(old_path, new_path)
        print(f"已重命名: {old_filename} -> {name}{extension}")


# 运行主函数
if __name__ == "__main__":
    # 确认操作
    confirm = input("将按Windows自然排序规则重命名图片文件，是否继续? (y/n): ").lower()
    if confirm == 'y':
        rename_images()
        print("重命名操作已完成!")
    else:
        print("操作已取消")