'''
此文件借鉴刘焕勇老师的知识图谱导入文件
对文件进行修改
功能:解决导入知识图谱数据库速度慢的问题
'''
import os
import re
import json
from time import time
from py2neo import Graph, Node, Relationship, Subgraph

#这里的py2neo版本指定2020.1.1


class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'medical.json')

    '''读取文件'''

    def read_nodes(self):
        # 共７类节点
        drugs = []  # 药品
        foods = []  # 食物
        checks = []  # 检查
        departments = []  # 科室
        producers = []  # 药品大类
        diseases = []  # 疾病
        symptoms = []  # 症状

        disease_infos = []  # 疾病信息

        # 构建节点实体关系
        rels_department = []  # 科室－科室关系
        rels_noteat = []  # 疾病－忌吃食物关系
        rels_doeat = []  # 疾病－宜吃食物关系
        rels_recommandeat = []  # 疾病－推荐吃食物关系
        rels_commonddrug = []  # 疾病－通用药品关系
        rels_recommanddrug = []  # 疾病－热门药品关系
        rels_check = []  # 疾病－检查关系
        rels_drug_producer = []  # 厂商－药物关系

        rels_symptom = []  # 疾病症状关系
        rels_acompany = []  # 疾病并发关系
        rels_category = []  # 疾病与科室之间的关系

        count = 0
        for data in open(self.data_path, encoding='utf8'):
            disease_dict = {}
            count += 1
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease, acompany])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                if len(cure_department) == 1:
                    rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])
                    rels_category.append([disease, small])

                disease_dict['cure_department'] = cure_department
                departments += cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']

            if 'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease, drug])
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])

                foods += not_eat
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do])

                foods += do_eat
                recommand_eat = data_json['recommand_eat']

                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check])
                checks += check
            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                producer = [i.split('(')[0] for i in drug_detail]
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                producers += producer
            disease_infos.append(disease_dict)
        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(
            diseases), disease_infos, \
               rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, \
               rels_symptom, rels_acompany, rels_category

    '''建立节点'''

    def create_node(self, label, nodes):
        count = 0
        nodess = []
        for node_name in nodes:
            node = Node(label, name=node_name)
            nodess.append(node)
            count += 1
        return nodess

    '''创建知识图谱中心疾病的节点'''

    def create_diseases_nodes(self, disease_infos):
        count = 0
        nodes = []
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'], cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'], cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        , cure_way=disease_dict['cure_way'], cured_prob=disease_dict['cured_prob'])
            nodes.append(node)
            count += 1
        return nodes

    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        a = self.create_diseases_nodes(disease_infos)
        b = self.create_node('Drug', Drugs)
        c = self.create_node('Food', Foods)
        d = self.create_node('Check', Checks)
        e = self.create_node('Department', Departments)
        f = self.create_node('Producer', Producers)
        g = self.create_node('Symptom', Symptoms)
        return a + b + c + d + e + f + g

    '''创建实体关系边'''

    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        a = self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        b = self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        c = self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        d = self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        e = self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        f = self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        g = self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        h = self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        i = self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        j = self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        k = self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')
        return a + b + c + d + e + f + g + h + i + j + k

    '''创建实体关联边'''

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        relationships = []
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            relationships.append(query)
            try:
                count += 1
            except Exception as e:
                print()
        return relationships


class ProgressBar:
    def __init__(self, total, name='', mode=0):
        self.total = total
        self.name = name
        modes = (
            lambda n: f"进度|{'=' * n}{'>'}{'·' * (100 - n)}"[:-1] + f"| {n}% |",
            lambda n: f"进度|{'█' * n:100s}| {n}% |",
            lambda n: f"\033[31m{'♥' * n}{'♡' * (100 - n)}  进度{n}♥\033[0m",
            lambda n: f"\033[46m进度{' ' * n}{n}% \033[44m{' ' * (100 - n)}\033[0m",
        )
        mode = 0 if mode > 3 else mode
        self.mode = modes[mode]

    def now(self, n):
        if BAR:
            n_ = 100 * n // self.total
            print(f"\r{self.name}: {self.mode(n_)} [{n:05d} / {self.total}]", end='', flush=True)

    def end(self, name):
        print(name)


BAR = True
t0 = time()

if __name__ == '__main__':
    handler = MedicalGraph()
    graphnodes = handler.create_graphnodes()
    graphrels = handler.create_graphrels()
    print(f"匹配所用时间：{time() - t0:.1f}秒")
    print('正在创建图谱 . . . . . .', end='')
    graph = Graph("http://localhost:7474/", username="neo4j-medical-robot-rasa", password="luofan66")
    # 版本 20201.
    dicts = {}
    for i in graphnodes:
        dicts[i['name']] = i
    import numpy as np

    len(np.array(graphrels))
    p = ProgressBar(len(np.array(graphrels)), '匹配进度', mode=3)
    s = 0
    relationships = []
    for i in graphrels:
        p.now(s)
        n = i.split(' ')[2].split("'")[1]
        m = i.split("'")[3]
        if m == '血清5':
            m = "血清5'-核苷酸酶（5'-NT）"
        rr = i.split('[')[-1].split(']')[0][4:].split("'")[1]
        r = i.split('[')[-1].split(':')[1].split('{')[0]
        relationships.append(Relationship(dicts[n], r, dicts[m], name=rr))
        s += 1

    print(f"匹配所用时间：{time() - t0:.1f}秒")
    print('数据正在导入数据库......')

    graph.create(Subgraph(nodes=graphnodes, relationships=relationships))

    print('\r知识图谱数据库创建完成 !!')
    print(f"总体所用时间：{time() - t0:.1f}秒")
