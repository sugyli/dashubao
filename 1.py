# import base64
#
# print(base64.b64encode(b"aaa")) #base64加密
# print (base64.b64decode("YWFh")) #base64解密

# import urllib.parse
# values={}
# values['username']='02蔡彩虹'
# values['password']='ddddd?'
# url="http://www.baidu.com"
# data=urllib.parse.urlencode(url)
# print(data)


# import urllib.parse
# s='长春'
# s=urllib.parse.quote(s)
# print(s)

mylist = [1,2,2,2,2,3,3,3,4,4,4,4,2,5]
myset = set(mylist) #myset是另外一个列表，里面的内容是mylist里面的无重复 项
print(myset)