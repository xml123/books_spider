import datetime

from config.read_sql import get_mysql_db

#保存作者和分类
def save_author_tag(one_book_dict):
    # 获取链接对象
    db = get_mysql_db()
    # 获取游标对象
    cursor = db.cursor()

    if not one_book_dict:
        return
    #获取作者
    book_author = one_book_dict.get('author')
    #获取分类
    book_tag = one_book_dict.get('kind')

    sql_author = 'SELECT id FROM books_author WHERE name="%s";' % book_author
    cursor.execute(sql_author)
    author_res = cursor.fetchone()

    sql_tag = 'SELECT id FROM books_category WHERE name="%s";' % book_tag
    cursor.execute(sql_tag)
    tag_res = cursor.fetchone()

    #执行存入数据库的操作
    if not author_res:  #判断数据库是否已存在该作者
        sql1 = r'INSERT into books_author (name) values("%s");' \
          % (book_author)
        cursor.execute(sql1)
        db.commit()

    if not tag_res:     #判断数据库是否已存在该分类
        sql2 = r'INSERT into books_category (name) values("%s");' \
          % (book_tag)
        cursor.execute(sql2)
        db.commit()
    
    try:
        print(datetime.datetime.now())
        print("保存作者和分类成功")
        cursor.close()
        db.close()
        return 1
    except:
        db.rollback()
        print(datetime.datetime.now())
        print("保存作者和分类失败")
        cursor.close()
        db.close()
        return 0

# 保存书本信息到数据库
def save_book_info(one_book_dict):
    # 获取链接对象
    db = get_mysql_db()
    # 获取游标对象
    cursor = db.cursor()

    if not one_book_dict:
        return
    # 获取书名
    book_name = one_book_dict.get('name')

    if_book = 'SELECT id FROM books_book WHERE title="%s";' % book_name
    cursor.execute(if_book)
    book_bull = cursor.fetchone()
    if book_bull:
        print('该书已存在')
        return 0

    # 获取书本的url
    book_url = one_book_dict.get('url')
    # 获取书本的封面图
    book_img = one_book_dict.get('img')
    #获取作者
    book_author = one_book_dict.get('author')
    #获取分类
    book_tag = one_book_dict.get('kind')
    #获取简介
    book_abstract = one_book_dict.get('abstract')
    # 获取书本的分类
    book_tag_id = get_tag_id_by_name(book_tag)
    # 获取书本的作者
    book_author_id = get_author_id_by_name(book_author)
    #创建时间
    #create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print('time',create_time)
    # 执行存入数据库的操作
    sql = r'INSERT into books_book (title,url,book_img,category_id,author_id,book_abstract) values("%s","%s","%s",%d,%d,"%s");' \
          % (book_name,book_url,book_img,book_tag_id,book_author_id,book_abstract)
    try:
        cursor.execute(sql)#保存书本信息
        db.commit()
        print(datetime.datetime.now())
        print("success save books_book")
        cursor.close()
        db.close()
        return 1
    except:
        db.rollback()
        print(datetime.datetime.now())
        print("rollback once")
        cursor.close()
        db.close()
        return 0

# 根据书名获取数据库中的id
def get_book_id_by_name(book_name):
    db = get_mysql_db()
    cursor = db.cursor()

    sql = 'SELECT id FROM books_book WHERE title="%s";' % book_name

    cursor.execute(sql)

    res = cursor.fetchone()

    cursor.close()
    db.close()

    if res:
        return res[0]
    else:
        return 0

# 根据作者获取数据库中的id
def get_author_id_by_name(author_name):
    db = get_mysql_db()
    cursor = db.cursor()

    sql = 'SELECT id FROM books_author WHERE name="%s";' % author_name

    cursor.execute(sql)

    res = cursor.fetchone()

    cursor.close()
    db.close()

    if res:
        return res[0]
    else:
        return 0

# 根据分类获取数据库中的id
def get_tag_id_by_name(tag_name):
    db = get_mysql_db()
    cursor = db.cursor()

    sql = 'SELECT id FROM books_category WHERE name="%s";' % tag_name

    cursor.execute(sql)

    res = cursor.fetchone()

    cursor.close()
    db.close()

    if res:
        return res[0]
    else:
        return 0


# 根据book_id,查询数据库并更改has_chapter的值设为0
def set_book_has_chapter_by_id(book_id):
    db = get_mysql_db()
    cursor = db.cursor()
    sql = r'update books_book set has_chapter=0  where id=%s;' % book_id
    try:
        cursor.execute(sql)
        db.commit()
        print(datetime.datetime.now())
        print("set has_chapter value success")
    except:
        db.rollback()

    cursor.close()
    db.close()


# 根据one_chapter字典保存信息到chapter表中
def save_chapter(one_chapter):
    # 获取传值
    book_id = one_chapter.get("book_id")
    name = one_chapter.get("name")
    chapter_url = one_chapter.get("href")
    chapter_text = one_chapter.get('data')
    chapter_id = one_chapter.get('chapter_id')
    # 获取db
    db = get_mysql_db()
    cursor = db.cursor()
    sql = r"INSERT INTO books_chapter (book_id_id,name,chapter_url,chapter_text,chapter_id) VALUES(%s,'%s','%s','%s','%s');" \
          % (book_id, name, chapter_url, chapter_text,chapter_id)
    try:
        cursor.execute(sql)
        db.commit()
        print(datetime.datetime.now())
        print("success save one chapter")
    except:
        db.rollback()

    cursor.close()
    db.close()
