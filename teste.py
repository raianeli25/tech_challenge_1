import requests
from bs4 import BeautifulSoup
import re

x = requests.get('http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1989&opcao=opt_02')

html_doc = x.text

soup = BeautifulSoup(html_doc, 'html.parser')

#extract table infos into a dict
data = []
for row in soup.find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
        row_data.append(cell.text)
    data.append(row_data)

#cut data
for index in range(len(data)):
    for sub_index in range(len(data[index])):
        if 'Ano:' in data[index][sub_index]:
            data_new = data[index+1:]
        if 'Total' in data[index][sub_index]:
            data_new = data_new[:-(len(data)-index)+1]

#cleaning data
for index in range(len(data_new)):
    for sub_index in range(len(data_new[index])):
        data_new[index][sub_index] = re.sub(r"[\n]", "", data_new[index][sub_index]).strip().replace('-','0').replace('.','')

print(data_new)

#convert to dict
res= {"data":""}
categorias=['VINHO DE MESA','VINHO FINO DE MESA (VINÍFERA)','SUCO','DERIVADOS']
for index in range(0,len(data_new)):
    if data_new[index] != []: 
        import ipdb; ipdb.set_trace()
        try:
            if categorias.index(data_new[index][0]) != None:
                res['data'][data_new[index][0]] == []
                categoria=data_new[index][0]
                res['data'][categoria].append({'Produto':data_new[index][0],'Quantidade(L.)':float(data_new[index][1])})
        except:
            pass
print(res)  