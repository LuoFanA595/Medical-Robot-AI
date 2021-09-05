#基于scrapy框架的医疗问答  

### 更换路径  

    docter.py   
    with open(r'Medical_Spider_API/QA/question.txt','r',encoding='utf-8') as f:

    pipeline.py  
    savepath = r'QA\Answer.txt
    
    Spider_open.py  
    with open(r'Medical_Spider_API/QA/question.txt','w',encoding='utf-8') as f:
    with open(r'Medical_Spider_API/QA/Answer.txt','r',encoding='utf-8') as fr:
    
    
### 更改本机IP地址

    Spider_open.py
    在本地运行cmd输入命令ipconfig查询本机IPV4地址即可

### 调用

    Spoder_open.py  
    开启api后通过api访问

### 更改输出格式

    pipeline.py  
    更改answer


