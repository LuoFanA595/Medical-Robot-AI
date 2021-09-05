# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
import json
from datetime import datetime
from typing import Any, Dict, List, Text, Optional
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime, date, timedelta

from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)
import jieba
from actions.api import question_parser
from actions.api import answer_search
from actions.api import Spider_open
from actions.api import weather
from actions.api import app
import subprocess
import datetime

USER_INTENT_OUT_OF_SCOPE = "out_of_scope"
import logging

logger = logging.getLogger(__name__)


class FindTheCorrespondingDisease(Action):
    def name(self) -> Text:
        return "FindTheCorrespondingDisease"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        disease = tracker.get_slot('disease')  # 获取疾病实体'
        print(disease)
        intentions = tracker.get_intent_of_latest_message()  # 获取意图
        if type(disease) != list:
            data = {'args': {disease: ['disease']}, 'question_types': [intentions]}
        else:
            data = {'args': {disease[0]: ['disease']}, 'question_types': [intentions]}
        parser = question_parser.QuestionPaser()
        searcher = answer_search.AnswerSearcher()
        print(data)
        sqls = parser.parser_main(data)  # 生成相关的查询语句
        print(sqls)
        final_answer = searcher.search_main(sqls)  # 查询相关内容
        print(final_answer)
        #  进行判断 输出结果
        if not final_answer:
            dispatcher.utter_message(template='utter_out')
            dispatcher.utter_message(template='utter_out1')
            try:
                if type(disease) != list:
                    data = Spider_open.open_s(disease[0])
                else:
                    data = Spider_open.open_s(disease)
                data = data.split('"')[3]
                dispatcher.utter_message(text=data)
            except Exception as e:
                print(e, '阿法师打发')
                dispatcher.utter_message(template='utter_exception')
        else:
            answer = '\n'.join(final_answer)
            print(answer)
            dispatcher.utter_message(text=answer)
        return [SlotSet('disease', None)]


class FindTheCorrespondingSymptom(Action):
    def name(self) -> Text:
        return "FindTheCorrespondingSymptom"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:

        symptom = tracker.get_slot("symptom")  # 获取症状实体'
        print(symptom)
        intentions = tracker.get_intent_of_latest_message()  # 获取意图
        if type(symptom) != list:
            data = {'args': {symptom: ['symptom']}, 'question_types': [intentions]}
        else:
            data = {'args': {symptom[0]: ['symptom']}, 'question_types': [intentions]}

        parser = question_parser.QuestionPaser()
        searcher = answer_search.AnswerSearcher()

        sqls = parser.parser_main(data)  # 生成相关的查询语句
        print(sqls)
        final_answer = searcher.search_main(sqls)  # 查询相关内容
        #  进行判断 输出结果
        if not final_answer:
            dispatcher.utter_message(template='utter_out')
            # dispatcher.utter_message(template='utter_out1')
            # data = Spider_open.open_s(symptom)
            # dispatcher.utter_message(text=data)
        else:
            answer = '\n'.join(final_answer)
            print(answer)
            dispatcher.utter_message(text=answer)
        return [SlotSet('symptom', None)]


class FindTheCorrespondingCheck(Action):
    def name(self) -> Text:
        return "FindTheCorrespondingCheck"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:

        check = tracker.get_slot("check")  # 获取检查项目实体

        intentions = tracker.get_intent_of_latest_message()  # 获取意图
        if type(check) != list:
            data = {'args': {check: ['check']}, 'question_types': [intentions]}
        else:
            data = {'args': {check[0]: ['check']}, 'question_types': [intentions]}

        parser = question_parser.QuestionPaser()
        searcher = answer_search.AnswerSearcher()

        sqls = parser.parser_main(data)  # 生成相关的查询语句
        print(sqls)
        final_answer = searcher.search_main(sqls)  # 查询相关内容
        #  进行判断 输出结果
        if not final_answer:
            dispatcher.utter_message(template='utter_out')
            # dispatcher.utter_message(template='utter_out1')
            # data = Spider_open.open_s(check)
            # dispatcher.utter_message(text=data)
        else:
            answer = '\n'.join(final_answer)
            print(answer)
            dispatcher.utter_message(text=answer)
        return [SlotSet('check', None)]


class FindTheCorrespondingDrug(Action):
    def name(self) -> Text:
        return "FindTheCorrespondingDrug"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        drug = tracker.get_slot("drug")  # 获取药物实体

        intentions = tracker.get_intent_of_latest_message()  # 获取意图
        if type(drug) != list:
            data = {'args': {drug: ['drug']}, 'question_types': [intentions]}
        else:
            data = {'args': {drug[0]: ['drug']}, 'question_types': [intentions]}

        parser = question_parser.QuestionPaser()
        searcher = answer_search.AnswerSearcher()

        sqls = parser.parser_main(data)  # 生成相关的查询语句
        print(sqls)
        final_answer = searcher.search_main(sqls)  # 查询相关内容
        #  进行判断 输出结果
        if not final_answer:
            dispatcher.utter_message(template='utter_out')
            # dispatcher.utter_message(template='utter_out1')
            # data = Spider_open.open_s(drug)
            # dispatcher.utter_message(text=data)
        else:
            answer = '\n'.join(final_answer)
            print(answer)
            dispatcher.utter_message(text=answer)
        return [SlotSet('drug', None)]


class FindTheCorrespondingFood(Action):
    def name(self) -> Text:
        return "FindTheCorrespondingFood"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        food = tracker.get_slot("food")  # 获取食物实体
        intentions = tracker.get_intent_of_latest_message()  # 获取意图
        if type(food) != list:
            data = {'args': {food: ['food']}, 'question_types': [intentions]}
        else:
            data = {'args': {food[0]: ['food']}, 'question_types': [intentions]}

        parser = question_parser.QuestionPaser()
        searcher = answer_search.AnswerSearcher()

        sqls = parser.parser_main(data)  # 生成相关的查询语句
        print(sqls)
        final_answer = searcher.search_main(sqls)  # 查询相关内容
        #  进行判断 输出结果
        if not final_answer:
            dispatcher.utter_message(template='utter_out')
        else:
            answer = '\n'.join(final_answer)
            print(answer)
            dispatcher.utter_message(text=answer)
        return [SlotSet('food', None)]


class FindTheCorrespondingsmallTalk(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:

        try:
            food = tracker.latest_message
            answer = app.talk(food['text'])
            dispatcher.utter_message(text=answer)
        except Exception as e:
            print(e)
            dispatcher.utter_message(template='utter_exception')
        return []


class FindTheCorrespondingWEATHER(Action):
    def name(self) -> Text:
        return "FindTheCorrespondingweather"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        location = tracker.get_slot('location')
        times = tracker.get_slot('time')

        if type(location) == list:
            location = location[-1]
        timesss = times[0]
        d = date.today()
        if timesss == '今天':
            timesss = str(d)
        elif timesss == '明天':
            timesss = str(d + timedelta(days=1))
        elif timesss == '后天':
            timesss = str(d + timedelta(days=2))
        elif timesss == '大后天':
            timesss = str(d + timedelta(days=3))
        data = weather.weather_api(location)

        try:
            text = ''
            for i in range(7):
                if data[i]['date'] == timesss:
                    index = ''.join([line['title'] + ' '
                                     + line['level'] + ' '
                                     + line['desc'] + '\n' for line in data[i]['index']])
                    text = location + '天气:' \
                                      '\n' + data[i]['date'] + ' ' + data[i]['week'] + \
                           '\n天气状况:' + data[i]['wea'] + \
                           '\n体感温度:' + data[i]['tem'] + \
                           '\n最高温度' + data[i]['tem1'] + \
                           '\n最低温度' + data[i]['tem2'] + \
                           '\n湿度:' + data[i]['humidity'] + \
                           '\n' + data[i]['win'][0] + data[i]['win'][1] + \
                           '\n风力等级:' + data[i]['win_speed'] + \
                           '\n空气质量:' + data[i]['air_level'] + \
                           '\n温馨提示:' + data[i]['air_tips'] + index

            print(text)
            dispatcher.utter_message(text=text)

        except Exception as e:
            print('error', e)
            dispatcher.utter_message(template='utter_exception')
        return [SlotSet('location', None), SlotSet('time', None)]
