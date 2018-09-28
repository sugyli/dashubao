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
def str_gl(str):
    str = str.strip()
    str = remove_tags(str)
    str = help.filter_tags(str)
    if str:
        str = str.split("\n")
        str = [
            '<p>' + item.strip() +
            '</p><br />' for item in str if item.strip()]
        str = "".join(str)
        #str = str.rstrip('<br />')


    return str

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
    cursor.execute('set global max_allowed_packet = 67108864')
    cursor.execute(
        "select * from jieqi_article_article where lastchapterid > 0  order by articleid asc LIMIT 200")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()

    count = 0
    batch_size = 100

    while True:
        count = count + 1
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了')
            break
        else:
            for item in data:
                print('id %s book %s 的数据 准备添加'%(item[0],item[4]))
                sql = """
                 insert into novels_noveldetail(url,url_md5,image, novel_status,novel_name,novel_author,novel_info,novel_old_id,novel_comefrom,create_time,update_time,novel_fav_nums,novel_zan_nums,novel_click_nums,novelclassify_id,ishide)
                     VALUES (%s,%s, %s, %s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE novel_name=VALUES(novel_name),image=VALUES(image),create_time=VALUES(create_time),update_time=VALUES(update_time)
                
                 """


                a = 'https://www.dashubao.net/book/%d/%d'%(item[0]//1000,item[0])
                b = get_md5(a)
                if int(item[47]):
                    c = 'oldfenmian/%d/%d/%ds.jpg' % (item[0] // 1000, item[0], item[0])
                else:
                    c = ''

                if int(item[46]):
                    d = True
                else:
                    d = False


                c_d =  datetime.fromtimestamp(item[2]).strftime("%Y-%m-%d %H:%M:%S")
                p_d = datetime.fromtimestamp(item[3]).strftime("%Y-%m-%d %H:%M:%S")

                params = (a, b, c,d,item[4], item[8], str_gl(item[15]), item[0],'88读书',c_d,p_d,0,0,0,0,0)

                cursor2.execute(sql, params)

                # 提交到数据库执行
                conn2.commit()
                print('%s 的数据入库成功'%item[4])


        print('获取%s到%s数据成功' % ((count - 1) * batch_size, count * batch_size-1))
        print('fetchmany获取全量数据所用时间:', (datetime.now() - start_time).seconds)

except Exception as e:
    print(e)
    conn2.rollback()


# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()