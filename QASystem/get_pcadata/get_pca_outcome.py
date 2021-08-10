# coding: utf-8
import json
from helper import deal_dict_value, get_base_str

with open('./data/pcalistdb_outcome.json', 'r', encoding='utf8') as f:
    js_dict = json.load(f)
    js_list = js_dict['RECORDS']
    f.close()

pca_otcdict_list = []
count = 0
cox_regression = [
    'proportional hazards model',
    'cox proportional hazards',
    'cox proportional hazards model',
    'cox regression models',
    'cox regression modeling',
    'cox proportional hazards regression model',
    'cox proportional hazards models']
logistic_regression = [
    'logistic regression model',
    'logistic regression analysis',
    'logistic regression models',
    'logistic regression analyses',
    'logistic regression']


for v in js_list:
    pca_singotc_dict = {}
    pca_singotc_dict['OutID'] = 'pcaoc_' + str(v['ID'])
    pca_singotc_dict['PMID'] = v['PMID']
    # pca_singotc_dict['Group_number'] = get_base_str(v['Group_number'])
    pca_singotc_dict['Pca_type'] = get_base_str(v['Pca_type'])
    # 三类
    pca_singotc_dict['First_Class'] = get_base_str(v['First_Class'])
    pca_singotc_dict['Second_Class'] = get_base_str(v['Second_Class'])
    pca_singotc_dict['Third_Class'] = get_base_str(v['Third_Class'])
    pca_singotc_dict['Index_name'] = get_base_str(v['Index_name'])
    pca_singotc_dict['Name'] = v['Name'].lower().strip()
    pca_singotc_dict['Unit'] = get_base_str(v['Unit'])
    pca_singotc_dict['Stratification'] = get_base_str(v['Stratification'])
    pca_singotc_dict['Sample_size'] = deal_dict_value(v['Sample_size'])
    pca_singotc_dict['N_of_pca'] = deal_dict_value(v['N_of_pca'])
    pca_singotc_dict['Pca_incidence'] = deal_dict_value(v['Pca_incidence'])
    pca_singotc_dict['Statistical_model'] = get_base_str(
        v['Statistical_model'])
    if pca_singotc_dict['Statistical_model'] in cox_regression:
        pca_singotc_dict['Statistical_model'] = cox_regression[0]
    if pca_singotc_dict['Statistical_model'] in logistic_regression:
        pca_singotc_dict['Statistical_model'] = logistic_regression[0]
    # pca_singotc_dict['type_of_Effect_index,OR/RR/IQR;'] = deal_dict_value(v['type_of_Effect_index,OR/RR/IQR;'])
    pca_singotc_dict['Effect_index_UnAj'] = get_base_str(
        v['Effect_index_UnAj'])
    pca_singotc_dict['N_of_pca'] = deal_dict_value(v['N_of_pca'])
    pca_singotc_dict['P_UnAj'] = deal_dict_value(v['P_UnAj'])
    pca_singotc_dict['Effect_index_Aj'] = get_base_str(v['Effect_index_Aj'])
    pca_singotc_dict['P_Aj'] = deal_dict_value(v['P_Aj'])
    # pca_singotc_dict['Effect_index_X'] = deal_dict_value(v['Effect_index_X'])
    if v['P_X'] is None:
        pca_singotc_dict['P_X'] = 'NA'
    else:
        pca_singotc_dict['P_X'] = v['P_X']
    # pca_singotc_dict['Ptrend,Adjusted/Unadjusted'] = deal_dict_value(v['Ptrend,Adjusted/Unadjusted'])
    # pca_singotc_dict['Data_type'] = deal_dict_value(v['Data_type'])
    pca_singotc_dict['Notes'] = deal_dict_value(v['Notes'])
    if v['a'] is None:
        pca_singotc_dict['a'] = 'NA'
    else:
        pca_singotc_dict['a'] = v['a']
    pca_otcdict_list.append(pca_singotc_dict)
    count += 1
