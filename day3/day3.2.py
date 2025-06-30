import requests
from lxml import etree
import os
import urllib.parse


def download_images():
    # 目标网址（彼岸图片网首页）
    base_url = "http://pic.netbian.com/"

    # 自定义保存路径（用户指定的文件夹）
    save_dir = r"C:\Users\Administrator\Desktop\新建文件夹 (2)"  # 原始字符串避免转义问题

    # 请求头（模拟浏览器访问）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        # 步骤1：获取网页源码
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP请求是否成功（非200状态码报错）
        response.encoding = "gbk"  # 彼岸图片网页面编码为gbk

        # 步骤2：解析HTML，提取图片链接
        html = etree.HTML(response.text)
        img_src_list = html.xpath("//ul[@class='clearfix']/li/a/span/img/@src")
        print(f"提取到 {len(img_src_list)} 张图片链接")

        # 步骤3：创建保存目录（若不存在则自动创建）
        try:
            os.makedirs(save_dir, exist_ok=True)  # exist_ok=True：目录存在时不报错
            print(f"保存目录已创建/确认：{save_dir}")
        except PermissionError:
            print(f"错误：无权限创建/写入目录 {save_dir}，请检查文件夹权限（右键→属性→安全）")
            return
        except Exception as e:
            print(f"创建目录失败：{e}")
            return

        # 步骤4：遍历下载图片
        for idx, img_src in enumerate(img_src_list, 1):
            # 拼接完整图片URL（处理相对路径，如 "/d/file/xxx.jpg" → 完整地址）
            full_img_url = urllib.parse.urljoin(base_url, img_src)

            try:
                # 下载图片二进制内容
                img_response = requests.get(full_img_url, headers=headers, timeout=10)
                img_response.raise_for_status()  # 检查图片请求是否成功

                # 提取文件扩展名（如.jpg、.png），若没有则默认.jpg
                file_ext = os.path.splitext(img_src)[1].lower()
                if not file_ext:  # 无扩展名时（罕见）默认用.jpg
                    file_ext = ".jpg"

                # 本地保存路径（如：d:\images\1.jpg）
                save_path = os.path.join(save_dir, f"{idx}{file_ext}")

                # 写入文件（二进制模式）
                with open(save_path, "wb") as f:
                    f.write(img_response.content)
                print(f"下载成功：{save_path}")

            except requests.exceptions.RequestException as e:
                print(f"下载失败（第{idx}张）：{img_src} - 网络错误：{e}")
            except PermissionError:
                print(f"下载失败（第{idx}张）：{img_src} - 无权限写入文件，请检查文件是否被其他程序占用")
            except Exception as e:
                print(f"下载失败（第{idx}张）：{img_src} - 其他错误：{e}")

    except requests.exceptions.RequestException as e:
        print(f"获取网页失败：{e}")
    except Exception as e:
        print(f"程序异常：{e}")


if __name__ == "__main__":
    download_images()