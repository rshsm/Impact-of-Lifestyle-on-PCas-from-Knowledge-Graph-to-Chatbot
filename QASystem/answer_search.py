#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="rdxsdzxgc123")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            '''查询类别'''
            question_type = sql_['question_type']
            '''查询类别对应的查询语句'''
            queries = sql_['sql']
            answers = []
            for qu in queries:
                ress = self.g.run(qu).data()
                answers.append(ress)
            for ans in answers:
                '''reply是一条字符串'''
                reply = self.answer_prettify(question_type, ans)
                if reply:
                    final_answers.append(reply)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板,这一块已经看懂'''

    def answer_prettify(self, question_type, answers):
        final_answer = ''
        if not answers:
            return ''
        if question_type == 'related_papers':
            desc = [i['q.name'] for i in answers]
            subject = answers[0]['p.name']
            if len(desc) >= 1:
                final_answer = 'The PMID of related researches about {0} are: {1}.'.format(
                    subject, '; '.join(list(set(desc))[:self.num_limit]))
            if len(desc) == 1:
                final_answer = 'The PMID of related researches about {0} is: {1}.'.format(
                    subject, '; '.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'askpaper_inf':
            desc = 'Title: ' + answers[0]['p.title'] + '; ' + 'Author: ' + \
                   answers[0]['p.author'] + '; ' + 'Study_Type: ' + answers[0]['p.study_type'] +\
                   '; ' + 'Year: ' + answers[0]['p.year'] + '.'
            subject = answers[0]['p.name']
            final_answer = 'The detailed information of survey {0} is as follows: {1}'.format(
                subject, desc)

        elif question_type == 'corresponding_units':
            desc = [i['q.name'] for i in answers]
            subject = answers[0]['p.name']
            final_answer = 'The corresponding units of {0} are: {1}.'.format(
                subject, '; '.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'lfst_pcas':
            desc = [i['q.name'] for i in answers]
            subject = answers[0]['p.name']
            final_answer = 'The lifestyle {0} may lead to: {1}.'.format(
                subject, '; '.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'factor_type':
            subject = answers[0]['p.name']
            desc = answers[0]['p.factor_type']
            final_answer = 'The influence factor of {0} is {1}'.format(
                subject, desc)

        elif question_type == 'lfst_baseline':
            desc_basname = [i['q.name'] for i in answers]
            subject = answers[0]['p.name']
            final_answer = 'The possible baselines of {0} are {1}'.format(
                subject, ';'.join(list(set(desc_basname))[:self.num_limit]))

        elif question_type == 'askbsl_inf':
            desc = 'index_name: ' + answers[0]['p.index_name'] + '; ' + 'group_number: ' + str(
                answers[0]['p.group_number']) + '; ' + 'stratification: ' + str(
                answers[0]['p.stratification']) + '; ' + 'value: ' + str(
                answers[0]['p.value']) + '.'
            subject = answers[0]['p.name']
            final_answer = subject + ': ' + '( ' + desc + ' )'

        elif question_type == 'lfst_pca_outcome':
            desc_outname = [i['q.name'] for i in answers]
            desc_pca = answers[0]['q.pcatype']
            subject = answers[0]['p.name']
            final_answer = 'When lifestyle {0} leads to {1}, the serial id of possible outcomes are: {2}'.format(
                subject, desc_pca, ';'.join(list(set(desc_outname))[:self.num_limit]))

        elif question_type == 'askotc_inf':
            desc = 'index_name: ' + answers[0]['p.index_name'] + '; ' + 'pcatype: ' + answers[0]['p.pcatype'] + '; ' \
                   + 'eaj: ' + str(answers[0]['p.eaj']) + ', ' + 'aj_value: ' + str(answers[0]['p.aj_value']) \
                   + '; ' + 'eunaj: ' + str(answers[0]['p.eunaj']) + ', ' + 'unaj_value: ' + str(answers[0]['p.unaj_value']) \
                   + '; ' + 'stratification: ' + str(answers[0]['p.stratification']) + '; ' + 'notes: ' \
                   + str(answers[0]['p.notes']) + '.'
            subject = answers[0]['p.name']
            final_answer = subject + ': ' + '( ' + desc + ' )'

        elif question_type == 'lfst_class':
            desc = [i['p.fenlei'] for i in answers]
            subject = answers[0]['p.name']
            final_answer = 'The {0} belongs to class of: {1}.'.format(
                subject, '; '.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'lfst_nation':
            desc = [i['q.name'] for i in answers]
            subject = answers[0]['p.name']
            final_answer = 'We find that the {0} appears in {1}.'.format(
                subject, '; '.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'pca_gene':
            desc = [i['q.name'] for i in answers]
            subject = answers[0]['p.name']
            final_answer = 'The {0} has potential correlations with gene such as {1}.'.format(
                subject, '; '.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
