
# -*- coding: utf-8 -*-

import re
import pickle

INF = 9999
MAX_SENTENCE_LENGTH = 300


class SpacingModule:

    def __init__(self, _path):
        self._string = ""
        self._path = _path
        self._max_length = MAX_SENTENCE_LENGTH
        self._table = []
        self._score = []
        self._bt = []
        self._segment = []
        self._buf_list = []
        self._schar_list = []
        self._kstring = []
        self._eojeol_dictionary = {}
        self._morpheme_dictionary = {}
        self._postpositional_particle_dictionary = {}
        self.__create_table()
        self.__open_dictionary()

    def spacing(self, _string):
        self.__init_table(_string)
        self.__special_char_processing()
        self.__prepare()
        self.__forward()
        self.__backward()
        self.__apply_heuristics()
        self.__merge_string()
        self.__quotation_mark_processing()
        self.__syllable_processing()
        self.__etc_heuristics()
        return self._string

    def ps(self, _string):
        self._segment = _string.split(' ')
        buffer = []
        for i in range(len(self._segment)):
            if self._segment[i] == '':
                continue
            else:
                buffer.append(self._segment[i])
        self._segment = buffer

    def __create_table(self):
        self._table = [[0] * self._max_length for col in range(self._max_length)]
        self._score = [0] * self._max_length
        self._bt = [0] * self._max_length

    def __open_dictionary(self):
        eojeol_dict_file = open(self._path + "\dict\eojeol\eojeol_dict.dict", 'rb')
        morpheme_dict_file = open(self._path + "\dict\morpheme\morpheme_dict.dict", 'rb')
        postpositional_particle_dict_file = open(self._path +
            "\dict\postpositional particle\postpositional_particle_dict.dict", 'rb')

        self._eojeol_dictionary = pickle.load(eojeol_dict_file, encoding='UTF-8')
        self._morpheme_dictionary = pickle.load(morpheme_dict_file, encoding='UTF-8')
        self._postpositional_particle_dictionary = pickle.load(postpositional_particle_dict_file, encoding='UTF-8')

    def __init_table(self, _string):
        self._string = _string.strip()
        for j in range(self._max_length):
            self._score[j] = 0
            self._bt[j] = 0
            for k in range(self._max_length):
                self._table[j][k] = 0
        self._segment.clear()
        self._schar_list.clear()

    def __special_char_processing(self):
        split_char = '!@#'
        schar = re.compile('[^\u3131-\u3163\uac00-\ud7a3]+')

        buffer = schar.sub(split_char, self._string)
        self._kstring = buffer.split(split_char)
        self._schar_list = schar.findall(self._string)

        self._string = schar.sub('', self._string)
        self._string = ' ' + self._string
        self._length = len(self._string)

    def __eojeol_score(self, _string):
        if _string in self._eojeol_dictionary:
            return self._eojeol_dictionary.get(_string)

    def __prepare(self):
        #   table is empty              ==      0
        #   table is exists             !=      0
        #   table is virtual eojeols    ==  -10.0
        for j in range(1, self._length):
            for k in range(j, self._length):
                if k - j >= 10:
                    break
                slicing_string = self._string[j:k + 1]
                if slicing_string in self._eojeol_dictionary:
                    self._table[j][k] = self.__eojeol_score(slicing_string)
                else:
                    self._table[j][k] = 0

        #   adding virtual eojeols
        for j in range(1, self._length):
            for k in range(j, self._length):
                if self._table[j][k] is not 0 and self._table[j][k] is not -10.0:
                    i = j - 1
                    cnt = 0
                    while i > 0 and cnt < 6:
                        if self._table[i][j - 1] is 0:
                            self._table[i][j - 1] = -10.0
                        i = i - 1
                        cnt = cnt + 1

    def __forward(self):
        self._score[0] = 0
        for i in range(1, self._length):
            self._score[i] = -INF
        for j in range(1, self._length):
            for k in range(j, self._length):
                if self._table[j][k] is not 0:
                    if (self._score[j - 1] + self._table[j][k]) > self._score[k]:
                        self._score[k] = self._score[j - 1] + self._table[j][k]
                        self._bt[k] = j
        self._bt[self._length - 1] = self._bt[self._length - 2]

    def __backward(self):
        k = self._length - 1
        while k > 0:
            j = self._bt[k]
            slicing_string = self._string[j:k + 1]
            self._segment.append(slicing_string)
            k = j - 1
        self._segment.reverse()

    def __add(self, _idx):
        _string = str(self._segment[_idx - 1]) + str(self._segment[_idx])
        self._segment.pop(_idx - 1)
        self._segment.pop(_idx - 1)
        self._segment.insert(_idx - 1, str(_string))

    def __apply_heuristics(self):
        sticklst = list()
        del sticklst[:]

        for idx in range(1, self._segment.__len__()):
            if self.__heuristics_1(idx) is True:
                if self.__heuristics_1_1(idx) is True or \
                        self.__heuristics_1_2(idx) is True or \
                        self.__heuristics_1_3(idx) is True:
                    sticklst.append(idx)

        dist = 0
        for i in range(sticklst.__len__()):
            self.__add(sticklst[i] - dist)
            dist = dist + 1

    def __heuristics_1(self, _idx):
        morpheme = self._segment[_idx - 1]
        if morpheme in self._morpheme_dictionary:
            for i in range(self._morpheme_dictionary[morpheme].__len__()):
                if self._morpheme_dictionary[morpheme][i] == "NNG" or \
                        self._morpheme_dictionary[morpheme][i] == "NNP" or \
                        self._morpheme_dictionary[morpheme][i] == "NNB":
                    return True
        return False

    def __heuristics_1_1(self, _idx):
        morpheme = self._segment[_idx]
        if morpheme in self._postpositional_particle_dictionary:
            return True
        if morpheme in self._morpheme_dictionary:
            for i in range(self._morpheme_dictionary[morpheme].__len__()):
                if self._morpheme_dictionary[morpheme][i] == "VX":
                    return True
        return False

    def __heuristics_1_2(self, _idx):
        this_eojeol = self._segment[_idx]
        length = this_eojeol.__len__()
        for k in range(length):
            morpheme = this_eojeol[0:k + 1]
            if morpheme in self._morpheme_dictionary and \
                    (morpheme is "하" or morpheme is "되" or morpheme is "시키"):
                for i in range(self._morpheme_dictionary[morpheme].__len__()):
                    if self._morpheme_dictionary[morpheme][i] == "VV":
                        return True
        return False

    def __heuristics_1_3(self, _idx):
        this_eojeol = self._segment[_idx]
        if this_eojeol[0] is "들":
            return True
        return False

    def __heuristics_2(self, _idx):
        morpheme = self._segment[_idx]
        if morpheme in self._morpheme_dictionary:
            for i in range(self._morpheme_dictionary[morpheme].__len__()):
                if self._morpheme_dictionary[morpheme][i] == "JKS" or \
                        self._morpheme_dictionary[morpheme][i] == "JKC" or \
                        self._morpheme_dictionary[morpheme][i] == "JKG" or \
                        self._morpheme_dictionary[morpheme][i] == "JKO" or \
                        self._morpheme_dictionary[morpheme][i] == "JKB" or \
                        self._morpheme_dictionary[morpheme][i] == "JKV" or \
                        self._morpheme_dictionary[morpheme][i] == "JKQ" or \
                        self._morpheme_dictionary[morpheme][i] == "JX" or \
                        self._morpheme_dictionary[morpheme][i] == "JC":
                    return True
        return False

    def __isN(self, _idx):
        morpheme = self._segment[_idx]
        if morpheme in self._morpheme_dictionary:
            for i in range(self._morpheme_dictionary[morpheme].__len__()):
                if self._morpheme_dictionary[morpheme][i] == "NNG" or \
                        self._morpheme_dictionary[morpheme][i] == "NNP" or \
                        self._morpheme_dictionary[morpheme][i] == "NNB":
                    return True
        return False

    def __merge_string(self):
        result = ''
        seg_length = self._segment.__len__()
        for i in range(seg_length):
            result += self._segment[i]
            result += ' '
        result = result[:-1]
        idx = 0
        for i in range(len(self._kstring) - 1):
            for j in range(len(self._kstring[i])):
                if result[idx] == ' ':
                    idx += 1
                if self._kstring[i][j] == result[idx]:
                    idx += 1
            result = result[:idx] + self._schar_list[i] + result[idx:]
            idx += len(self._schar_list[i])

        string = result
        length = len(result)
        result = result[0]
        kor = re.compile('[가-힝]')
        num = re.compile('[0-9]')
        eng = re.compile('[a-zA-Z]')

        for i in range(1, length - 1):
            fk = kor.match(string[i - 1])
            tk = kor.match(string[i + 1])
            n = num.match(string[i])
            fn = num.match(string[i - 1])
            fe = eng.match(string[i - 1])
            if fk and n:
                result += ' '
            if fe and tk and string[i] == ' ':
                continue
            if fn and tk and string[i] == ' ':
                continue
            result += string[i]
        result += string[length - 1]
        self._string = result

    def __quotation_mark_processing(self):
        # 큰따옴표, 작은따옴표, 쉼표
        result = self._string
        length = result.__len__()
        ret = ""
        flag1 = 0
        flag2 = 0
        for i in range(length):
            if result[i] is '"':
                flag1 = flag1 + 1
                if flag1 % 2 is 1:
                    if i - 1 >= 0 and result[i - 1] is not ' ':
                        ret = ret + ' "'
                        continue
                    ret = ret + '"'
                    continue
                elif flag1 % 2 is 0:
                    if i - 1 >= 0 and result[i - 1] is ' ':
                        ret = ret[0:ret.__len__() - 1]
                    ret = ret + '"'
                    continue
            elif result[i] is "'":
                flag2 = flag2 + 1
                if flag2 % 2 is 1:
                    if i - 1 >= 0 and result[i - 1] is not ' ':
                        ret = ret + " '"
                        continue
                    ret = ret + "'"
                    continue
                elif flag2 % 2 is 0:
                    if i - 1 >= 0 and result[i - 1] is ' ':
                        ret = ret[0:ret.__len__() - 1]
                    ret = ret + "'"
                    continue
            if i - 1 >= 0 and result[i - 1] is '"' and result[i] is ' ':
                continue
            if i - 1 >= 0 and result[i - 1] is "'" and result[i] is ' ':
                continue
            ret = ret + result[i]
        self._string = ret

    def __syllable_processing(self):
        self._segment = self._string.split(' ')
        self.__backward_processing()
        self.__forward_processing()
        buffer = ""
        for i in range(self._segment.__len__()):
            buffer += self._segment[i]
            buffer += ' '
        self._string = buffer[:-1]

    def __forward_processing(self):
        length = self._segment.__len__() - 1
        self._buf_list = []
        flag = 0
        for i in range(length, 0, -1):
            if flag == 1:
                flag = 0
                continue
            if len(self._segment[i]) == 1:
                buffer = self._segment[i - 1] + self._segment[i]
                if buffer in self._eojeol_dictionary:
                    self._buf_list.append(buffer)
                    flag += 1
                    continue
            self._buf_list.append(str(self._segment[i]))
        if flag == 0:
            self._buf_list.append(self._segment[0])
        self._segment = list(reversed(self._buf_list))

    def __backward_processing(self):
        length = self._segment.__len__()
        self._buf_list = []
        flag = 0
        for i in range(length):
            if flag == 1:
                flag = 0
                continue
            if len(self._segment[i]) == 1:
                if i == length - 1:
                    self._buf_list.append(self._segment[i])
                    break
                buffer = self._segment[i] + self._segment[i+1]
                if buffer in self._eojeol_dictionary:
                    self._buf_list.append(buffer)
                    flag += 1
                    continue
            self._buf_list.append(self._segment[i])
        self._segment = self._buf_list

    def __etc_heuristics(self):
        result = self._string
        result = re.sub(',', ', ', result)
        result = re.sub('% ', '%', result)
        result = re.sub(' 를', '를', result)
        result = re.sub(' 을', '을', result)
        result = re.sub(' 만 ', '만 ', result)
        result = re.sub(' 만,', '만,', result)
        result = re.sub('지않', '지 않', result)
        result = re.sub('것같', '것 같', result)
        result = re.sub(' {1}\(', '(', result)
        result = re.sub('\( {1}', '(', result)
        result = re.sub(' {1}\)', ')', result)
        result = re.sub('\) {1}', ')', result)
        result = re.sub('· {1}', '·', result)
        result = re.sub(' {2}', ' ', result)
        self._string = result
