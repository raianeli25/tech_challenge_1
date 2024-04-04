import requests
from bs4 import BeautifulSoup
import re

def html_to_list(url):

    x = requests.get(url)

    html_doc = x.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    #extract table infos into a list
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
                data_new = data_new[:-(len(data)-index)]

    #cleaning data
    for index in range(len(data_new)):
        for sub_index in range(len(data_new[index])):
            data_new[index][sub_index] = re.sub(r"[\n]", "", data_new[index][sub_index]).strip().replace('-','0').replace('nd','0').replace('*','0').replace('.','')

    return data_new

def get_export_import_page(url,tipo_produto,ano):
    
    data_new = html_to_list(url)

    #convert to dict
    res= {"data":[]}
    for index in range(0,len(data_new)):
        if data_new[index] != []: 
            res['data'].append({'País':data_new[index][0],'Quantidade(kg)':float(data_new[index][1]),'Valor(US$)':float(data_new[index][2]),'Tipo produto':tipo_produto,'Ano': ano})

    return res        

def get_production_commercialization_processing_page(url,categorias,tipo_produto,ano):

    data_new = html_to_list(url)

    #convert to dict
    res= {"data":[]}
    for index in range(0,len(data_new)):
        if data_new[index] != []: 
            try:
                if categorias.index(data_new[index][0]) != None:
                    categoria = data_new[index][0]
                    total = data_new[index][1]
            except:
                pass
            if data_new[index][0] not in categorias:
                if tipo_produto != None:
                        res['data'].append({'Produto':data_new[index][0],'Quantidade(L.)':float(data_new[index][1]),'Categoria':categoria, 'Tipo produto': tipo_produto, 'Total Categoria':float(total),'Ano': ano})
                else:
                    res['data'].append({'Produto':data_new[index][0],'Quantidade(L.)':float(data_new[index][1]),'Categoria':categoria, 'Total Categoria':float(total),'Ano': ano})
    return res

