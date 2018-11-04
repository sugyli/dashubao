import MySQLdb
import MySQLdb.cursors as cursors
from xpinyin import Pinyin



p = Pinyin()

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def format_str(content):
    quanping = ''
    slug = ''
    iswenzi = False
    for i in content:
        if is_chinese(i):
            iswenzi = True
            i = p.get_pinyin(u"%s"%i)
            quanping = quanping+i + ' '
            slug = slug+i + '-'

        elif is_alphabet(i):
            quanping = quanping + i
            slug = slug + i

        elif is_number(i):
            quanping = quanping + i
            slug = slug + i

    slug = slug.strip()
    return quanping.strip(),slug.rstrip('-'),iswenzi





try:

    conn = MySQLdb.connect(
        host='60.171.117.207',
        user='cbscbx',
        passwd='chenbenshouchenbenxing5566778899',
        db='shubao',
        charset='utf8',
        cursorclass=cursors.SSCursor)
    conn2 = MySQLdb.connect(
        host='60.171.117.207',
        user='cbscbx',
        passwd='chenbenshouchenbenxing5566778899',
        db='shubao',
        charset='utf8')

    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    # 使用execute方法执行SQL语句
    #cursor.execute('set global max_allowed_packet = 67108864')
    cursor.execute(
        "select * from novels_noveldetail where novel_old_id > 0 and novel_old_id<= 98000 order by novel_old_id asc")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()

    batch_size = 1000

    while True:

        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了')
            break
        else:
            for item in data:
                novel_name = item[3]
                #slug = item[4]
                #quanping = item[5]

                url_md5 = item[2]
                quanping,slug,iswenziname= format_str(novel_name)
                novel_old_id = item[11]
                


                sql = """
                 update novels_noveldetail set slug = %s , quanping = %s , caiji_url_md5 = %s ,stop_update = 0 ,iswenziname = %s where novel_old_id = %s

                 """
                params = (slug,quanping,url_md5,iswenziname,novel_old_id)
                cursor2.execute(sql, params)
                conn2.commit()
                print('%s 更新成功' % novel_old_id)

except Exception as e:
    print(e)


# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()