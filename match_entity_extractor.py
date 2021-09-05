# -*- codeing = utf-8 -*-
# @Time :2021/8/12 14:59
# @Author : 兢兢业业的小码农
# @File : 00.py
# @Software : PyCharm
# @Email: 1795947368@qq.com

import os
from itertools import combinations
from typing import Any, Text, Dict
from rasa.nlu.extractors.extractor import EntityExtractor


class MatchEntityExtractor(EntityExtractor):
    """绝对匹配提取实体"""
    provides = ["entities"]

    defaults = {
        "dictionary_path": None,
        "take_long": None,
        "take_short": None
    }

    def __init__(self, component_config=None):
        print("init")
        super(MatchEntityExtractor, self).__init__(component_config)
        self.dictionary_path = self.component_config.get("dictionary_path")
        self.take_long = self.component_config.get("take_long")
        self.take_short = self.component_config.get("take_short")
        if self.take_long and self.take_short:
            raise ValueError("take_long and take_short can not be both True")
        self.data = {}  # 用于绝对匹配的数据
        for file_path in os.listdir(self.dictionary_path):
            if file_path.endswith(".txt"):
                file_path = os.path.join(self.dictionary_path, file_path)
                file_name = os.path.basename(file_path)[:-4]
                with open(file_path, mode="r", encoding="utf-8") as f:
                    self.data[file_name] = f.read().splitlines()

    def process(self, message, **kwargs):
        """绝对匹配提取实体词"""
        print("process")
        entities = []
        for entity, value in self.data.items():
            for i in value:
                start = message.text.find(i)
                if start != -1:
                    entities.append({
                        "start": start,
                        "end": start + len(i),
                        "value": i,
                        "entity": entity,
                        "confidence": 1
                    })
        if self.take_long or self.take_short:
            for i in list(combinations(entities, 2)):
                v0, v1 = i[0]["value"], i[1]["value"]
                if v0 in v1 or v1 in v0:
                    (long, short) = (i[0], i[1]) if len(v0) > len(v1) else (i[1], i[0])
                    if self.take_long == True and short in entities:
                        entities.remove(short)
                    if self.take_short == True and long in entities:
                        entities.remove(long)
        extracted = self.add_extractor_name(entities)
        message.set("entities", extracted, add_to_output=True)

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        print("load")
        return cls(meta)
