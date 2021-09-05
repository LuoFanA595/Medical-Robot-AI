import scrapy
import sys
import os
import re
import pandas as pd
from docterSpider.items import DocterspiderItem
# from open_api import ask
# from test__ import test_ask

class DocterSpider(scrapy.Spider):
    '''
    爬取有问必答网站 根据用户输入的问题进行对应返回网页进行爬取
    网址 ： ’https://www.120ask.com/‘
    '''
    name = 'docter'
    allowed_domains = ['120ask.com']
    with open(r'D:\PycharmProjects\Medical_Robot_Rasa\Medical_Spider_API\QA\question.txt','r',encoding='utf-8') as f:
        inputs = f.read()
    # inputs = input('请输入')

    start_urls = ['http://so.120ask.com/?kw=' + inputs]
    #第一层爬虫 根据用户输入数据进行返回页面查询
    def parse(self, response):
        try:
            respo = re.split('https', str(response.body))[4]
        except:
            print('没有查询到您的病症')
            os._exit(0)
        respo = re.findall('www.*htm',respo)
        urlll = 'https://' + respo[0]
        #嵌套爬取 返回查询出的网页的具体页面
        return scrapy.Request(urlll,callback=self.parses,dont_filter=True)
    #第二层爬虫 爬取用户问题问题的具体回答
    def parses(self,response):

        item = DocterspiderItem()
        #设置 有关医生回答的返回字段 propose ，helpCount ，greet
        valueDict = {
            'propose':[],
            'helpCount':[],
            'greet':[]
        }
        # for each in response.xpath('//div[@class="crazy_new"]'):
        #     Condition_analysis = str(each.xpath("p/text()").extract()[0])
        #     # Condition_analysis = ' '.join(each.xpath('/p/text()'))
        #     print('1',Condition_analysis)
        #     Condition_analysis = Condition_analysis.strip('\xa0')
        #     valueDict['propose'].append(Condition_analysis)
        #对数据进行数据处理
        for each2 in response.xpath('//div[@class = "b_anscont_cont"]'):
            Condition_analysis_ = each2.xpath("div/p/text()").extract()
            if Condition_analysis_ == []:
                Condition_analysis_ = str(each2.xpath("p/text()").extract()[0])
            else:
                Condition_analysis_ = "".join(word.strip('\xa0') for word in Condition_analysis_)
            # print(type(Condition_analysis_))
            Condition_analysis_ = Condition_analysis_.strip('\xa0')
            # print('1', Condition_analysis_)
            valueDict['propose'].append(Condition_analysis_)
        count=0
        #识别的对应回答的 点赞数 和 帮助网友数
        for each1 in response.xpath('//span[@class="b_sp2"]'):
            greet = each1.xpath("i[@class='b_gico']/following::text()[1]").extract()
            helpcount = each1.xpath("i[@class='b_hico']/following::text()[1]").extract()
            print(greet)
            print(helpcount)
            if count%2 != 0:
                helpcount = str(helpcount[0]).strip()
                helpcount = int(helpcount.split('：')[1])
                valueDict['helpCount'].append(helpcount)
                if greet != []:
                    greet = str(greet[0]).strip()
                    greet = int(greet.split('：')[1])
                    valueDict['greet'].append(greet)
                elif greet == []:
                    valueDict['greet'].append(0)
            count += 1
        if len(valueDict['propose'])!=len(valueDict['greet']):
            rangcount = len(valueDict['propose']) - len(valueDict['greet'])
            for i in range(rangcount):
                valueDict['greet'].append(0)
        if len(valueDict['propose'])!=len(valueDict['helpCount']):
            rangcount = len(valueDict['propose']) - len(valueDict['helpCount'])
            for i in range(rangcount):
                valueDict['helpCount'].append(0)
        print(len(valueDict['propose']),len(valueDict['greet']), len(valueDict['helpCount']))
        # print(valueDict['propose'],valueDict['greet'],valueDict['helpCount'])

        #生成DataFrame数据格式
        #对输入数据进行判断 优先选择点赞数多，其次选择帮助网友人数多的  点赞数 > 帮助网友数
        valuepd = pd.DataFrame(valueDict)
        if len(valuepd[valuepd['greet'] == valuepd['greet'].max()]['greet'].values) > 1:
            if len(valuepd[valuepd['helpCount'] == valuepd['helpCount'].max()]['helpCount'].values) > 1:
                best = valuepd[valuepd['helpCount'] == valuepd['helpCount'].max()]['propose'].values[0]
            else:
                best = valuepd[valuepd['helpCount'] == valuepd['helpCount'].max()]['propose'].values
        else:
            best = valuepd[valuepd['greet'] == valuepd['greet'].max()]['propose'].values
        # print(best[0])
        item['propose'] = best[0]
        recommend = {
            'drugs':[],
            'introduce':[],
            'Price':[]
        }
        # 爬取 药品名称  药品信息 药品价格
        for each3 in response.xpath('//dl[@class="clears yaopin_gg"]'):
            drugs = each3.xpath("dd/p[@class='p1']/b/a/text()").extract()
            introduce = each3.xpath("dd/p[@class='p2']/text()").extract()
            Price = each3.xpath("dd/p[@class='p3 clears']/span/b/text()").extract()
            recommend['drugs'].append(drugs[0])
            recommend['introduce'].append(introduce[0])
            recommend['Price'].append(Price[0])
        item['drugs'] = recommend['drugs']
        item['introduce'] = recommend['introduce']
        item['Price'] = recommend['Price']
        # 返回字段
        return item
