#!/usr/bin/env python3
# coding: utf-8
# date: 21-03-25
import os
import re
import ahocorasick
from helper import add_fushu


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.lfsty_path = os.path.join(cur_dir, 'dict/lfsty.txt')
        self.paper_path = os.path.join(cur_dir, 'dict/paper.txt')
        self.unit_path = os.path.join(cur_dir, 'dict/unit.txt')
        self.pca_path = os.path.join(cur_dir, 'dict/cancer.txt')
        self.nation_path = os.path.join(cur_dir, 'dict/nation.txt')
        self.gene_path = os.path.join(cur_dir, 'dict/gene.txt')
        self.baseline_path = os.path.join(cur_dir, 'dict/baseline.txt')
        self.outcome_path = os.path.join(cur_dir, 'dict/outcome.txt')

        # 加载特征词
        self.lfsty_wds = [
            i.strip() for i in open(
                self.lfsty_path, encoding='utf-8') if i.strip()]
        self.paper_wds = [
            i.strip() for i in open(
                self.paper_path, encoding='utf-8') if i.strip()]
        self.unit_wds = [i.strip() for i in open(self.unit_path, encoding='utf-8') if i.strip()]
        self.pca_wds = [i.strip() for i in open(self.pca_path, encoding='utf-8') if i.strip()]
        self.nation_wds = [
            i.strip() for i in open(
                self.nation_path, encoding='utf-8') if i.strip()]
        self.gene_wds = [i.strip() for i in open(self.gene_path, encoding='utf-8') if i.strip()]
        self.baseline_wds = [
            i.strip() for i in open(
                self.baseline_path, encoding='utf-8') if i.strip()]
        self.outcome_wds = [
            i.strip() for i in open(
                self.outcome_path, encoding='utf-8') if i.strip()]
        self.region_words = set(
            self.lfsty_wds +
            self.pca_wds +
            self.paper_wds +
            self.outcome_wds +
            self.baseline_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句类型关键词
        self.ask_lfstres_qwds = [
            'survey',
            'study',
            'studie',
            'dissertation',
            'article',
            'treatise',
            'thesis',
            'paper',
            'investigation',
            'research',
            'researche',
            'report']
        self.ask_lfstres_qwds = add_fushu(self.ask_lfstres_qwds)
        self.askinf_qwds = [
            'information',
            'introduction',
            'detailed information',
            'specific information',
            'core information',
            'brief introduction',
            'brief information']
        self.askunit_qwds = [
            'measurement',
            'unit',
            'units',
            'measure',
            'measures']
        self.jibing_qwds = [
            'pca',
            'illness',
            'illnesse',
            'sickness',
            'sicknesse',
            'disease',
            'pathema',
            'prostate cancer',
            'prostatic carcinoma',
            'CRPC',
            'prostatic cancer',
            'cancer']
        self.jibing_qwds = add_fushu(self.jibing_qwds)
        self.lead_qwds = ['lead', 'arise', 'rise', 'result', 'bring']
        self.lead_qwds = add_fushu(self.lead_qwds)
        self.fenlei_qwds = [
            'kind',
            'class',
            'classe',
            'type',
            'classification', 'belong']
        self.fenlei_qwds = add_fushu(self.fenlei_qwds)
        self.factor_qwds = ['factor', 'impact level', 'influence factor', 'impact factor', 'affected factor']
        self.cornation_qwds = [
            'where',
            'area',
            'areas',
            'country',
            'countries',
            'nation',
            'nations',
            'region',
            'regions',
            'location',
            'appear',
            'appears']
        self.gene_qwds = ['gene', 'genes']
        self.pca_bsl_qwds = ['baseline', 'baselines']
        self.pca_otc_qwds = ['outcome', 'outcomes']
        print('model init finished ......')

        return

    '''分类主函数'''

    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for tp in medical_dict.values():
            types += tp

        question_type = 'others'

        question_types = []

        if self.check_words(
                self.ask_lfstres_qwds, question) and (
                'lifestyle' in types):
            question_type = 'related_papers'
            question_types.append(question_type)

        if self.check_words(self.askinf_qwds, question) and ('paper' in types):
            question_type = 'askpaper_inf'
            question_types.append(question_type)

        if self.check_words(
                self.askunit_qwds, question) and (
                'lifestyle' in types):
            question_type = 'corresponding_units'
            question_types.append(question_type)

        if self.check_words(
                self.lead_qwds,
                question) and self.check_words(
                self.jibing_qwds,
                question) and self.check_words(
                self.fenlei_qwds,
                question) and (
                'lifestyle' in types):
            question_type = 'lfst_pcas'
            question_types.append(question_type)

        if self.check_words(self.factor_qwds, question) and ('lifestyle' in types):
            question_type = 'factor_type'
            question_types.append(question_type)

        if self.check_words(
            self.pca_otc_qwds,
            question) and (
            'lifestyle' in types) and (
                'pca_type' in types):
            question_type = 'lfst_pca_outcome'
            question_types.append(question_type)

        if self.check_words(self.pca_bsl_qwds, question) and ('lifestyle' in types):
            question_type = 'lfst_baseline'
            question_types.append(question_type)

        if 'baseline' in types:
            question_type = 'askbsl_inf'
            question_types.append(question_type)

        if 'outcome' in types:
            question_type = 'askotc_inf'
            question_types.append(question_type)

        if self.check_words(
                self.fenlei_qwds,
                question) and self.check_words(
                self.lead_qwds,
                question) == False and self.check_words(self.factor_qwds, question) == False and (
                'lifestyle' in types):
            question_type = 'lfst_class'
            question_types.append(question_type)

        if self.check_words(
                self.cornation_qwds,
                question) and (
                'lifestyle' in types):
            question_type = 'lfst_nation'
            question_types.append(question_type)

        if self.check_words(
                self.gene_qwds, question) and (
                'pca_type' in types):
            question_type = 'pca_gene'
            question_types.append(question_type)
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型，已经看懂'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.lfsty_wds:
                wd_dict[wd].append('lifestyle')
            if wd in self.paper_wds:
                wd_dict[wd].append('paper')
            if wd in self.unit_wds:
                wd_dict[wd].append('unit')
            if wd in self.pca_wds:
                wd_dict[wd].append('pca_type')
            if wd in self.nation_wds:
                wd_dict[wd].append('nation')
            if wd in self.gene_wds:
                wd_dict[wd].append('gene')
            if wd in self.baseline_wds:
                wd_dict[wd].append('baseline')
            if wd in self.outcome_wds:
                wd_dict[wd].append('outcome')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''句子切分'''

    def sent_split(self, sent):
        sent_after = re.sub(' +', ' ', sent)
        return [tk.lower() for tk in sent_after.strip('!?.,').split(' ')]

    '''问句过滤，已经看懂'''

    def check_medical(self, question):
        region_wds = []
        for item in self.region_tree.iter_long(question):
            wd = item[1][1]
            region_wds.append(wd)
        '''去除不正常匹配'''
        qs_tokens = self.sent_split(question)
        for wd in region_wds:
            for tk in qs_tokens:
                if ' ' not in wd:
                    if wd in tk and wd != tk:
                        region_wds.remove(wd)
        '''停用词'''
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        # 切分句子
        sent_tokens = self.sent_split(sent)
        # n-gram
        n_tokens = []
        for gram_l in range(1, len(sent_tokens) + 1):
            for start in range(len(sent_tokens) - gram_l + 1):
                n_tokens.append(' '.join(sent_tokens[start: start + gram_l]))
        for wd in wds:
            if wd in n_tokens:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while True:
        question = input('input an question:')
        data = handler.classify(question)
        handler.check_medical(question)
        print(data)
