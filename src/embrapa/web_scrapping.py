import requests
from bs4 import BeautifulSoup
import re
from embrapa.static_definitions import EmbrapaConstants

class EmbrapaCollect(EmbrapaConstants):
    def __init__(self) -> None:
        pass

    def parsing_url(self,opt_arg:str,subopt_arg:str,ano_arg:int)->str:
        '''
        Creates a suitable string representing the URL for requesting data to Embrapa Website.        
        Example: considering ano_arg=2020, opt_arg=processamento, subopt_arg=viniferas
        the URL string after correct parsing should be 
        http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2020&opcao=opt_03&subopcao=subopt_01
        Notice that for some options, there is no suboption.
        Example 2: considering year=2020, option=producao (and suboption=None)
        then http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2020&opcao=opt_02
        """
        '''
        if subopt_arg is None:
            url_request = self.URL_INDEX+self.REQ_YEAR+str(ano_arg)+"&"+self.REQ_OPTION+self.OPTIONS_DICT[opt_arg]
        else:
            url_request = self.URL_INDEX+self.REQ_YEAR+str(ano_arg)+"&"+self.REQ_SUBOPTION+self.SUBOPTIONS_DICT[opt_arg][subopt_arg]+"&"+self.REQ_OPTION+self.OPTIONS_DICT[opt_arg]
        return url_request

    def scrap_table_from_website(self, url:str):
        '''
        Receives the URL string, 
        makes the request to the website and returns its HTML table.
        '''
        x = requests.get(url)
        html_doc = x.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        return soup.find('table', {'class': 'tb_base tb_dados'})
    
    def extract_table_infos_into_list(self, table)->list:
        '''
        Extract all table infos from HTML table into a list.
        Example: 
        Input:
        table = 
        <tr><td> Argentina </td> <td> 25.276.991 </td> <td> 83.918.138 </td></tr>
        <tr><td> Brasil </td> <td> 6.229 </td> <td> 76.894 </td></tr>
        Output
        data =  [   [Argentina	25.276.991	83.918.138  ],
                    [Brasil	    6.229	    76.894      ] ]
        '''
        data:list = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(cell.text)
            data.append(row_data)

        return data

    def remove_total_row(self,data:list)->list:
        '''
        The row with "Total" value can be obtained from raw data.
        Thus, it can be despised.
        In this case, it is always the last row from the list.
        '''

        return data[:-1]

    def replace_invalid_null_chars(self,data_new:list)->list:
        '''
        "Invalid" values such as "-", "*" and "nd" are replaced
        by the constant VALUE_TO_REPLACE_NULL_CHAR.
        Also, numbers come as "string" with separation dots, which are removed.
        '''
        VALUE_TO_REPLACE_NULL_CHAR = EmbrapaConstants.VALUE_TO_REPLACE_NULL_CHAR
        for index in range(len(data_new)):
            for sub_index in range(len(data_new[index])):
                data_new[index][sub_index] = re.sub(r"[\n]", "", data_new[index][sub_index]).\
                    strip().\
                    replace('-',VALUE_TO_REPLACE_NULL_CHAR).\
                    replace('nd',VALUE_TO_REPLACE_NULL_CHAR).\
                    replace('*',VALUE_TO_REPLACE_NULL_CHAR).\
                    replace('.','')
                                
        return data_new

    def html_to_list(self,url:str):
        '''
        Receives the str URL to scrap,
        extract relevant infos into a list and treat invalid
        characters.
        '''
        table = self.scrap_table_from_website(url)
        data = self.extract_table_infos_into_list(table)
        data_new = self.remove_total_row(data)

        data_new = self.replace_invalid_null_chars(data_new)

        return data_new

    def check_if_not_empty(self, value:list)->bool:
        """
        The table has some empty rows (that should be removed).
        This method checks for them.
        """
        return value != []

    def check_if_category(self, value:str)->bool:
        """
        The table has some rows used to define categories.
        Such rows always have keys in UPPERCASE.
        This method identifies this pattern.
        """
        return value.isupper()

    def check_if_category_is_in_exception_list(self,category:str)->bool:
        '''
        In the page "comercializacao", there are some exceptional categories
        that also have values (representing the products themselves).
        This method checks for them for an after treatment.
        '''
        if category in self.CATEGORY_EXCEPTION_LIST:
            return True
        else:
            return False
    
    def check_if_tipo_produto_is_not_none(self, value:str)->bool:
        """
        Check if this page (option) has 
        an specific type "tipo_produto" (suboption)
        """
        return value != None

    def update_category(self, data:list)->tuple|None:
        """
        Check if this is a category and returns a tuple (categoria, total) in this case.
        Otherwise, raises an error for after treatment and generates no return.
        """
        if self.check_if_category(data[0]):
            return (data[0],data[1])
        else:
            raise Exception()

    def make_entry_import_export_pages(self,data:list,tipo_produto:str,ano:int)->dict:
        '''
        Make a new dict-formatted entry to be returned
        suitable for pages "Importação" and "Exportação"
        '''
        return {
            'País':data[0],
            'Quantidade(kg)':float(data[1]),
            'Valor(US$)':float(data[2]),
            'Tipo produto':tipo_produto,
            'Ano': ano
            }

    def make_entry_prod_processamento_comercializacao(self,data_new:list,categoria:str,tipo_produto:str,total:str,ano:int)->dict:
        '''
        Make a new dict-formatted entry to be returned
        suitable for pages "Produção", "Comercialização" e "Processamento".
        '''
        if self.check_if_tipo_produto_is_not_none(tipo_produto):
            new_entry = {
                'Produto':data_new[0],
                'Quantidade(L.)':float(data_new[1]),
                'Categoria':categoria,
                'Tipo produto': tipo_produto,
                'Total Categoria':float(total),
                'Ano': ano
            }
        else:
            new_entry = {
                'Produto':data_new[0],
                'Quantidade(L.)':float(data_new[1]),
                'Categoria':categoria,
                'Total Categoria':float(total),
                'Ano': ano
            }
        return new_entry

    def check_if_row_is_not_empty(self,data_new:list)->bool:
        '''
        Some entries from the table are empty (i.e., they are []).
        '''
        return data_new != []

    def convert_data_list_to_dict_import_export(self,data_new:list,tipo_produto:str,ano:int)->dict:
        '''
        This will create a suitable dict/json containing all the data
        scraped from pages importacao/exportacao for a given year.
        '''
        # Initialize the result variable
        result = {"data":[]}
        # Run through each row
        for index in range(0,len(data_new)):
            # Just check if not an empty table entry (i.e. [])
            if self.check_if_not_empty(data_new[index]):
                # If not empty, make a new entry and append
                new_entry = self.make_entry_import_export_pages(
                    data_new[index], tipo_produto, ano
                    )
                result['data'].append(new_entry)

        return result
    
    def convert_data_list_to_dict_prod_proc_comer(self,data_new:list,tipo_produto:str,ano:int)->dict:
        '''
        This will create a suitable dict/json containing all the data
        scraped from pages producao/processamento/comercializacao for a given year.
        '''
        # Initialize variables
        result = {"data":[]}
        categoria = None
        total = None
        # Run through each row
        for index in range(0,len(data_new)):
            # Just check if not an empty table entry (i.e. [])
            if self.check_if_not_empty(data_new[index]):
                # Try to update the category/total values.
                # This will only succeed if this row has categories (all UPPER)
                # Otherwise, it raises an exception and do nothing
                try:
                    (categoria, total) = self.update_category(data_new[index])
                except:
                    pass
                # If this is not a category, then it is data to be stored in the dict
                if not self.check_if_category(data_new[index][0]):
                    new_entry = self.make_entry_prod_processamento_comercializacao(data_new[index],categoria,tipo_produto,total,ano)
                    result['data'].append(new_entry)
                # There are a few exceptional cases where categories should be stored too
                elif self.check_if_category_is_in_exception_list(data_new[index][0]):
                    new_entry = self.make_entry_prod_processamento_comercializacao(data_new[index],categoria,tipo_produto,total,ano)
                    result['data'].append(new_entry)

        return result

    def get_export_import_page(self,url:str,tipo_produto:str,ano:int)->dict:
        '''
        Calls the full routines for scraping and data treatment (pages importacao/exportacao).
        '''
        data_new = self.html_to_list(url)
        return self.convert_data_list_to_dict_import_export(data_new,tipo_produto,ano)

    def get_production_commercialization_processing_page(self,url:str,tipo_produto:str,ano:int)->dict:
        '''
        Calls the full routines for scraping and data treatment (pages producao/processamento/comercializacao).
        '''
        data_new = self.html_to_list(url)
        return self.convert_data_list_to_dict_prod_proc_comer(data_new,tipo_produto,ano)
        

