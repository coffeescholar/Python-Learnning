# 下载教材PDF文件小工具
# 主要功能：从国家智慧教育公共服务平台下载小学、中学的教材电子版
# 作者：loongba
# 版本：V1.0

# Stmart Education 智慧教育
# SmartEdu.cn
# 国家智慧教育公共服务平台 —— 推进教育资源公平化：网络课件 同等的教育资源
# 国家中小学智慧教育平台 —— basic.SmartEdu.cn 基础教育：基教处——《义务教育法》，“九漏鱼”
# 

# 主要步骤：
# 1. 获得要下载的教材的 URL——参数：用户提供
#   https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=8b9c7052-add4-4744-ab04-69d6c180d5d9&catalogType=tchMaterial&subCatalog=tchMaterial
# 2. 用代码下载该 Url，获得网页的内容 HTML
# 3. 分析该 HTML 找出我们所需要的内容：教材PDF 的 URL
# 4. 用代码下载该 URL，另存为 PDF 文件
# 5. 完成，显示提示信息，打开 PDF 文件
import os
import sys
import re
import requests       # request 请求 response 回应/响应
# 获取指定 Url 的 HTML 并返回
def get_html_by_url(url):
    session = requests.Session()
    try:
        response = session.get(url, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        print_error(f"获取 HTML 时发生错误: {e}")
        return None    
    return html

# 获取课件的 PDF url 并返回
def get_book_pdf_url(html:str):
# https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets_document/5cd7e623-5c38-4602-871a-3fba8a551db2.pkg/pdf.pdf
    # 定义一个正则表达式规则，用于匹配 PDF url
    pattern = r'https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets_document/\w+-\w+-\w+-\w+.pkg/pdf.pdf'
    # 使用 re.search() 函数查找匹配的字符串
    match = re.search(pattern, html)
    # 如果找到匹配的字符串，返回它；否则，返回 None
    if match:
        return match.group()
    else:
        return None

# 下载指定的文件，并以指定的文件名，保存到指定的位置
def download_file(file_url, save_path, save_file_name):
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        with open(os.path.join(save_path, save_file_name), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return True
    except requests.RequestException as e:
        print(f"下载文件时发生错误: {e}")
        return False
    return

def main():
    book_url = "https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=8b9c7052-add4-4744-ab04-69d6c180d5d9&catalogType=tchMaterial&subCatalog=tchMaterial"
    # 1. 获得要下载的教材的 URL——参数：用户提供
    if len(sys.argv) > 1:
        book_url = sys.argv[1]
    else:
        print_error("请提供有效的教材 Url 参数")
        #return

    # 2. 用代码下载该 Url，获得网页的内容 HTML
    html = get_html_by_url(book_url)

    # 3. 分析该 HTML 找出我们所需要的内容：教材PDF 的 URL
    book_pdf_url, book_name = get_book_pdf_url(html)

    # 4. 用代码下载该 URL，另存为 PDF 文件
    # 默认保存在脚本的同级目录下
    script_folder_path = os.path.dirname(os.path.abspath(__file__))  #相对路径转换为绝对路径，以防万一
    pdf_file_path = download_file(book_pdf_url, script_folder_path, book_name)

    # 5. 完成，显示提示信息，打开 PDF 文件
    print_color(f"成功下载教材 {book_name} 的 PDF 文件：{pdf_file_path}", "green")
    run_file_by_default_app(pdf_file_path)
    #run_file_by_default_app(script_folder_path)

# 输出错误信息
def print_error(message):
    print_color(message, "red")
    return

def print_color(message, color="green", end_str="\r\n"):
    text = color_text(color, message)
    # 用 switch 判断常用的颜色，或者用 字典
    print(text, end=end_str)

def color_text(color, text):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }

    if color in colors:
        return f"{colors[color]}{text}{colors['reset']}"
    else:
        return text

def run_file_by_default_app(file_path):
    if os.path.isfile(file_path):
        os.startfile(file_path)
    else:
        os.system("explorer.exe", file_path)

    return

if __name__ == "__main__":
    main()