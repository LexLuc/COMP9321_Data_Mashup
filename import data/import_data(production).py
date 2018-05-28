import pandas as pd
from pymongo import MongoClient
import re
import xlrd

datapath='./data/AFAS_2016_ProductionHistorical_V1.0.0.xls'
excel=xlrd.open_workbook(datapath)

client=MongoClient("mongodb://admin:qwer1234@ds117739.mlab.com:17739/fish")
db=client["fish"]
db.authenticate('admin','qwer1234')

# def check_value(value):
#     if value=='0':
#         return 0.0
#     elif value=='na':
#         return

def get_fish_detail(table,colume):
    detail={
        'Tuna':{'value':table.cell(10,colume).value,
                'volume':table.cell(31,colume).value},
        'Salmonids':{'value':table.cell(11,colume).value,
                     'volume':table.cell(32,colume).value},
        'Other_fish':{'value':table.cell(12,colume).value,
                      'volume':table.cell(33,colume).value},
        'Prawns':{'value':table.cell(15,colume).value,
                  'volume':table.cell(36,colume).value},
        'Rock lobster':{'value':table.cell(16,colume).value,
                        'volume':table.cell(37,colume).value},
        'Crab':{'value':table.cell(17,colume).value,
                'volume':table.cell(38,colume).value},
        'Other_Curstaceans':{'value':table.cell(18,colume).value,
                             'volume':table.cell(39,colume).value},
        'Abalone':{'value':table.cell(21,colume).value,
                   'volume':table.cell(42,colume).value},
        'Scallop':{'value':table.cell(22,colume).value,
                   'volume':table.cell(43,colume).value},
        'Oyster':{'value':table.cell(23,colume).value,
                  'volume':table.cell(44,colume).value},
        'Squid':{'value':table.cell(24,colume).value,
                 'volume':table.cell(45,colume).value},
        'Other_Molluscs':{'value':table.cell(25,colume).value,
                          'volume':table.cell(46,colume).value},

    }
    keylist=list(detail.keys())
    for key in keylist:
        if detail[key]['volume']=='0' \
                and detail[key]['value']=='0':
            detail[key]['volume'] = 0.0
            detail[key]['value'] = 0.0
            detail[key]['unit_price'] = 0.0
        elif detail[key]['volume']=='na' \
                and detail[key]['value']=='na':
            detail[key]['volume']=0.0
            detail[key]['value']=0.0
            detail[key]['unit_price']=0.0

        elif detail[key]['volume'] not in ['0','na'] and detail[key]['value'] not in ['0','na']:
            # print(key,detail[key]['value'],detail[key]['volume'])
            detail[key]['unit_price']=detail[key]['value']/detail[key]['volume']
        else:
            detail[key]['volume'] = 0.0
            detail[key]['value'] = 0.0
            detail[key]['unit_price'] = 0.0
    return detail

def create_entity(table,colume):
    result={'year':table.cell(6,1).value.split(" in ")[1][0:4],
            'total':{'value':table.cell(28,colume).value,'volume':table.cell(49,colume).value}
            }
    fish_detail=get_fish_detail(table,colume)

    result.update(fish_detail)
    # print(result)
    return result


sheets=[
    'Aust fish prod 05-06',
    'Aust fish prod 06-07',
    'Aust fish prod 07-08',
    'Aust fish prod 08-09',
    'Aust fish prod 09-10',
    'Aust fish prod 10-11',
    'Aust fish prod 11-12',
    'Aust fish prod 12-13',
    'Aust fish prod 13-14',
    'Aust fish prod 14-15 ',
    'Aust fish prod 15-16']

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
print(stat_list)
data=dict.fromkeys(stat_list)

for state in stat_list:
    temp=[]
    colume=state_col[state]
    # print(colume)
    print('----------------------'+state)
    for sheet in sheets:
        print('*************************'+sheet)
        table=excel.sheet_by_name(sheet)
        temp.append(create_entity(table,colume))
    data[state]=temp
        # print(data)
# print(data)
for state in stat_list:
    # print(data[state])
    collection=client.fish[state+'_production']
    collection.delete_many({})
    collection.insert_many(data[state])
