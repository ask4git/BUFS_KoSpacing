
# -*- coding: utf-8 -*-

import re
import glob
import math
import pickle


class Dict:

    def __init__(self):
        self.data = dict()

    def save_dict(self, _path, _data):
        with open(_path, 'wb') as save_file:
            pickle.dump(_data, save_file)

    def save_as_txt(self, _path, _data):
        with open(_path, 'w', encoding='utf-8-sig') as save_file:
            for key, value in _data.items():
                print(key + " : ", value, file=save_file)

    def print_data(self, _data):
        for key, value in _data.items():
            print(key + " : ", value)


class Eojeoldict(Dict):

    # initialize
    def __init__(self, _path):
        Dict.__init__(self)
        self.__eojeol_freq = dict()
        self.__syllable_freq = dict()
        self.__path = _path

    def create_dictionary(self):
        self.__read()
        self.__scoring()
        self.__save()

    def add_eojeol_data(self, _target_path):
        eojeol_data_file = open(self.__path + "\dict\eojeol\eojeol_dict.dict", 'rb')
        eojeol_freq_file = open(self.__path + "\dict\eojeol\eojeol_freq.dict", 'rb')
        syllable_freq_file = open(self.__path + "\dict\eojeol\syllable_freq.dict", 'rb')

        self.data = pickle.load(eojeol_data_file, encoding='UTF-8')
        self.__eojeol_freq = pickle.load(eojeol_freq_file, encoding='UTF-8')
        self.__syllable_freq = pickle.load(syllable_freq_file, encoding='UTF-8')

        target_file_list = glob.glob(_target_path)
        for file in target_file_list:
            with open(file, 'rt', encoding='utf-8-sig') as f:
                for each_line in f:
                    each_line = re.sub('[^가-힝\\s]', ' ', each_line)
                    self.__add_data(each_line.strip())
        self.__scoring()
        self.__save()

    # corpus를 한 줄씩 읽어서 한글만 골라내서 넘겨줌
    def __read(self):
        path = self.__path + "\corpus\*.txt"
        file_list = glob.glob(path)
        for file in file_list:
            with open(file, 'rt', encoding='utf-8-sig') as f:
                for each_line in f:
                    each_line = re.sub('[^가-힝\\s]', ' ', each_line)
                    self.__add_data(each_line.strip())

    # read()에서 받은 string을 각각 어절과 음절로 분리 후 빈도사전에 추가
    def __add_data(self, _string):
        buffer = _string.split()
        # add eojeol frequency
        for eojeol in buffer:
            if eojeol == '':
                continue
            if eojeol in self.__eojeol_freq:
                self.__eojeol_freq[eojeol] += 1
            else:
                self.__eojeol_freq[eojeol] = 1

        # add syllable frequency
        for index in range(_string.__len__()):
            syllable = _string[index]
            if syllable != ' ' :
                if syllable in self.__syllable_freq:
                    self.__syllable_freq[syllable] += 1
                else:
                    self.__syllable_freq[syllable] = 1

    # 어절점수를 채점
    def __scoring(self):
        for key, value in self.__eojeol_freq.items():
            minimum = 0x7fffffff
            word = str(key)
            for index in range(word.__len__()):
                if self.__syllable_freq[word[index]] < minimum:
                    minimum = self.__syllable_freq[word[index]]
            self.data[key] = math.log10(self.__eojeol_freq[key] / minimum)

    # save file
    def __save(self):
        self.save_dict(self.__path + "\dict\eojeol\eojeol_freq.dict", self.__eojeol_freq)
        self.save_as_txt(self.__path + "\dict\eojeol\eojeol_freq.txt", self.__eojeol_freq)

        self.save_dict(self.__path + "\dict\eojeol\syllable_freq.dict", self.__syllable_freq)
        self.save_as_txt(self.__path + "\dict\eojeol\syllable_freq.txt", self.__syllable_freq)

        self.save_dict(self.__path + "\dict\eojeol\eojeol_dict.dict", self.data)
        self.save_as_txt(self.__path + "\dict\eojeol\eojeol_dict.txt", self.data)
