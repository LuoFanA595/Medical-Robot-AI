from flask import Flask, request
import json
import subprocess

app = Flask(__name__)


# 只接受POST方法访问
@app.route("/Answer", methods=["POST"])
def check():
    # 默认返回内容
    return_dict = {'statusCode': '200', 'message': 'successful!', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['statusCode'] = '5004'
        return_dict['message'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    get_data = request.get_data()  # 获取传入的参数
    get_data = json.loads(get_data)  # 传入的参数为bytes类型，需要转化成json
    questions = get_data.get('question')
    with open(r'D:\PycharmProjects\Medical_Robot_Rasa\Medical_Spider_API\QA\question.txt', 'w', encoding='utf-8') as f:
        f.write(questions)
    spider_name = "docter"
    subprocess.check_output(['scrapy', 'crawl', spider_name])
    with open(r'D:\PycharmProjects\Medical_Robot_Rasa\Medical_Spider_API\QA\Answer.txt', 'r', encoding='utf-8') as fr:
        answer = fr.read()
    dict = {'1': answer}
    json1 = json.dumps(dict, ensure_ascii=False)
    return json1


if __name__ == "__main__":

    app.run('172.27.96.1', port=8888, debug=True)
