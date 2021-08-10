import operator, os
import numpy as np
from decimal import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_base_str(s):
    if s is None or s == 'NA':
        return 'NA'
    else:
        return s.strip().lower()


def txt_deal(s):
    if s is None or s == 'NA':
        return 'NA'
    elif '\n' not in s:
        return s.strip().lower()
    else:
        new_s = s.strip().lower().replace('\n', '')
        return ' '.join(new_s.split())


def get_synonmys_tolist(s):
    if '\n' in s:
        return s.strip().split('\n')
    elif ';' in s:
        return s.strip().split(';')
    elif s == 'NA' or s is None:
        return 'NA'
    else:
        return [s]


def get_ncicode(s):
    if s is None or s == 'NA':
        return 'NA'
    elif ';' in s:
        ncicode_list_v1 = s.strip().split(';')
        ncicode_list_v2 = [v.strip() for v in ncicode_list_v1]
        return ncicode_list_v2
    else:
        return [s]


def deal_dict_value(s):
    if s is None or s == 'NA':
        return 'NA'
    elif ';' in s:
        s_tolist = s.strip().lower().split(';')
        return [item.strip() for item in s_tolist]
    else:
        return [s.strip().lower()]


def deal_cancers(testlist):
    final_list = []
    for item_str in testlist:
        item_str = item_str.replace(
            'pca',
            '').replace(
            'cases',
            '').replace(
            ',',
            ';').replace(
                ';;',
                ';').replace(
                    'or',
                    ';').replace(
                        '/',
                        ';').replace(
                            'and',
            ';')
        item_list = item_str.split(';')
        item_list = [v.strip() for v in item_list]
        final_list.extend(item_list)
    final_list = set(final_list)
    return final_list


def doulist_rem(dou_list):
    newdou_list = []
    newdou_list.append(dou_list[0])
    for ls in dou_list[1:]:
        if ls not in newdou_list:
            newdou_list.append(ls)
    return newdou_list

def add_fushu(baselist):
    return baselist + [ba + 's' for ba in baselist]

def takeSecond(elem):
    return elem[1]

class CharPairs:
    def __init__(self, string):
        self.string = string.lower()
        self.create_char_list()
        self.create_char_pairs()

    def create_char_list(self):
        self.str_length = 0
        self.strChars = {}
        for char in self.string:
            self.strChars[self.str_length] = char
            self.str_length += 1

    def create_char_pairs(self):
        self.charPairs = []
        self.charPairCount = 0
        count = 0
        for char in self.strChars:
            if count < (self.str_length - 1):
                y = count + 1
                pair = self.strChars[count] + self.strChars[y]
                self.charPairs.append(pair)
                self.charPairCount += 1

            count += 1

    def getCharPairs(self):
        return self.charPairs

    def getCharPairCount(self):
        return self.charPairCount


class similarity:
    def __init__(self, string1, string2):
        # get character pairs for string1
        strChar1 = CharPairs(string1)
        self.charPair1 = strChar1.getCharPairs()
        self.charPair1Count = strChar1.getCharPairCount()
        self.string1 = string1.lower()
        # get character pairs for string2
        strChar2 = CharPairs(string2)
        self.charPair2 = strChar2.getCharPairs()
        self.charPair2Count = strChar2.getCharPairCount()
        self.string2 = string2.lower()
        # run steps
        self.find_in_common_char_pairs()
        self.calculate_similarity()

    def find_in_common_char_pairs(self):
        self.incommon = set(self.charPair1).intersection(self.charPair2)
        self.incommon_count = 0
        for i in self.incommon:
            self.incommon_count += 1

    def calculate_similarity(self):
        numerator = 2 * self.incommon_count
        denominator = self.charPair1Count + self.charPair2Count
        getcontext().prec = 4
        self.sim = Decimal(numerator) / Decimal(denominator)

    def get_sim(self):
        return self.sim

def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    v0 = np.array([vectors[0]])
    v1 = np.array([vectors[1]])
    return cosine_similarity(v0, v1)[0][0]

def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

def lifestyle_pipei(inp):
    cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    lfsty_path = os.path.join(cur_dir, 'dict/lfsty.txt')
    lfsty_wds = [i.strip() for i in open(lfsty_path, encoding='utf-8') if i.strip()]

    wds_sim = []
    for wd in lfsty_wds:
        # wds_sim.append((wd, similarity(inp, wd).get_sim()))
        wds_sim.append((wd, get_cosine_sim(inp, wd)))

    wds_sim.sort(key=takeSecond, reverse=True)

    ned_lfsts = []
    for item in wds_sim[:]:
        if inp in item[0] or item[0] in inp:
            ned_lfsts.append(item[0])
    return ned_lfsts

