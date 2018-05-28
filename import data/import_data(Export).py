import pandas as pd
from pymongo import MongoClient
import re
import xlrd


datapath='./data/AFAS_2016_Exports_v1.0.0.xlsx'
excel1=xlrd.open_workbook(datapath)
datapath='./data/AFAS_2013_Exports_v1.2.0.xls'
excel2=xlrd.open_workbook(datapath)
excel_list=[excel1,excel2]

client=MongoClient("mongodb://admin:qwer1234@ds117739.mlab.com:17739/fish")
db=client["fish"]
db.authenticate('admin','qwer1234')

years=['2013','2010','2014','2011','2015','2012']
def get_fish_detail(table,colume):
    detail={
        'Live':{'value':table.cell(10,colume).value,'volume':table.cell(28,colume).value},
        'Tuna':{'value':table.cell(11,colume).value,'volume':table.cell(29,colume).value},
        'Salmonids':{'value':table.cell(12,colume).value,'volume':table.cell(30,colume).value},
        'Swordfish':{'value':table.cell(13,colume).value,'volume':table.cell(31,colume).value},
        'Whiting':{'value':table.cell(14,colume).value,'volume':table.cell(32,colume).value},
        'Other_fish':{'value':table.cell(15,colume).value,'volume':table.cell(33,colume).value},
        'Prawns':{'value':table.cell(19,colume).value,'volume':table.cell(37,colume).value},
        'Rock lobster':{'value':table.cell(18,colume).value,'volume':table.cell(36,colume).value},
        'Crab':{'value':table.cell(22,colume).value,'volume':table.cell(40,colume).value},
        'Abalone':{'value':table.cell(20,colume).value,'volume':table.cell(38,colume).value},
        'Scallop':{'value':table.cell(21,colume).value,'volume':table.cell(39,colume).value},
        'Other_M&C':{'value':table.cell(23,colume).value,'volume':table.cell(41,colume).value},

    }
    keylist = list(detail.keys())
    for key in keylist:
        if detail[key]['volume'] == '0' \
                and detail[key]['value'] == '0':
            detail[key]['volume'] = 0.0
            detail[key]['value'] = 0.0
            detail[key]['unit_price'] = 0.0
        elif detail[key]['volume'] == 'na' \
                and detail[key]['value'] == 'na':
            detail[key]['volume'] = 0.0
            detail[key]['value'] = 0.0
            detail[key]['unit_price'] = 0.0
        elif detail[key]['volume'] not in ['0', 'na'] and detail[key]['value'] not in ['0', 'na']:
            # print(key,detail[key]['value'],detail[key]['volume'])
            detail[key]['unit_price'] = detail[key]['value'] / detail[key]['volume']
        else:
            print(key)
            detail[key]['volume'] = 0.0
            detail[key]['value'] = 0.0
            detail[key]['unit_price'] = 0.0
    return detail

def create_entity(table,colume,year):
    # print(table.row(6))
    result={
        'year':year,
            'total':{'value':table.cell(25,colume).value,'volume':table.cell(43,colume).value}
            }
    fish_detail=get_fish_detail(table,colume)

    result.update(fish_detail)
    # print(result)
    return result


sheets=[
    'Table 26',
    'Table 27',
    'Table 28'
    ]

state_col={
    'NSW':2,
    'Vic':3,
    'Qld':4,
    'SA':5,
    'WA':6,
    'Tas':7,
    'NT':8,
}
stat_list=list(state_col.keys())
# print(stat_list)
data=dict.fromkeys(stat_list)

for state in stat_list:
    i=0
    temp=[]
    colume=state_col[state]
    # print(colume)
    for sheet in sheets:
        for excel in excel_list:
            year=years[i]
            table=excel.sheet_by_name(sheet)
            temp.append(create_entity(table,colume,year))
            i+=1
    data[state]=temp
        # print(data)
# print(data)
for state in stat_list:
    # print(data[state])
    collection=client.fish[state+'_export']
    collection.delete_many({})
    collection.insert_many(data[state])
