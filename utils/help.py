import hashlib
import base64
import urllib.parse
import re
import os

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
    if not settings.OPEN_GL:
        return content
    path = os.path.join(settings.BASE_DIR, 'wj.txt')
    wenjian = open(path, "r", encoding=u'utf-8', errors='ignore')
    while True:
        line = wenjian.readline()
        line = line.strip()
        if line:
            arr = line.split('|')
            content = content.replace(arr[0], arr[1])
        if not line:
            break
    wenjian.close()
    return content

# if __name__ == '__main__':
