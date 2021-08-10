# coding: utf-8
import json
import re
from helper import txt_deal, deal_cancers, get_base_str

with open('./data/pcalistdb_main.json', 'r', encoding='utf8') as f:
    js_dict = json.load(f)
    js_list = js_dict['RECORDS']
    f.close()

# print(js_list)

nation_city = [['Australia',
                'Melbourne',
                'Sydney',
                'Perth',
                'New South Wales'],
               ['United States of America',
                'Puerto Rico',
                'Maryland',
                'North Carolina',
                'Winston-Salem',
                'Erie',
                'Niagara counties',
                'Minnesota',
                'San Francisco',
                'California'],
               ['United Kingdom',
                'England',
                'Scotland'],
               ['Iran',
                'Khorasan',
                'Tehran',
                'Isfahan',
                'Gilan',
                'Mazandaran',
                'Hamadan',
                'Lorestan',
                'Fars'],
               ['Finland',
                'Helsinki'],
               ['Korea',
                'Seoul'],
               ['Israel',
                'Western Jerusalem'],
               ['Spain',
                'Granada']]


def get_deal_str(s):
    if s is None:
        return 'NA'
    else:
        return s


def sol_stw(s):
    s = str(s)
    stopwds = ['.', 'The', 'the']
    for wd in stopwds:
        if wd in s:
            s = s.strip(wd)
    if 'and' in s:
        s = s.lstrip('and')
    return s.strip()


'''处理地域的函数'''


def deal_area(area):
    nameRegex = re.compile(r'\(.*\)')
    region_list = []
    newreg_list = []
    if area != 'NA':
        area = area.replace('\n', '')
        if '(' in area and ')' in area:
            mo = nameRegex.search(area)
            area = area.replace(mo.group(), '').strip()
            region_list.extend([v.strip() for v in area.split(',')])
        else:
            area = area.strip()
            region_list.extend([v.strip() for v in area.split(',')])
        region_list = [sol_stw(region) for region in region_list]
        '''特殊情况处理'''
        if '' in region_list:
            region_list.remove('')
        region_list = ['United Kingdom' if i ==
                       'UK' else i for i in region_list]
        for reg in region_list:
            if ' and ' in reg:
                weilist = [v.strip() for v in reg.split(' and ')]
                newreg_list.extend(weilist)
            else:
                newreg_list.append(reg)
        '''将城市变为所在的国家'''
        for i in range(len(newreg_list)):
            for nc in nation_city:
                if newreg_list[i] in nc[1:]:
                    newreg_list[i] = nc[0]
        newreg_list = list(set(newreg_list))
    else:
        newreg_list.append('NA')
    return newreg_list


pca_mainlist = []
# 计算导入条目个数
count = 0
# 清洗数据
for v in js_list:
    pca_sin_dict = {}
    pca_sin_dict['PMID'] = v['PMID']
    pca_sin_dict['Author'] = txt_deal(v['Author'])
    pca_sin_dict['Year'] = v['Year']
    pca_sin_dict['Title'] = txt_deal(v['Title'])
    pca_sin_dict['Study_type'] = txt_deal(v['Study_type'])
    pca_sin_dict['Meta_if'] = txt_deal(v['Meta_if'])
    pca_sin_dict['Pca_type'] = txt_deal(v['Pca_type'])
    pca_sin_dict['Cohort_name'] = txt_deal(v['Cohort_name'])
    pca_sin_dict['Area'] = deal_area(get_deal_str(v['Area']))
    pca_sin_dict['Duration'] = txt_deal(v['Duration'])
    pca_sin_dict['Group_number'] = v['Group_number']
    # 对组名进行列表切分
    if ';' in txt_deal(v['Group_name']):
        pca_sin_dict['Group_name'] = txt_deal(v['Group_name']).split(';')
    elif txt_deal(v['Group_name']) != '':
        pca_sin_dict['Group_name'] = [txt_deal(v['Group_name'])]
    else:
        pca_sin_dict['Group_name'] = txt_deal(v['Group_name'])
    # 对样本大小进行列表切分
    if ';' in txt_deal(v['Sample_size']):
        pca_sin_dict['Sample_size'] = txt_deal(v['Sample_size']).split(';')
    elif txt_deal(v['Sample_size']) != '':
        pca_sin_dict['Sample_size'] = [txt_deal(v['Sample_size'])]
    else:
        pca_sin_dict['Sample_size'] = txt_deal(v['Sample_size'])
    pca_sin_dict['RF_name'] = txt_deal(v['RF_name'])
    pca_sin_dict['RF_type'] = txt_deal(v['RF_type'])
    pca_sin_dict['RF_category'] = txt_deal(v['RF_category'])
    pca_sin_dict['RF_level'] = txt_deal(v['RF_level'])
    pca_sin_dict['RF_class'] = txt_deal(v['RF_class'])
    pca_sin_dict['Associated_genes'] = get_deal_str(v['Associated_genes'])
    pca_mainlist.append(pca_sin_dict)
    count += 1

# fei_list = []
# for v in pca_mainlist:
    # my_item = v['Study_type'].replace('.', ' ')
    # if ',' in my_item:
    #     fei_list.extend(item.strip() for item in my_item.split(','))
    # else:
    #     fei_list.append(my_item)
#     fei_list.append(v['Associated_genes'])
#
# print(len(pca_mainlist))

# total_areas = []
# for pm in pca_mainlist:
#     total_areas.extend(pm['Area'])
# total_areas = list(set(total_areas))
# total_areas.remove('NA')
# print(len(total_areas))
# for ta in total_areas:
#     print(ta)

# for pm in pca_mainlist:
#     print(pm['Area'])

# fei_list = ['United Kingdom' if i == 'UK' else i for i in fei_list]
# fei_list.remove('')
# fei_list = list(set(fei_list))
# print(len(fei_list))
# for e in fei_list:
#     print(e)
