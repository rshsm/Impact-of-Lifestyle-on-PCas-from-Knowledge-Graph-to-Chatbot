# coding: utf-8
import json
import pickle
from helper import get_synonmys_tolist, get_ncicode

with open('./data/pcalistdb_lifestyle.json', 'r', encoding='utf8') as f:
    js_dict = json.load(f)
    js_list = js_dict['RECORDS']
    f.close()

pca_lifestyle_list = js_list
for v in pca_lifestyle_list:
    v['Synonmys'] = get_synonmys_tolist(v['Synonmys'])
    v['NCI_code'] = get_ncicode(v['NCI_code'])

print(len(pca_lifestyle_list))
# lifestyles = []
# for sin_otc in pca_otcdict_list:
#     lifestyles.append(sin_otc['Name'])
# lifestyles = list(set(lifestyles))
#
# testlist = []
# for lfst in lifestyles:
#     for e in pca_lifestyle_list:
#         if lfst in e['Name'] or lfst in e['Synonmys']:
#             testlist.append([lfst, e['Name']])
