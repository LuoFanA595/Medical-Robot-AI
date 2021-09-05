'''
详情见http://api.qingyunke.com/
智能机器人API接口说明
支持功能：天气、翻译、藏头诗、笑话、歌词、计算、域名信息/备案/收录查询、IP查询、手机号码归属、人工智能聊天
接口地址：http://api.qingyunke.com/api.php?key=free&appid=0&msg=关键词
　　　　　key　固定参数free
　　　　　appid 设置为0，表示智能识别，可忽略此参数
　　　　　msg　关键词，请参考下方参数示例，该参数可智能识别，该值请经过 urlencode 处理后再提交
返回结果：{"result":0,"content":"内容"}
　　　　　result　状态，0表示正常，其它数字表示错误
　　　　　content　信息内容
想要学习Python？Python学习交流群：1136201545满足你的需求，资料都已经上传群文件，可以自行下载！
'''
import urllib.request
import time
import ssl
import json
import string
import jieba


def talk(keyword):
    target = r'http://api.qingyunke.com/api.php?key=free&appid=0&msg='
    while True:
        if keyword == "exit":
            return "不聊算了，拜拜"
        else:
            tmp = target + keyword
            url = urllib.parse.quote(tmp, safe=string.printable)
            page = urllib.request.urlopen(url)

            html = page.read().decode("utf-8")

            res = json.loads(html)
            list = jieba.cut(res['content'], cut_all=False)

            jieba.add_word('菲菲')
            answers = ''
            for i in list:
                if i == '菲菲':
                    i = 'Friday'
                    answers += i
                else:
                    answers += i
            return answers.replace('{br}','\n').replace('&quot;','"')
