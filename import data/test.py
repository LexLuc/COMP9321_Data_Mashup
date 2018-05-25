import xlrd

datapath='./data/AFAS_2016_ProductionHistorical_V1.0.0.xls'
excel=xlrd.open_workbook(datapath)
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
for sheet in sheets:
    # print('*************************' + sheet)
    table = excel.sheet_by_name(sheet)
    print(sheet)
    print(table.cell(25,4).value,table.cell(46,4).value)
