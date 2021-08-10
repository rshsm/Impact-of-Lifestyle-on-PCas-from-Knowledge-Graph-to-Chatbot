#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Date: 21-03-25

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = 'Sorry, there exists no answer in our KG that meets your questions!'
        '''给出问句的类别,类别可以不止一个'''
        res_classify = self.classifier.classify(sent)
        '''如果问句类别无法识别，则返回默认答案'''
        if not res_classify:
            return answer
        ''' 给出问句类别对应的sql语句, res_sql:[{'question_type': value,'sql_':value},...] '''
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = ChatBotGraph()
    while True:
        question = input('User:')
        answer = handler.chat_main(question)
        print('Bot:', answer)
