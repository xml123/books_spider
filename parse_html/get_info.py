import datetime
import json

from get_html.get_html_text import get_html_text,save_img
from lxml import etree
import urllib
import time


def html_parser(html_text, compl_str):
    # 解析HTML文件
    try:
        tree = etree.HTML(html_text)
        res = tree.xpath(compl_str)
    except:
        print(datetime.datetime.now())
        print("can't parse html")
        return
    return res


# 获取书本的说明信息和各个章节的URL
def get_info_and_chapter_url(one_book_url):
    # 本书目录信息
    book_info = {}
    # 得到URL的HTML文件
    try:
        book_html_text = get_html_text(one_book_url)
        # 得到书本的url
        book_info['url'] = one_book_url
        # 得到书的标题
        title_res = html_parser(book_html_text, '//*[@id="info"]/h1/text()')
        print('booksName',title_res[0])
    except:
        print('解析html出错')
        return
    if len(title_res):
        title = title_res[0]
        book_info["name"] = title
    else:
        return
    # 得到书的分类
    book_kind_list = html_parser(book_html_text,
                                 '//*[@id="wrapper"]/div[@class="box_con"]/div[@class="con_top"]/text()')
    if len(book_kind_list) > 2:
        book_kind = str(book_kind_list[2]).split('>')[1].replace(" ", '')
        book_info["kind"] = book_kind
    else:
        book_info['kind'] = ''
    # 得到书的简介
    book_abstract = html_parser(book_html_text, '//*[@id="intro"]/p[1]/text()')
    if len(book_abstract):
        book_info["abstract"] = book_abstract[0]
    else:
        book_info["abstract"] = ''
    # 得到书本的封面图
    book_img_list = html_parser(book_html_text, '//*[@id="fmimg"]/img/@src')
    if len(book_img_list):
        book_half_img = book_img_list[0]
        # print('name',name)
        print('book_half_img',book_half_img)
        # book_img = r"http://www.biquge.com.tw" + book_half_img
        # 将远程图片下载到本地，第二个参数就是要保存到本地的文件名

        #book_img = book_half_img
        book_info["img"] = book_half_img
    else:
        book_info['img'] = ''
    # 得到书本的作者信息
    book_author_list = html_parser(book_html_text, '//*[@id="info"]/p[1]/text()')
    if len(book_author_list):
        book_author_str = str(book_author_list[0]).split("：")[1]
        book_info['author'] = book_author_str
    else:
        book_info['author'] = ''
    # 得到文章章节链接和章节名
    chapter_list = []
    chapter_nodes = html_parser(book_html_text, '//*[@id="list"]/dl/dd/a')
    for one in chapter_nodes:
        tmp = {}
        # 得到章节节点的标题
        chapter_name_res = one.xpath("text()")
        if len(chapter_name_res):
            chapter_name = chapter_name_res[0]
            tmp["chapter_name"] = chapter_name
        # 得到章节的url
        chapter_href_res = one.xpath("@href")
        if len(chapter_href_res):
            chapter_href = r"http://www.biquge.com.tw" + chapter_href_res[0]
            tmp["chapter_href"] = chapter_href
        chapter_list.append(tmp)
    # 重新组合信息
    book_info['chapter'] = chapter_list
    return book_info


# 根据一个章节url,获取格式化的章节信息
def get_chapter_text_by_url(url):
    # 根据url获取html内容
    chapter_text = get_html_text(url)
    # 获取章节正文内容
    res = html_parser(chapter_text,
                      "/html/body/div[@id='wrapper']/div[@class='content_read']"
                      "/div[@class='box_con']/div[@id='content']/text()")
    if not res:
        return 0
    chapter_text = str(res).replace(r"\r\n\xa0\xa0\xa0\xa0", "").replace(
        r"\xa0\xa0\xa0\xa0", "").replace(r'\r\n', "\n").replace("'", '').replace("[", '').replace("]", '').replace(r',', '')

    #print(chapter_text)

    return chapter_text
