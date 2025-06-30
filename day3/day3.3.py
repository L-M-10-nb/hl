import time
import random
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager  # 仅需导入ChromeDriverManager

# 文献列表
papers = [
    "Automatic crater detection and age estimation for mare regions on the lunar surface",
    "The origin of planetary impactors in the inner solar system",
    "Deep learning based systems for crater detection: A review",
    "A preliminary study of classification method on lunar topography and landforms",
    "The CosmoQuest Moon mappers community science project: The effect of incidence angle on the Lunar surface crater distribution",
    "Fast r-cnn",
    "You only look once: Unified, real-time object detection",
    "Attention is all you need",
    "End-to-end object detection with transformers"
]


def setup_driver():
    """配置并启动Chrome浏览器（自动匹配ChromeDriver）"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无界面模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 反自动化设置
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # 设置真实用户代理（匹配Chrome 137）
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    ]
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')

    # 自动安装并配置匹配的ChromeDriver（省略ChromeType）
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 隐藏自动化特征
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def human_like_delay(min=0.5, max=3.0):
    """模拟人类操作延迟"""
    time.sleep(random.uniform(min, max))


def get_bibtex(driver, paper_title):
    """获取并返回文献的BibTeX引用格式"""
    try:
        # 构建搜索URL
        encoded_title = urllib.parse.quote_plus(paper_title)
        url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={encoded_title}"

        # 访问搜索页面
        driver.get(url)
        human_like_delay(1.0, 2.5)

        # 等待结果加载
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_r.gs_or.gs_scl"))
        )

        # 模拟人类滚动
        for _ in range(2):
            driver.execute_script("window.scrollBy(0, window.innerHeight * 0.5);")
            human_like_delay(0.7, 1.5)

        # 获取第一个结果
        first_result = driver.find_element(By.CSS_SELECTOR, "div.gs_r.gs_or.gs_scl")

        # 显示更多的引用选项
        cite_button = first_result.find_element(By.CSS_SELECTOR, "a.gs_or_cit")
        driver.execute_script("arguments[0].click();", cite_button)
        human_like_delay(1.0, 2.0)

        # 等待引用弹出框出现
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_citr"))
        )

        # 切换到BibTeX格式
        bibtex_link = driver.find_element(By.XPATH, "//a[contains(., 'BibTeX')]")
        bibtex_url = bibtex_link.get_attribute('href')

        # 直接访问BibTeX链接
        driver.get(bibtex_url)
        human_like_delay(2.0, 3.0)

        # 获取并返回BibTeX内容
        pre_element = driver.find_element(By.TAG_NAME, 'pre')
        bibtex_content = pre_element.text
        return bibtex_content

    except (TimeoutException, NoSuchElementException):
        print(f"未找到文献: {paper_title[:50]}...")
        return f"@article{{ERROR: 未能找到文献引用 - {paper_title[:50]}...}}\n"
    except Exception as e:
        print(f"处理文献时出错: {paper_title[:50]}..., 原因: {str(e)[:100]}")
        return f"@article{{ERROR: {str(e)[:100].replace('@', '')}}}\n"


def main():
    driver = setup_driver()
    output = "以下是您文献的BibTeX引用格式：\n\n"

    try:
        # 首先访问主页建立会话
        driver.get("https://scholar.google.com")
        human_like_delay(2.0, 4.0)

        for i, paper in enumerate(papers, 1):
            print(f"正在处理第 {i}/{len(papers)} 篇文献: {paper[:50]}...")

            # 随机延迟避免封禁
            human_like_delay(random.uniform(3.0, 7.0))

            # 获取文献引用
            bibtex = get_bibtex(driver, paper)

            # 添加到输出
            output += f"%%% 文献 {i} - {paper[:60]}... %%%\n"
            output += bibtex + "\n\n"

            # 返回主页
            driver.get("https://scholar.google.com")
            human_like_delay(1.5, 2.5)

        # 显示最终结果
        print("\n" + "=" * 70)
        print(output)
        print("=" * 70)
        print("所有文献的BibTeX格式已成功生成！")

    except Exception as e:
        print(f"严重错误: {str(e)}")
    finally:
        driver.quit()
        print("浏览器已关闭")


if __name__ == "__main__":
    main()