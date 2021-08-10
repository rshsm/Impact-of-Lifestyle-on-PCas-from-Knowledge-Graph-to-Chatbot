#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Date: 21-03-25

class QuestionParser:

    '''构建实体节点'''

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'related_papers':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'askpaper_inf':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('paper'))

            elif question_type == 'corresponding_units':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'lfst_pcas':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'lfst_baseline':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'askbsl_inf':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('baseline'))

            elif question_type == 'factor_type':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'lfst_pca_outcome':
                lfsts = entity_dict.get('lifestyle')
                pcas = entity_dict.get('pca_type')
                double_entities = []
                for l in lfsts:
                    for p in pcas:
                        double_entities.append([l, p])
                sql = self.sql_transfer(question_type, double_entities)

            elif question_type == 'askotc_inf':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('outcome'))

            elif question_type == 'lfst_class':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'lfst_nation':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('lifestyle'))

            elif question_type == 'pca_gene':
                sql = self.sql_transfer(
                    question_type, entity_dict.get('pca_type'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询生活方式的相关文献
        if question_type == 'related_papers':
            sql = [
                "MATCH (p:Lifestyle)-[r:related_papers]-(q:Paper) where p.name = '{0}' return p.name, q.name".format(i) for i in entities]

        # 查询研究的详细信息
        elif question_type == 'askpaper_inf':
            sql = ["MATCH (p:Paper) where p.name = '{0}' return p.name,p.title,p.author,p.study_type,p.year".format(
                i) for i in entities]

        # 查询生活方式对应的单位
        elif question_type == 'corresponding_units':
            sql = [
                "MATCH (p:Lifestyle)-[r:units_of_lfst]-(q:Unit) where p.name = '{0}' return p.name, q.name".format(i) for i in entities]

        # 查询生活方式会导致的前列腺癌
        elif question_type == 'lfst_pcas':
            sql = [
                "MATCH (p:Lifestyle)-[r:lead_PCas]-(q:PCA_Cancer) where p.name = '{0}' return p.name, q.name".format(i) for i in entities]

        # 查询生活方式的影响因子
        elif question_type == 'factor_type':
            sql = ["MATCH (p:Lifestyle) where p.name = '{0}' return p.name, p.factor_type".format(i) for i in entities]

        # 查询生活方式的baseline
        elif question_type == 'lfst_baseline':
            sql = ["MATCH (p:Lifestyle)-[r:baselines_of_lfst]-(q:Baseline) where p.name = '{0}' return p.name, q.name".format(i) for i in entities]

        # 查询baseline的具体信息
        elif question_type == 'askbsl_inf':
            sql = ["MATCH (p:Baseline) WHERE p.name = '{0}' RETURN p.name, p.index_name, p.group_number, p.stratification, p.value".format(
                i) for i in entities]

        # 查询生活方式对应的前列腺癌症带来的后果
        elif question_type == 'lfst_pca_outcome':
            sql = [
                "MATCH (p:Lifestyle)-[r:outcomes_of_lfst]-(q:Outcome) where p.name = '{0}' and q.pcatype = '{1}' return p.name, q.pcatype, q.name".format(
                    en[0],
                    en[1]) for en in entities]

        # 查询outcome的具体信息
        elif question_type == 'askotc_inf':
            sql = ["MATCH (p:Outcome) WHERE p.name = '{0}' RETURN p.name, p.index_name, p.pcatype, p.eaj, p.aj_value, p.eunaj, p.unaj_value, p.stratification, p.notes".format(
                i) for i in entities]

        # 查询生活方式属于的class
        elif question_type == 'lfst_class':
            sql = ["MATCH (p:Lifestyle) where p.name = '{0}' return p.name, p.fenlei".format(
                i) for i in entities]

        # 查询生活方式属于的nation
        elif question_type == 'lfst_nation':
            sql = [
                "MATCH (p:Lifestyle)-[r:nations_of_lfst]-(q:Nation) where p.name = '{0}' return p.name, q.name".format(i) for i in entities]

        # 查询影响pca的基因
        elif question_type == 'pca_gene':
            sql = [
                "MATCH (p:PCA_Cancer)-[r:cancer_by_gene]-(q:Gene) where p.name = '{0}' return p.name, q.name".format(i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionParser()
