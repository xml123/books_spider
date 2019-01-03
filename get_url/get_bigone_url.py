# 获取一级页面的url
import json
import time

from parse_html.get_info import get_chapter_text_by_url
from save_to_db.save_book import get_book_id_by_name, set_book_has_chapter_by_id, save_chapter


def get_level_one_url():
    bigone_url_list = []
    for i in range(0, 20):
        if i == 0:
            half_url = r'http://www.biquge.com.tw/%s_' % (i)
            for j in range(1, 1000):
                url = half_url + str(j)
                bigone_url_list.append(url)
        else:
            half_url = r'http://www.biquge.com.tw/%s_%s' % (i, i)
            for j in range(1, 1000):
                if i == 19:
                    if j < 768:
                        url = splicing_bigone_url(half_url, j)
                        bigone_url_list.append(url)
                else:
                    url = splicing_bigone_url(half_url, j)
                    bigone_url_list.append(url)
    return bigone_url_list


# 拼接一级页面URL
def splicing_bigone_url(half_url, j):
    str_num = str(j)
    len_num = len(str_num)
    if len_num == 1:
        str_num = "00" + str_num
    elif len_num == 2:
        str_num = "0" + str_num
    url = half_url + str_num + '/'
    return url


# 根据book_info,获取所有的章节url和章节名
def get_chapter_by_book_info(book_info):
    # 根据书名,查询数据库,然后得到id
    book_name = book_info.get("name")
    # 得到书的id
    book_id = get_book_id_by_name(book_name)
    # 得到所有的章节数组,然后重新组合成为一个数据
    chapter_list = book_info.get('chapter')
    chapter_id = 0
    for one in chapter_list:
        chapter_id = chapter_id+1
        one_chapter = {}
        chapter_url = one.get("chapter_href")
        one_chapter['href'] = chapter_url
        one_chapter['name'] = one.get("chapter_name")
        # 根据章节url去获取页面,并解析格式化数据
        res = get_chapter_text_by_url(chapter_url)
        # 当有章节为空的时候就跳出本次循环
        if not res:
            set_book_has_chapter_by_id(book_id)
            break
        one_chapter['data'] = res
        # 对章节执行保存到数据库的操作
        one_chapter["book_id"] = book_id
        one_chapter["chapter_id"] = chapter_id
        # 保存章节信息到章节表
        save_chapter(one_chapter)
        # 延时一秒操作
        time.sleep(1)
