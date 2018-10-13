import hashlib
import base64
import urllib.parse
import re
from django.conf import settings


def get_md5(t):
    if isinstance(t, str):
        t = t.encode("utf-8")
    m = hashlib.md5()
    m.update(t)
    return m.hexdigest()

def encryption_urllib_base64(v):
    """
    加密
    """
    s = bytes(v, encoding="utf8")
    s = base64.b64encode(s)
    s = str(s, encoding="utf-8")
    return urllib.parse.quote(s)


def decrypt_urllib_base64(v):
    s = urllib.parse.unquote(v)
    s = bytes(s, encoding="utf8")
    s = base64.b64decode(s)
    return str(s, encoding="utf-8")

# 过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile(
        '<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',
        re.I)  # Script
    re_style = re.compile(
        '<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',
        re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    re_stopwords = re.compile('\u3000')  # 去除无用的'\u3000'字符
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    s = re_stopwords.sub('', s)
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s

# 替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr



def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

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

def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str


def guolv_content(content):

    try:
        if not settings.OPEN_GL:
            return content
        f = open('./wj.txt', "r", encoding=u'utf-8', errors='ignore')
        while True:
            line = f.readline()
            line = line.strip()
            if line:
                arr = line.split('|')
                content = content.replace(arr[0],arr[1])
            if not line:
                break

        return content

    except Exception as e:
        print(e)

    finally:
        if f:
            f.close()

if __name__ == '__main__':
    a = """
    48岁的兽欲，去年12月27日再婚，迎娶比自己年轻22岁的北京嫩模张伟铃。鼓手大婚，Beyond另外两位成员家强和黄贯中却未获通知。其实Beyond三人心病，早在三年前种下，当时叶世荣到内地发展，经常以Beyond名义在内地开唱，黄家强直指对方借Beyond发财，两人从此无联系;至于黄家强和黄贯中，2009年抛弃叶世荣在香港开唱后，竟为一首歌意见有分歧，在酒吧大打出手，俨如《天与地》真实版。一起唱歌很有默契，却没办法好好相处，昔日肝胆相照的好兄弟，今日各走各路。

    有指对叶世荣最不满的黄家强，去年两人不约而同在黄家驹生忌(6月19日)前往拜祭，却刚好撞见，两个互当透明未有交谈。“那时候他们骂世荣的话真的好难听，但其实黄贯中、黄家强现在都有用Beyond的名义去内地演出，也一样有唱Beyond的歌!其实大家各做各的，应该互相体谅。”叶世荣身边好友说。事实上，近年工作量没多少的黄家强，因为身家丰厚，根本没经济压力。

    2009年7月，黄家强决定和阿Paul “复合”开唱，抛弃叶世荣。“他们两个搞双星Rock n Roll Live，也一样唱Beyond的歌，他们以为可以安然无恙，谁知道开完Rock n Roll Live，二人竟因为合作出唱片问题，为一首歌出现意见分歧，在尖沙咀一间酒吧大打出手。“家强还气到拿起椅子扔到黄贯中那，推推撞撞打烂了很多东西，黄贯中又学过泰拳，还好有朋友拉开大家才没受伤，不过两人却翻脸了!”知情者说。

    Beyond由地下穷乐队，到现在成为乐队界一哥，多年友情全靠黄家驹维系，但自从失去灵魂人物，黄家强黄贯中经常因音乐路向各异而吵架，昔日好兄弟情已不再，歌迷想Beyond为三十周年开唱，难!

    1983年黄家驹、叶世荣与其他成员组成Beyond，参加吉他比赛得冠军，以玩票性质组成乐队，直至1983年黄家强加入，Beyond正式成型，亦在1985年自资搞“永远等待演唱会”及出唱片，同年阿Paul(黄贯中)才加入。

    1987年当时Beyond有五位成员，除黄家驹、黄家强、黄贯中、叶世荣，还有刘志远， 1987年推出首张EP《永远等待》，正式踏入主流乐坛。1988年刘志远退出，四人Beyond签约新艺宝，作品《喜欢你》、《大地》大受欢迎。

    1989年推出大碟《真的爱你》及《Beyond IV》，以及1990年专辑《命运派对》，共获五白金销量(25万张)，先后在新伊馆及红馆举行十多场演唱会，其后更到台湾以及马来西亚等地发展，是Beyond的光辉时期。


    """
    print(guolv_content(a))