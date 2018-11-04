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
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='xiaoshubao',
        charset='utf8',
        cursorclass=cursors.SSCursor)

    conn2 = MySQLdb.connect(
        host='60.171.117.207',
        user='cbscbx',
        passwd='chenbenshouchenbenxing5566778899',
        db='shubao',
        charset='utf8')
    conn3 = MySQLdb.connect(
        host='60.171.117.207',
        user='cbscbx',
        passwd='chenbenshouchenbenxing5566778899',
        db='shubao',
        charset='utf8')
    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    cursor3 = conn3.cursor()
    # 使用execute方法执行SQL语句
    cursor3.execute(
        "select * from novels_noveldetail where novel_old_id > 91290 and novel_old_id<=94999   order by novel_old_id asc limit 20000")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()
    #cursor.execute('set global wait_timeout=600000')
    cursor.execute('set global max_allowed_packet = 67108864')
    batch_size = 5000
    while True:
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor3.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了------1')
            break
        else:
            for item in data:

                print('查询到oid %s 书名 %s 的数据 准备添加章节' % (item[11], item[3]))
                cursor.execute(
                    "select * from jieqi_article_chapter where articleid =%d and chaptertype = 0  order by chapterorder asc"%item[11])
                count = 1
                while True:
                    chapterdata = cursor.fetchmany(batch_size)
                    if not chapterdata:
                        count = 1
                        print('没有章节数据了-------2')
                        break
                    else:

                        for i, v in enumerate(chapterdata):

                            print('添加章节 %s 入库 %s' % (v[9],item[11]))

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
                                v[9], count, 0, c_d, p_d, url, md5_url, item[2], 0, v[0])
                            cursor2.execute(sql, params)
                            # get_chapter_insert_id = cursor2.execute("select LAST_INSERT_ID()")
                            cursor2.execute("select chapter_url_md5 from novels_novelchapter where chapter_url_md5 = %s", [md5_url])

                            get_chapter_insert_id = cursor2.fetchone()[0]

                            # if count == 1:
                            #     cursor2.execute("update novels_noveldetail SET first_chapter_addr=%s where url_md5 = %s ",(md5_url,item[2]))

                            try:
                                path = '/Users/sugyil/Downloads/txt/%d/%d/%d.txt' % (item[11] // 1000, item[11], v[0])
                                with open(path, 'r', encoding='gbk') as f:

                                    t = f.read()
                                    t, num = str_count(t)
                                    if num > 0:
                                        sql2 = """
                                                insert into novels_novelcontent(content,content_url,content_url_md5,create_time,update_time,num_words,comefrom_id,ishide) VALUES (%s,%s, %s, %s ,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(content),content_url=VALUES(content_url),content_url_md5=VALUES(content_url_md5),create_time=VALUES(create_time),update_time=VALUES(update_time),num_words=VALUES(num_words)

                                             """
                                        md5_url2 = get_md5(path)
                                        params2 = (t, path, md5_url2, c_d, p_d, num, 97, 0)
                                        cursor2.execute(sql2, params2)

                                        cursor2.execute("select content_url_md5 from novels_novelcontent where content_url_md5 = %s",[md5_url2])

                                        get_content_insert_id = cursor2.fetchone()[0]

                                        sql3 = """
                                                insert into novels_chaptercontent(novelcontent_id,novelchapter_id,create_time) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE novelcontent_id=VALUES(novelcontent_id),novelchapter_id=VALUES(novelchapter_id)

                                            """

                                        params3 = (get_content_insert_id, get_chapter_insert_id,c_d)
                                        cursor2.execute(sql3, params3)
                                        print('%s 添加本章节内容成功'%item[11])
                                    else:
                                        print('内容为空不添加')

                            except Exception as e:
                                print('TXT丢失 ', e)
                                with open('/Users/sugyil/Downloads/txt/log.txt', 'a+') as f:
                                    f.write(path + 'TXT丢失2\t\n')
                                # if count == 1:
                                #     with open('/Users/sugyil/Downloads/txt/log.txt', 'a+') as f:
                                #         f.write(path + 'TXT丢失1\t\n')
                                # else:
                                #     with open('/Users/sugyil/Downloads/txt/log.txt', 'w+') as f:
                                #         f.write(path + 'TXT丢失2\t\n')

                            finally:
                                if f:
                                    f.close()

                            conn2.commit()
                            count += 1

                print('%s 的章节数据添加完成' % item[11])

except Exception as e:
    print(e)
    conn2.rollback()


# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()

cursor3.close()
conn3.close()





