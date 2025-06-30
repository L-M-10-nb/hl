import requests
from bs4 import BeautifulSoup


def get_douban_top_movies():
    # 目标URL
    url = "https://movie.douban.com/chart"

    # 模拟浏览器的请求头（避免被反爬）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功（非200状态码会抛出异常）
        response.encoding = "utf-8"  # 指定编码（豆瓣页面默认编码为utf-8）

        # 解析HTML内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 定位电影条目（根据豆瓣当前页面结构调整选择器）
        # 每个电影条目包裹在 class="pl2" 的div中，标题在其中的a标签内
        movie_items = soup.select("div.pl2 a")

        # 提取前10部电影名称（去除可能的空白和换行）
        top_10 = [item.get_text(strip=True) for item in movie_items[:10]]

        return top_10

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except Exception as e:
        print(f"解析失败: {e}")
        return []


if __name__ == "__main__":
    top_movies = get_douban_top_movies()
    if top_movies:
        print("豆瓣电影排行榜前十名：")
        for idx, movie in enumerate(top_movies, 1):
            print(f"{idx}. {movie}")
    else:
        print("未获取到电影数据")