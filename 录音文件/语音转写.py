import urllib.request
import urllib
import json
import base64


class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        # 语音合成的resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib.request.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getText(self, filename):
        # 2. 向Rest接口提交数据
        data = {}
        # 语音的一些参数
        data['format'] = 'wav'
        data['rate'] = 16000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(self.upvoice_url,data=bytes(post_data,encoding="utf-8")).read()
        print(r_data)
        return json.loads(r_data)['result']

if __name__ == "__main__":
     #上面得到的API key与Screct Key,替换为自己的即可
    api_key = "B861swYYURVSSK7HwL85npGv"
    api_secert = "nQ0ZovxkyrecAycItr9zNlQyVGD5olxI"
    # 初始化
    bdr = BaiduRest("test_python", api_key, api_secert)
    # 识别test.wav语音内容并显示
    print(bdr.getText(r"D:\pycharm\python15\rasa_医疗\录音文件\input.wav"))
