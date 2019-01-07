import datetime
import time
import random

from get_url.get_bigone_url import get_level_one_url, get_chapter_by_book_info

from parse_html.get_info import get_info_and_chapter_url
from save_to_db.save_book import save_book_info,save_author_tag

# 得到所有小说的大目录的url
big_one_url_list = get_level_one_url()
# 遍历所有的书本链接,进行具体的解析
for one in big_one_url_list:
    # 记录开始时间
    start_time = time.time()
    print(one)
    # 获取书本的书本名\所有章节名和章节url
    try:
        book_info = get_info_and_chapter_url(one)
        time.sleep(random.randint(1,3))
    except Exception as e:
        print(datetime.datetime.now())
        print("save book info fail")
        print(e)
        time.sleep(random.randint(1,3))
        continue
    # 如果没有获取到书本信息,则直接退出本次循环
    if not book_info:
        print(datetime.datetime.now())
        print("no book_info ,exit this one")
        time.sleep(random.randint(1,3))
        continue
    # 执行存入数据库的操作
    is_save = save_author_tag(book_info)
    if not is_save:
        print(datetime.datetime.now())
        print("save book faile ,exit this one")
        time.sleep(random.randint(1,3))
        continue
    is_success = save_book_info(book_info)
    # 如果保存书名的时候出错,直接退出本次循环
    if not is_success:
        print(datetime.datetime.now())
        print("save book faile ,exit this one")
        time.sleep(random.randint(1,3))
        continue
    try:
        get_chapter_by_book_info(book_info)
        time.sleep(random.randint(1,3))
    except Exception as e:
        print(datetime.datetime.now())
        print("save chapter info fail")
        print(e)
        time.sleep(random.randint(1,3))
        continue

    # 记录结束时间
    end_time = time.time()
    cost_time = end_time - start_time
    print(datetime.datetime.now())
    print("cost time is :%s" % cost_time)
