import xlrd

datapath='./data/AFAS_2016_ProductionHistorical_V1.0.0.xls'
excel=xlrd.open_workbook(datapath)
table=excel.sheet_by_name('Aust fish prod 05-06')
print(table.cell(6,1).value.find('2005'))
print(table.cell(6,1).value[49:53])
print(table.cell(10,2).value)
print(type(table.cell(10,2).value))