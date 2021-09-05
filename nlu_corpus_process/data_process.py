# -*- codeing = utf-8 -*-
# @Time :2021-08-12 10:23
# @Author : LUOFAN-LeiYingJie
# @File : read_data.py
# @Software : PyCharm
# @Email: 609751841@qq.com

import os

def lookup_corpus():
    path = os.path.join(os.getcwd(), 'lookup_corpus')
    namelist = os.listdir(path)
    for filename in namelist:
        with open(os.path.join(path, filename), 'r', encoding='utf-8')as f:
            with open('lookup_top.txt', 'r', encoding='utf-8')as r:
                with open(os.path.join(path, filename.split('.')[0] + '.yml'), 'w', encoding='utf-8')as t:
                    words = r.readlines()
                    for word in words:
                        if word.split(':')[1] == ' disease\n':
                            word = '  - lookup: ' + word.split(':')[1].replace(word.split(':')[1],
                                                                               filename.split('.')[0] + '\n')
                            print(filename + ' replace success!')

                        t.writelines(word)
                    t.writelines('\n')

                    for line in f.readlines():
                        t.writelines('      ' + '- ' + line)


def location_process():
    with open('地区数据处理/地区.txt', 'r', encoding='utf-8')as f:
        with open('lookup_top.txt', 'r', encoding='utf-8')as r:
            with open('地区数据处理/location.yml', 'w', encoding='utf-8')as t:
                words = r.readlines()
                for word in words:
                    if word.split(':')[1] == ' disease\n':
                        word = '  - lookup: ' + word.split(':')[1].replace(word.split(':')[1], 'location' + '\n')
                    t.writelines(word)
                t.writelines('\n')
                for line in f.readlines():
                    data = line.split(',')
                    if data == ['\n']:
                        del data
                    else:
                        data = line.split(',')[2]
                        t.writelines('      ' + '- ' + data)


if __name__ == '__main__':
    # lookup_corpus()
    location_process()
