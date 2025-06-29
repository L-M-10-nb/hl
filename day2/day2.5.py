import numpy as np
import rasterio
from PIL import Image
import os


def process_sentinel2_image(input_path, output_path):
    """
    处理哨兵2号卫星图像
    :param input_path: 输入TIFF文件路径
    :param output_path: 输出图像路径
    """
    try:
        # 1. 使用rasterio打开TIFF文件
        with rasterio.open(input_path) as src:
            # 2. 获取图像信息
            print(f"图像信息: {src.width}x{src.height}像素, {src.count}个波段")

            # 3. 读取所有波段数据
            data = src.read()  # 形状为 (band_count, height, width)
            red = data[2]  # 波段4 (红)
            green = data[1]  # 波段3 (绿)
            blue = data[0]  # 波段2 (蓝)

            rgb_image = np.dstack((red, green, blue))
            min = np.min(rgb_image)
            max = np.max(rgb_image)
            band_compressed =  (rgb_image - min) * 255.0  / (max - min)

            band_int = band_compressed.astype(np.uint8)

            # 7. 保存为图像文件
            img = Image.fromarray(band_int)

            img.save(output_path)

    except Exception as e:
        print(f"处理出错: {str(e)}")
        return False


# 输入文件路径和输出文件路径
input_tiff = r"C:\Users\Administrator\Desktop\2020_0427_fire_B2348_B12_10m_roi.tif"
output_image = r"D:\hlnb\pythonProject\day2\sentinel2_rgb.png"

# 处理图像
process_sentinel2_image(input_tiff, output_image)