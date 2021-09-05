# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class DocterspiderPipeline:
    def process_item(self, item, spider):
        '''
        获得字段  组成回答语句进行输出

        :param item:
        :param spider:
        :return:
        '''
        propose = item['propose']
        print(propose)
        drugs = item['drugs']
        introduce = item['introduce']
        Price = item['Price']
        savepath = r'Medical_Spider_API/QA/Answer.txt'
        answer = propose + "\n推荐您使用:" + "|"+drugs[0]+"|" + "\n功效:" + introduce[0] + "\n价格:" + Price[0]
        with open(savepath,'w',encoding='utf-8') as f:
            f.write(answer)
        return item