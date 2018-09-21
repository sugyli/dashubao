import MySQLdb
import MySQLdb.cursors as cursors
from datetime import datetime
import hashlib
from w3lib.html import remove_tags

import help

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def str_count(str):
    str = str.strip()
    str = remove_tags(str)
    str = help.filter_tags(str)
    c = 0
    if str:
        str = str.split("\n")
        str = [
            '<p>' + item.strip() +
            '</p><br />' for item in str if item.strip()]
        str = "".join(str)
        #str = str.rstrip('<br />')

        for s in str:
            # 中文字符范围
            if '\u4e00' <= s <= '\u9fff':
                c += 1

    return str , c


try:
    # 开始时间
    start_time = datetime.now()
    print(start_time)
    conn = MySQLdb.connect(
        host='98.126.65.66',
        user='root',
        passwd='chenbenshouchenbenxing!@#123',
        db='xiaoshubao',
        charset='utf8',
        cursorclass=cursors.SSCursor)

    conn2 = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        db='dashubao',
        charset='utf8')
    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    # 使用execute方法执行SQL语句
    cursor2.execute(
        "select * from novels_noveldetail  order by id asc")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()
    #cursor.execute('set global wait_timeout=600000')
    cursor.execute('set global max_allowed_packet = 67108864')
    count = 0
    batch_size = 100
    while True:
        count = count + 1
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor2.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了')
            break
        else:
            for item in data:
                print('查询到id %s 书名 %s 的数据 准备添加章节' % (item[0], item[3]))
                cursor.execute(
                    "select * from jieqi_article_chapter where articleid =%d and chaptertype = 0  order by chapterorder asc" %
                    (item[10]))
                count = 1
                while True:

                    chapterdata = cursor.fetchmany(batch_size)
                    if not chapterdata:
                        count = 1
                        print('没有章节数据了')
                        break
                    else:

                        for i, v in enumerate(chapterdata):

                            print('添加章节 %s 入库' % (v[9]))

                            sql = """
                                insert into novels_novelchapter(chapter_name,chapter_order,chapter_type, create_time,update_time,chapter_url,chapter_url_md5,noveldetail_id,ishide,chapter_old_id) VALUES (%s,%s, %s, %s ,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE chapter_name=VALUES(chapter_name),chapter_order=VALUES(chapter_order),create_time=VALUES(create_time),update_time=VALUES(update_time),chapter_url=VALUES(chapter_url),chapter_url_md5=VALUES(chapter_url_md5)

                             """

                            c_d = datetime.fromtimestamp(
                                v[7]).strftime("%Y-%m-%d %H:%M:%S")
                            p_d = datetime.fromtimestamp(
                                v[8]).strftime("%Y-%m-%d %H:%M:%S")

                            url = 'https://www.dashubao.net/book/%d/%d/%d.html' % (
                                v[2] // 1000, v[2], v[0])
                            md5_url = get_md5(url)

                            params = (
                                v[9], count, 0, c_d, p_d, url, md5_url, item[2],0,v[0])
                            cursor2.execute(sql, params)
                            #get_chapter_insert_id = cursor2.execute("select LAST_INSERT_ID()")
                            cursor2.execute("select id from novels_novelchapter where chapter_url_md5 = %s",[md5_url])

                            get_chapter_insert_id = cursor2.fetchone()[0]



                            # if count == 1:
                            #     cursor2.execute("update novels_noveldetail SET first_chapter_addr=%s where url_md5 = %s ",(md5_url,item[2]))

                            try:
                                path = '/Users/sugyil/txt/%d/%d/%d.txt'%(item[10]//1000,item[10],v[0])
                                with open(path, 'r',encoding='gbk') as f:

                                    t = f.read()
                                    t , num = str_count(t)
                                    if num > 0:
                                        sql2 = """
                                            insert into novels_novelcontent(content,content_url,content_url_md5,create_time,update_time,num_words,comefrom_id) VALUES (%s,%s, %s, %s ,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(content),content_url=VALUES(content_url),content_url_md5=VALUES(content_url_md5),create_time=VALUES(create_time),update_time=VALUES(update_time),num_words=VALUES(num_words)
    
                                         """
                                        md5_url2 = get_md5(path)
                                        params2 = (t,path,md5_url2,c_d,p_d,num,100)
                                        cursor2.execute(sql2, params2)


                                        cursor2.execute("select id from novels_novelcontent where content_url_md5 = %s",[md5_url2])
                                        get_content_insert_id = cursor2.fetchone()[0]

                                        sql3 = """
                                            insert into novels_novelcontent_chapter(novelcontent_id,novelchapter_id) VALUES (%s,%s) ON DUPLICATE KEY UPDATE novelcontent_id=VALUES(novelcontent_id),novelchapter_id=VALUES(novelchapter_id)

                                        """

                                        params3 = (get_content_insert_id,get_chapter_insert_id)
                                        cursor2.execute(sql3, params3)
                                        print('添加本章节内容成功')
                                    else:
                                        print('内容为空不添加')

                            except Exception as e:
                                print('TXT丢失 ',e)
                                if count == 1:
                                    with open('/Users/sugyil/txt/log.txt', 'a+') as f:
                                        f.write(path+'\t\n')
                                else:
                                    with open('/Users/sugyil/txt/log.txt', 'w+') as f:
                                        f.write(path+'\t\n')

                            finally:
                                if f:
                                    f.close()

                            conn2.commit()
                            count += 1

                print('%s 的章节数据添加完成' % item[4])

        print(
            '获取%s到%s数据成功' %
            ((count - 1) * batch_size, count * batch_size - 1))
        print('fetchmany获取全量数据所用时间:', (datetime.now() - start_time).seconds)

except Exception as e:
    print(e)
    conn2.rollback()


# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()
