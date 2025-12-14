import requests
from lxml import etree
import sys
import os

# 豆瓣书籍搜索URL
DOUBAN_SEARCH_URL = "https://search.douban.com/book/subject_search"

def get_book_info(book_name):
    """
    根据书名爬取豆瓣书籍信息
    :param book_name: 输入的书名
    :return: 书籍信息字典，失败返回None
    """
    # 请求头（模拟浏览器，避免被反爬）
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    # 请求参数
    params = {
        "search_text": book_name,
        "cat": "1001"  # 1001表示只搜索书籍
    }

    try:
        # 1. 发送请求获取搜索结果页面
        response = requests.get(
            url=DOUBAN_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=10  # 超时时间10秒
        )
        response.raise_for_status()  # 若请求失败（如404/500），抛出异常

        # 调试：打印响应状态和部分HTML内容
        print(f"【调试】响应状态码：{response.status_code}")
        print(f"【调试】响应URL：{response.url}")
        print(f"【调试】HTML内容前1000字符：{response.text[:1000]}...")
        print(f"【调试】HTML内容中包含'subject'的部分：{[line for line in response.text.splitlines() if 'subject' in line][:5]}")

        # 2. 解析JavaScript数据（豆瓣现在使用动态加载，搜索结果在window.__DATA__中）
        import json
        try:
            # 提取window.__DATA__变量的值
            data_start = response.text.find('window.__DATA__ = ')
            if data_start == -1:
                print("未找到window.__DATA__变量")
                return None
                
            data_start += len('window.__DATA__ = ')
            data_end = response.text.find(';', data_start)
            if data_end == -1:
                data_end = response.text.find('<', data_start)
                
            json_str = response.text[data_start:data_end].strip()
            print(f"【调试】提取的JSON字符串前200字符：{json_str[:200]}...")
            
            # 解析JSON数据
            data = json.loads(json_str)
            
            # 获取搜索结果
            if 'items' not in data:
                print("JSON数据结构不符合预期，未找到items字段")
                print(f"【调试】JSON数据键：{list(data.keys())}")
                return None
                
            items = data['items']
            print(f"【调试】找到{len(items)}个搜索结果")
            
            # 提取第一个有效书籍链接
            first_book_link = None
            for item in items:
                if 'url' in item and 'subject' in item['url']:
                    first_book_link = item['url']
                    print(f"【调试】找到书籍链接：{first_book_link}")
                    break
            
            if not first_book_link:
                print(f"未找到《{book_name}》相关书籍信息1")
                return None
                
        except json.JSONDecodeError as e:
            print(f"解析JSON数据出错：{e}")
            return None
        except Exception as e:
            print(f"处理JavaScript数据出错：{e}")
            return None

        # 4. 访问书籍详情页
        book_detail_response = requests.get(
            url=first_book_link,
            headers=headers,
            timeout=10
        )
        book_detail_response.raise_for_status()
        detail_html = etree.HTML(book_detail_response.text)

        # 5. 提取书籍核心信息（使用XPath定位元素）
        book_info = {}
        
        # 书名
        try:
            book_info["title"] = detail_html.xpath('//h1/span[@property="v:itemreviewed"]/text()')[0].strip()
        except:
            try:
                book_info["title"] = detail_html.xpath('//h1/text()')[0].strip()
            except:
                book_info["title"] = book_name
                
        # 作者
        try:
            author_xpath = '//div[@id="info"]//a[contains(@href, "/author/")]/text()'
            authors = detail_html.xpath(author_xpath)
            book_info["author"] = ", ".join([a.strip() for a in authors]) if authors else "未知"
        except:
            book_info["author"] = "未知"
            
        # 出版年份
        try:
            # 尝试多种方式提取出版年份
            publish_year = "未知"
            
            # 方式1：查找包含"出版年"的节点（考虑不同的中文表述）
            year_patterns = ["出版年", "出版日期", "出版时间", "年份"]
            for pattern in year_patterns:
                year_nodes = detail_html.xpath(f'//div[@id="info"]//text()[contains(., "{pattern}")]/following-sibling::text()')
                for node in year_nodes:
                    year_text = node.strip()
                    if year_text:
                        # 提取4位数字年份
                        import re
                        year_match = re.search(r'(\d{4})', year_text)
                        if year_match:
                            publish_year = year_match.group(1)
                            break
                if publish_year != "未知":
                    break
                    
            # 方式2：如果方式1失败，查找所有包含4位数字的文本
            if publish_year == "未知":
                all_text = "".join(detail_html.xpath('//div[@id="info"]//text()'))
                import re
                year_match = re.search(r'(19|20)\d{2}', all_text)
                if year_match:
                    publish_year = year_match.group(0)
                        
            # 方式3：尝试另一种XPath结构
            if publish_year == "未知":
                try:
                    year_text = detail_html.xpath('//div[@id="info"]//span[contains(text(), "出版年")]/following::text()')[0].strip()
                    import re
                    year_match = re.search(r'(\d{4})', year_text)
                    if year_match:
                        publish_year = year_match.group(1)
                except:
                    pass
                        
            book_info["publish_year"] = publish_year
        except:
            book_info["publish_year"] = "未知"
            
        # 出版社
        try:
            # 尝试多种方式提取出版社
            publisher = "未知"
            
            # 方式1：查找包含"出版社"的节点
            publisher_nodes = detail_html.xpath('//div[@id="info"]//text()[contains(., "出版社")]/following-sibling::text()')
            for node in publisher_nodes:
                publisher_text = node.strip()
                if publisher_text and publisher_text != ":":
                    publisher = publisher_text
                    break
                    
            # 方式2：查找所有a标签，排除作者链接
            if publisher == "未知":
                publisher_nodes = detail_html.xpath('//div[@id="info"]//a[not(contains(@href, "/author/")) and not(contains(@href, "/subject/"))]/text()')
                for node in publisher_nodes:
                    publisher_text = node.strip()
                    if publisher_text:
                        publisher = publisher_text
                        break
                        
            book_info["publisher"] = publisher
        except:
            book_info["publisher"] = "未知"
            
        # ISBN
        try:
            # 尝试多种方式提取ISBN
            isbn = "未知"
            
            # 方式1：查找包含"ISBN"的节点
            isbn_nodes = detail_html.xpath('//div[@id="info"]//text()[contains(., "ISBN")]/following-sibling::text()')
            for node in isbn_nodes:
                isbn_text = node.strip()
                if isbn_text and len(isbn_text) > 5:
                    isbn = isbn_text
                    break
                    
            # 方式2：使用更通用的方式查找ISBN
            if isbn == "未知":
                all_text = "".join(detail_html.xpath('//div[@id="info"]//text()'))
                import re
                isbn_match = re.search(r'ISBN\s*:\s*(\d+)', all_text)
                if isbn_match:
                    isbn = isbn_match.group(1)
                    
            book_info["isbn"] = isbn
        except:
            book_info["isbn"] = "未知"

        return book_info

    except IndexError:
        print(f"未找到《{book_name}》的详细信息2：{IndexError}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误：{e}")
        return None
    except Exception as e:
        print(f"解析数据出错：{e}")
        return None

def generate_markdown(book_info, output_dir="output"):
    """
    根据书籍信息生成Markdown文件
    :param book_info: 书籍信息字典
    :param output_dir: 输出目录
    """
    # 创建输出目录（不存在则创建）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Markdown文件名（用书名命名，避免特殊字符）
    safe_title = book_info["title"].replace("/", "-").replace("\\", "-").replace(":", "-")
    md_filename = f"{output_dir}/{safe_title}.md"

    # 构建Markdown内容
    md_content = f"""# {book_info['title']}

## 书籍基础信息
| 项目 | 内容 |
|------|------|
| 书名 | {book_info['title']} |
| 作者 | {book_info['author']} |
| 出版年份 | {book_info['publish_year']} |
| 出版社 | {book_info['publisher']} |
| ISBN | {book_info['isbn']} |

## 说明
本文件由book2MK工具自动生成，数据来源：豆瓣读书
"""

    # 写入文件
    try:
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Markdown文件已生成：{md_filename}")
    except Exception as e:
        print(f"生成Markdown文件失败：{e}")

def main():
    """
    主函数：处理用户输入，执行爬取和生成Markdown
    """
    # 检查用户是否输入书名
    if len(sys.argv) < 2:
        print("使用方法：uv run book2mk.py <书名>")
        print("示例：uv run book2mk.py 三体")
        sys.exit(1)

    # 获取用户输入的书名
    book_name = sys.argv[1]
    print(f"正在搜索书籍：{book_name}")

    # 爬取书籍信息
    book_info = get_book_info(book_name)
    if not book_info:
        sys.exit(1)

    # 生成Markdown文件
    generate_markdown(book_info)

if __name__ == "__main__":
    main()