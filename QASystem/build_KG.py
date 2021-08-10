#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
from get_pcadata.get_pca_main import pca_mainlist
from get_pcadata.get_pca_baseline import pca_base_list
from get_pcadata.get_pca_outcome import pca_otcdict_list
from helper import deal_cancers, get_base_str, doulist_rem
import os
import json
from py2neo import Graph, Node


def delete_lien(liebiao, e):
    if e in liebiao:
        liebiao.remove(e)
        return liebiao
    else:
        return liebiao


class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="rdxsdzxgc123")

    def read_nodes(self):
        lfstys_info = []
        papers_info = []
        baselines_info = pca_base_list
        outcomes_info = pca_otcdict_list

        '''共12类节点'''
        lifestyles = []
        units = []
        nations = []
        # sta_models = []
        firclas = []
        secclas = []
        thrclas = []
        papers = []
        cancers = []
        genes = []
        base_entities = []
        otc_entities = []

        '''共13对关系'''
        lifestyles_papers = []
        lifestyles_cancers = []
        lifestyles_units = []
        lifestyles_nations = []
        # lifestyles_models = []
        lifestyles_firclas = []
        lifestyles_secclas = []
        lifestyles_thrclas = []
        cancers_genes = []
        papers_genes = []

        papers_baselines = []
        papers_outcomes = []

        lifestyles_baselines = []
        lifestyles_outcomes = []

        pcatype_outcomes = []

        '''提取生活方式实体,单位实体，统计模型实体，种类实体'''
        for sin_otc in pca_otcdict_list:
            if sin_otc['Name'] not in lifestyles:
                lifestyles.append(sin_otc['Name'])

            if sin_otc['Unit'] not in units:
                units.append(sin_otc['Unit'])

            # if sin_otc['Statistical_model'] not in sta_models:
            #     sta_models.append(sin_otc['Statistical_model'])

            if sin_otc['First_Class'] not in firclas:
                firclas.append(sin_otc['First_Class'])

            if sin_otc['Second_Class'] not in secclas:
                secclas.append(sin_otc['Second_Class'])

            if sin_otc['Third_Class'] not in thrclas:
                thrclas.append(sin_otc['Third_Class'])

        lifestyles = delete_lien(lifestyles, 'NA')
        units = delete_lien(units, 'NA')
        # sta_models = delete_lien(sta_models, 'NA')
        firclas = delete_lien(firclas, 'NA')
        secclas = delete_lien(secclas, 'NA')
        thrclas = delete_lien(thrclas, 'NA')

        '''生活方式信息'''
        for lfst in lifestyles:
            '''初始化'''
            lfst_sin_infdict = {}
            lfst_sin_infdict['name_lifestyle'] = lfst
            lfst_sin_infdict['level_class'] = []
            lfst_sin_infdict['pca_type'] = []
            lfst_sin_infdict['index_name'] = []
            lfst_sin_infdict['involved_papers'] = []
            lfst_sin_infdict['fenlei_of_lfst'] = ''
            # lfst_sin_infdict['Statistical_model'] = ''
            lfst_sin_infdict['unit'] = []
            lfst_sin_infdict['Type_of_factor'] = []
            for otc in pca_otcdict_list:
                if lfst == otc['Name']:
                    lfst_sin_infdict['involved_papers'].append(otc['PMID'])
                    lfst_sin_infdict['pca_type'].append(otc['Pca_type'])
                    lfst_sin_infdict['index_name'].append(otc['Index_name'])
                    lfst_sin_infdict['level_class'].append(
                        [otc['First_Class'], otc['Second_Class'], otc['Third_Class']])
                    lfst_sin_infdict['unit'].append(otc['Unit'])
                    # lfst_sin_infdict['Statistical_model'] = otc['Statistical_model']
                    if otc['P_X'] == 'NA' or otc['a'] == 'NA':
                        lfst_sin_infdict['Type_of_factor'].append('NA')
                    else:
                        if otc['P_X'] == '<0.05' and float(otc['a']) < 1:
                            if float(otc['a']) < 0.7:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Protective factor; impact level:Strong')
                            if float(
                                    otc['a']) >= 0.7 and float(
                                    otc['a']) < 0.9:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Protective factor; impact level:Medium')
                            if float(otc['a']) >= 0.9 and float(otc['a']) < 1:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Protective factor; impact level:Weak')
                        elif otc['P_X'] == '<0.05' and float(otc['a']) >= 1 and float(otc['a']) < 1.2:
                            lfst_sin_infdict['Type_of_factor'].append(
                                'No influencing factor')
                        elif otc['P_X'] == '<0.05' and float(otc['a']) >= 1.2:
                            if float(
                                    otc['a']) >= 1.2 and float(
                                    otc['a']) < 1.5:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Risk factor; impact level:Weak')
                            if float(
                                    otc['a']) >= 1.5 and float(
                                    otc['a']) < 3.0:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Risk factor; impact level:Medium')
                            if float(otc['a']) >= 3.0 and float(otc['a']) < 10:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Risk factor; impact level:Strong')
                            if float(otc['a']) >= 10:
                                lfst_sin_infdict['Type_of_factor'].append(
                                    'Risk factor; impact level:Super strong')
                        else:
                            lfst_sin_infdict['Type_of_factor'].append(
                                'No statistical significance factor')

            lfst_sin_infdict['level_class'] = lfst_sin_infdict['level_class'][0]
            lfst_sin_infdict['fenlei_of_lfst'] = lfst_sin_infdict['level_class'][0]
            '''单位'''
            lfst_sin_infdict['unit'] = list(set(lfst_sin_infdict['unit']))
            if len(lfst_sin_infdict['unit']
                   ) >= 2 and 'NA' in lfst_sin_infdict['unit']:
                lfst_sin_infdict['unit'].remove('NA')
            '''可能导致的pca'''
            lfst_sin_infdict['pca_type'] = list(
                set(lfst_sin_infdict['pca_type']))
            lfst_sin_infdict['index_name'] = list(
                set(lfst_sin_infdict['index_name']))
            '''涉及到的文献去重并统计文献总数'''
            lfst_sin_infdict['involved_papers'] = list(
                set(lfst_sin_infdict['involved_papers']))
            lfst_sin_infdict['paper_count'] = len(
                lfst_sin_infdict['involved_papers'])
            lfst_sin_infdict['Type_of_factor'] = list(
                set(lfst_sin_infdict['Type_of_factor']))
            if len(lfst_sin_infdict['Type_of_factor']
                   ) >= 2 and 'NA' in lfst_sin_infdict['Type_of_factor']:
                lfst_sin_infdict['Type_of_factor'].remove('NA')
            lfstys_info.append(lfst_sin_infdict)

        # for inf_dict in lfstys_info:
        #     inf_dict['Stratification'] = []
        #     for paper in inf_dict['involved_papers']:
        #         strati = ''
        #         for otc in pca_otcdict_list:
        #             if paper == otc['PMID'] and otc['Name'] == inf_dict['name_lifestyle']:
        #                 strati = strati + otc['Stratification'] + '*'
        #         strati = strati.strip('*')
        #         strati = ';'.join(list(set(strati.split('*'))))
        #         inf_dict['Stratification'].append([paper, strati])

        '''以上就是生活方式的信息'''

        '''参考文献实体，参考文献信息'''
        for pcamain in pca_mainlist:
            paper_info_dict = {}
            papers.append(pcamain['PMID'])

            '''填入单个文献字典'''
            paper_info_dict['PMID'] = pcamain['PMID']
            paper_info_dict['Title'] = pcamain['Title']
            paper_info_dict['Author'] = pcamain['Author']
            paper_info_dict['Year'] = pcamain['Year']
            paper_info_dict['Area'] = pcamain['Area']
            nations.extend(paper_info_dict['Area'])
            paper_info_dict['Duration'] = pcamain['Duration']
            paper_info_dict['Study_type'] = pcamain['Study_type']
            paper_info_dict['Sample_size'] = pcamain['Sample_size']
            if pcamain['Associated_genes'] == 'NA':
                paper_info_dict['gene'] = ['NA']
            else:
                paper_info_dict['gene'] = [
                    as_ge.strip() for as_ge in pcamain['Associated_genes'].split(',')]
                genes.extend(paper_info_dict['gene'])
            papers_info.append(paper_info_dict)

        '''基因种类实体'''
        genes = list(set(genes))
        genes = delete_lien(genes, 'NA')

        '''nations实体'''
        nations = list(set(nations))
        nations = delete_lien(nations, 'NA')

        '''参考文献和基因的关系'''
        for paper_dict in papers_info:
            if paper_dict['gene'] != ['NA']:
                for v in paper_dict['gene']:
                    if [paper_dict['PMID'], v] not in papers_genes:
                        papers_genes.append([paper_dict['PMID'], v])

        for lfst_dict in lfstys_info:
            '''前列腺癌种类实体库'''
            for pca in lfst_dict['pca_type']:
                cancers.append(pca)
            '''生活方式与参考文献的关系'''
            for paper in lfst_dict['involved_papers']:
                if paper != 'NA':
                    lifestyles_papers.append(
                        [lfst_dict['name_lifestyle'], paper])
            '''生活方式和癌症种类的关系'''
            for pca in lfst_dict['pca_type']:
                if pca != 'NA':
                    lifestyles_cancers.append(
                        [lfst_dict['name_lifestyle'], pca])
            '''生活方式和单位的关系'''
            for u in lfst_dict['unit']:
                if u != 'NA':
                    lifestyles_units.append([lfst_dict['name_lifestyle'], u])
            '''生活方式和统计模型的关系'''
            # for model in lfst_dict['Statistical_model']:
            #     if model != 'NA':
            #         lifestyles_models.append(
            #             [lfst_dict['name_lifestyle'], model])

            '''生活方式和三个类的关系'''
            if lfst_dict['level_class'][0] != 'NA':
                lifestyles_firclas.append(
                    [lfst_dict['name_lifestyle'], lfst_dict['level_class'][0]])
            if lfst_dict['level_class'][1] != 'NA':
                lifestyles_secclas.append(
                    [lfst_dict['name_lifestyle'], lfst_dict['level_class'][1]])
            if lfst_dict['level_class'][2] != 'NA':
                lifestyles_thrclas.append(
                    [lfst_dict['name_lifestyle'], lfst_dict['level_class'][2]])

        '''前列腺癌种类去重'''
        cancers = list(set(cancers))
        cancers = delete_lien(cancers, 'NA')

        '''癌症种类和基因的关系'''
        for rl in papers_genes:
            for pcm in pca_mainlist:
                if rl[0] == pcm['PMID']:
                    if [pcm['Pca_type'], rl[1]] not in cancers_genes:
                        cancers_genes.append([pcm['Pca_type'], rl[1]])

        '''base实体添加'''
        for pca_basedict in baselines_info:
            base_entities.append(pca_basedict['PcabaseID'])

        '''outcome实体添加'''
        for otc in outcomes_info:
            otc_entities.append(otc['OutID'])

        # 生活方式和baseline以及outcome之间的关系
        for lfst_dict in lfstys_info:
            for ind_na in lfst_dict['index_name']:

                for pca_basedict in baselines_info:
                    if ind_na == pca_basedict['Index_name']:
                        lifestyles_baselines.append(
                            [lfst_dict['name_lifestyle'], pca_basedict['PcabaseID']])

                for otc in outcomes_info:
                    if ind_na == otc['Index_name']:
                        lifestyles_outcomes.append(
                            [lfst_dict['name_lifestyle'], otc['OutID']])

        for paper in papers:
            '''参考文献和base的关系'''
            for pca_basedict in pca_base_list:
                if paper == pca_basedict['PMID']:
                    papers_baselines.append([paper, pca_basedict['PcabaseID']])
            '''参考文献和otc的关系'''
            for otc in pca_otcdict_list:
                if paper == otc['PMID']:
                    papers_outcomes.append([paper, otc['OutID']])

        '''生活方式和nation的关系?'''
        for lf_pa in lifestyles_papers:
            for inf in papers_info:
                if lf_pa[1] == inf['PMID']:
                    for a in inf['Area']:
                        if a != 'NA':
                            lifestyles_nations.append([lf_pa[0], a])
        '''去重'''
        lifestyles_nations = doulist_rem(lifestyles_nations)

        '''cancer和outcomes的关系'''
        for pca in cancers:
            for otc in pca_otcdict_list:
                if pca == otc['Pca_type']:
                    pcatype_outcomes.append([pca, otc['OutID']])

        return lifestyles, units, nations, firclas, secclas, thrclas, papers, cancers, genes, base_entities, otc_entities, lfstys_info, papers_info, baselines_info, outcomes_info, \
            lifestyles_papers, lifestyles_nations, lifestyles_cancers, papers_genes, cancers_genes, lifestyles_baselines, lifestyles_outcomes, papers_baselines, papers_outcomes, lifestyles_units, \
            lifestyles_firclas, lifestyles_secclas, lifestyles_thrclas, pcatype_outcomes

    '''创建知识图谱节点(无属性添加)'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱节点(有属性添加)已阅'''

    def create_lfst_nodes(self, info):
        count = 0
        for lfst_dict in info:
            node = Node(
                "Lifestyle",
                name=lfst_dict['name_lifestyle'],
                level_class=lfst_dict['level_class'],
                pca_type=lfst_dict['pca_type'],
                index_name=lfst_dict['index_name'],
                inv_papers=lfst_dict['involved_papers'],
                fenlei=lfst_dict['fenlei_of_lfst'],
                unit=lfst_dict['unit'],
                factor_type=lfst_dict['Type_of_factor'],
                paper_count=str(
                    lfst_dict['paper_count']))
            self.g.create(node)
            count += 1
            print(count)
        return

    '''已阅'''

    def create_paper_nodes(self, info):
        count = 0
        for paper_dict in info:
            node = Node(
                "Paper",
                name=paper_dict['PMID'],
                title=paper_dict['Title'],
                author=paper_dict['Author'],
                year=paper_dict['Year'],
                area=paper_dict['Area'],
                duration=paper_dict['Duration'],
                sample_size=paper_dict['Sample_size'],
                study_type=paper_dict['Study_type'],
                gene=paper_dict['gene'])
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_baseline_nodes(self, info):
        count = 0
        for base_dict in info:
            node = Node(
                "Baseline",
                name=base_dict['PcabaseID'],
                pmid=base_dict['PMID'],
                group_number=base_dict['Group_number'],
                index_name=base_dict['Index_name'],
                stratification=base_dict['Stratification'],
                value=base_dict['P_value'],
                notes=base_dict['Notes'])
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_outcome_nodes(self, info):
        count = 0
        for otc_dict in info:
            node = Node(
                "Outcome",
                name=otc_dict['OutID'],
                pmid=otc_dict['PMID'],
                pcatype=otc_dict['Pca_type'],
                index_name=otc_dict['Index_name'],
                stratification=otc_dict['Stratification'],
                unit=otc_dict['Unit'],
                unaj_value=otc_dict['P_UnAj'],
                aj_value=otc_dict['P_Aj'],
                eunaj=otc_dict['Effect_index_UnAj'],
                eaj=otc_dict['Effect_index_Aj'],
                notes=otc_dict['Notes'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self):
        lifestyles, units, nations, firclas, secclas, thrclas, papers, cancers, genes, base_entities, otc_entities, lfstys_info, papers_info, baselines_info, outcomes_info, \
            lifestyles_papers, lifestyles_nations, lifestyles_cancers, papers_genes, cancers_genes, lifestyles_baselines, lifestyles_outcomes, papers_baselines, papers_outcomes, lifestyles_units, \
            lifestyles_firclas, lifestyles_secclas, lifestyles_thrclas, pcatype_outcomes = self.read_nodes()
        self.create_lfst_nodes(lfstys_info)
        print('num of lifestyles: ', len(lfstys_info))
        self.create_paper_nodes(papers_info)
        print('num of papers: ', len(papers_info))
        self.create_node('PCA_Cancer', cancers)
        print('num of cancer_types: ', len(cancers))
        self.create_node('Gene', genes)
        print('num of genes: ', len(genes))
        self.create_node('Unit', units)
        print('num of units: ', len(units))
        self.create_node('Nation', nations)
        print('num of nations: ', len(nations))
        # self.create_node('Statistical_model', sta_models)
        # print('num of statistical_models: ', len(sta_models))
        self.create_node('FirClass', firclas)
        print('num of firstclasses: ', len(firclas))
        self.create_node('SecClass', secclas)
        print('num of secondclasses: ', len(secclas))
        self.create_node('ThrClass', thrclas)
        print('num of thridclasses: ', len(thrclas))
        self.create_baseline_nodes(baselines_info)
        print('num of baselines: ', len(baselines_info))
        self.create_outcome_nodes(outcomes_info)
        print('num of outcomes: ', len(outcomes_info))
        return

    '''创建实体关系边'''

    def create_graphrels(self):
        lifestyles, units, nations, firclas, secclas, thrclas, papers, cancers, genes, base_entities, otc_entities, lfstys_info, papers_info, baselines_info, outcomes_info, \
            lifestyles_papers, lifestyles_nations, lifestyles_cancers, papers_genes, cancers_genes, lifestyles_baselines, lifestyles_outcomes, papers_baselines, papers_outcomes, lifestyles_units, \
            lifestyles_firclas, lifestyles_secclas, lifestyles_thrclas, pcatype_outcomes = self.read_nodes()
        self.create_relationship(
            'Lifestyle',
            'Paper',
            lifestyles_papers,
            'related_papers',
            '相关论文')
        self.create_relationship(
            'Lifestyle',
            'PCA_Cancer',
            lifestyles_cancers,
            'lead_PCas',
            '导致的PCas')
        self.create_relationship(
            'Paper',
            'Gene',
            papers_genes,
            'inv_genes',
            '文献涉及的基因')
        self.create_relationship(
            'PCA_Cancer',
            'Gene',
            cancers_genes,
            'cancer_by_gene',
            '基因影响的癌症')
        self.create_relationship(
            'Lifestyle',
            'Baseline',
            lifestyles_baselines,
            'baselines_of_lfst',
            '生式基准')
        self.create_relationship(
            'Lifestyle',
            'Outcome',
            lifestyles_outcomes,
            'outcomes_of_lfst',
            '生式结果')
        self.create_relationship(
            'Paper',
            'Baseline',
            papers_baselines,
            'baselines_in_papers',
            '文献中基准')
        self.create_relationship(
            'Paper',
            'Outcome',
            papers_outcomes,
            'outcomes_in_papers',
            '文献中结果')
        self.create_relationship(
            'Lifestyle',
            'Unit',
            lifestyles_units,
            'units_of_lfst',
            '单位')
        self.create_relationship(
            'Lifestyle',
            'Nation',
            lifestyles_nations,
            'nations_of_lfst',
            '国籍')
        self.create_relationship(
            'PCA_Cancer',
            'Outcome',
            pcatype_outcomes,
            'outcomes_of_pcatype',
            'PCa对应的结果')
        self.create_relationship(
            'Lifestyle',
            'FirClass',
            lifestyles_firclas,
            'first_class',
            '首类')
        self.create_relationship(
            'Lifestyle',
            'SecClass',
            lifestyles_secclas,
            'second_class',
            '次类')
        self.create_relationship(
            'Lifestyle',
            'ThrClass',
            lifestyles_thrclas,
            'third_class',
            '末类')

    '''创建实体关联边'''

    def create_relationship(
            self,
            start_node,
            end_node,
            edges,
            rel_type,
            rel_name):
        count = 0
        # 去重处理
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
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self):
        lifestyles, units, nations, firclas, secclas, thrclas, papers, cancers, genes, base_entities, otc_entities, lfstys_info, papers_info, baselines_info, outcomes_info, \
            lifestyles_papers, lifestyles_nations, lifestyles_cancers, papers_genes, cancers_genes, lifestyles_baselines, lifestyles_outcomes, papers_baselines, papers_outcomes, lifestyles_units, \
            lifestyles_firclas, lifestyles_secclas, lifestyles_thrclas, pcatype_outcomes = self.read_nodes()
        f_lfsty = open('dict/lfsty.txt', 'w+')
        f_paper = open('dict/paper.txt', 'w+')
        f_cancer = open('dict/cancer.txt', 'w+')
        f_gene = open('dict/gene.txt', 'w+')
        f_unit = open('dict/unit.txt', 'w+')
        f_nation = open('dict/nation.txt', 'w+')
        # f_stamod = open('dict/stamod.txt', 'w+')
        f_fircla = open('dict/fircla.txt', 'w+')
        f_seccla = open('dict/seccla.txt', 'w+')
        f_thrcla = open('dict/thrcla.txt', 'w+')
        f_baseline = open('dict/baseline.txt', 'w+')
        f_outcome = open('dict/outcome.txt', 'w+')

        f_lfsty.write('\n'.join(list(lifestyles)))
        f_paper.write('\n'.join(list(papers)))
        f_cancer.write('\n'.join(list(cancers)))
        f_gene.write('\n'.join(list(genes)))
        f_unit.write('\n'.join(list(units)))
        f_nation.write('\n'.join(list(nations)))
        # f_stamod.write('\n'.join(list(sta_models)))
        f_fircla.write('\n'.join(list(firclas)))
        f_seccla.write('\n'.join(list(secclas)))
        f_thrcla.write('\n'.join(list(thrclas)))
        f_baseline.write('\n'.join(list(base_entities)))
        f_outcome.write('\n'.join(list(otc_entities)))

        f_lfsty.close()
        f_paper.close()
        f_cancer.close()
        f_gene.close()
        f_unit.close()
        f_nation.close()
        # f_stamod.close()
        f_fircla.close()
        f_seccla.close()
        f_thrcla.close()
        f_baseline.close()
        f_outcome.close()

        return


if __name__ == '__main__':
    handler = MedicalGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")
    handler.create_graphrels()
    print("step3:实体写入文本文件中")
    handler.export_data()
