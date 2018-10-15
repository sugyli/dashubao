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
import urllib.parse
import base64
# def encryption_urllib_base64(v):
#     """
#     加密
#     """
#     s = bytes(v, encoding="utf8")
#     s = base64.b64encode(s)
#     s = str(s, encoding="utf-8")
#     return urllib.parse.quote(s)
#
#
# def decrypt_urllib_base64(v):
#     s = urllib.parse.unquote(v)
#     s = bytes(s, encoding="utf8")
#     s = base64.b64decode(s)
#     return str(s, encoding="utf-8")
#
# a = """
# 48岁的叶世荣，去年12月27日再婚，迎娶比自己年轻22岁的北京嫩模张伟铃。鼓手大婚，Beyond另外两位成员家强和黄贯中却未获通知。其实Beyond三人心病，早在三年前种下，当时叶世荣到内地发展，经常以Beyond名义在内地开唱，黄家强直指对方借Beyond发财，两人从此无联系;至于黄家强和黄贯中，2009年抛弃叶世荣在香港开唱后，竟为一首歌意见有分歧，在酒吧大打出手，俨如《天与地》真实版。一起唱歌很有默契，却没办法好好相处，昔日肝胆相照的好兄弟，今日各走各路。
#
# 有指对叶世荣最不满的黄家强，去年两人不约而同在黄家驹生忌(6月19日)前往拜祭，却刚好撞见，两个互当透明未有交谈。“那时候他们骂世荣的话真的好难听，但其实黄贯中、黄家强现在都有用Beyond的名义去内地演出，也一样有唱Beyond的歌!其实大家各做各的，应该互相体谅。”叶世荣身边好友说。事实上，近年工作量没多少的黄家强，因为身家丰厚，根本没经济压力。
#
# 2009年7月，黄家强决定和阿Paul “复合”开唱，抛弃叶世荣。“他们两个搞双星Rock n Roll Live，也一样唱Beyond的歌，他们以为可以安然无恙，谁知道开完Rock n Roll Live，二人竟因为合作出唱片问题，为一首歌出现意见分歧，在尖沙咀一间酒吧大打出手。“家强还气到拿起椅子扔到黄贯中那，推推撞撞打烂了很多东西，黄贯中又学过泰拳，还好有朋友拉开大家才没受伤，不过两人却翻脸了!”知情者说。
#
# Beyond由地下穷乐队，到现在成为乐队界一哥，多年友情全靠黄家驹维系，但自从失去灵魂人物，黄家强黄贯中经常因音乐路向各异而吵架，昔日好兄弟情已不再，歌迷想Beyond为三十周年开唱，难!
#
# 1983年黄家驹、叶世荣与其他成员组成Beyond，参加吉他比赛得冠军，以玩票性质组成乐队，直至1983年黄家强加入，Beyond正式成型，亦在1985年自资搞“永远等待演唱会”及出唱片，同年阿Paul(黄贯中)才加入。
#
# 1987年当时Beyond有五位成员，除黄家驹、黄家强、黄贯中、叶世荣，还有刘志远， 1987年推出首张EP《永远等待》，正式踏入主流乐坛。1988年刘志远退出，四人Beyond签约新艺宝，作品《喜欢你》、《大地》大受欢迎。
#
# 1989年推出大碟《真的爱你》及《Beyond IV》，以及1990年专辑《命运派对》，共获五白金销量(25万张)，先后在新伊馆及红馆举行十多场演唱会，其后更到台湾以及马来西亚等地发展，是Beyond的光辉时期。
#
#
# """
# a = encryption_urllib_base64(a)
#
# print(a)
#
# print('------------我是分割线-------------')
#
# a = decrypt_urllib_base64(a)
#
# print(a)

t = ('wo','ni','ta')
a ,*o = t
print(a,o)