# coding: utf-8
import json
from helper import deal_dict_value, get_base_str

with open('./data/pcalistdb_baseline.json', 'r', encoding='utf8') as f:
    js_dict = json.load(f)
    js_list = js_dict['RECORDS']
    f.close()

# print(js_list)

pca_base_list = []
count = 0

for v in js_list:
    pca_singbase_dict = {}
    pca_singbase_dict['PcabaseID'] = 'pbase_' + str(count)
    pca_singbase_dict['PMID'] = v['PMID']
    # ?
    pca_singbase_dict['Group_number'] = deal_dict_value(v['Group_number'])
    # pca_singbase_dict['Pca_type'] = deal_dict_value(v['Pca_type'])
    pca_singbase_dict['Index_name'] = get_base_str(v['Index_name'])
    # pca_singbase_dict['Unit'] = deal_dict_value(v['Unit'])
    pca_singbase_dict['Stratification'] = get_base_str(v['Stratification'])
    # if deal_dict_value(v['Stratification']) == 'NA':
    #     pca_singbase_dict['Stratification'] = 'NA'
    # else:
    #     pca_singbase_dict['Stratification'] = [
    #         item.strip(':') for item in deal_dict_value(
    #             v['Stratification'])]
    pca_singbase_dict['Value_'] = deal_dict_value(v['Value_'])
    pca_singbase_dict['P_value'] = deal_dict_value(v['P_value'])
    # pca_singbase_dict['Data_type'] = deal_dict_value(v['Data_type'])
    pca_singbase_dict['Notes'] = deal_dict_value(v['Notes'])
    pca_base_list.append(pca_singbase_dict)
    count += 1

myindex_name = []
for sin in pca_base_list:
    myindex_name.append(sin['Index_name'])

myindex_name = list(set(myindex_name))
for ind in myindex_name:
    print(ind)

