import pytest

from .web_scrapping import EmbrapaCollect

@pytest.mark.parametrize("opt_arg, subopt_arg, ano_arg, expected_result", [
    ("producao", None, 2022 , "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_02"),
    ("processamento", "viniferas", 2020 , "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2020&subopcao=subopt_01&opcao=opt_03"),
    ("comercializacao", None, 1999 , "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1999&opcao=opt_04"),
    ("importacao", "espumantes", 1970 , "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1970&subopcao=subopt_02&opcao=opt_05"),
    ("exportacao", "suco_de_uva", 2001 , "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2001&subopcao=subopt_04&opcao=opt_06"),
])
def test_parsing_url(opt_arg:str,subopt_arg:str,ano_arg:int,expected_result:str):
    collect_data = EmbrapaCollect()
    url = collect_data.parsing_url(opt_arg,subopt_arg,ano_arg)
    assert url == expected_result

@pytest.mark.parametrize("url, row, col, expected_result", [
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2000&opcao=opt_02", 2, 0, "Tinto"),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_04", 4, 1, "20.658.933"), # Branco
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1970&subopcao=subopt_02&opcao=opt_03", 2, 0, "Bacarina"),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1999&subopcao=subopt_01&opcao=opt_05", 3, 1, "-"),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2001&subopcao=subopt_01&opcao=opt_06", 1, 2, "-"),
])
def test_extract_table_infos_into_list(url:str, row:int, col:int, expected_result:str):
    collect_data = EmbrapaCollect()
    table = collect_data.scrap_table_from_website(url)
    data = collect_data.extract_table_infos_into_list(table)

    assert expected_result in data[row][col]

def test_remove_row_total():
    URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2000&opcao=opt_02"
    collect_data = EmbrapaCollect()
    table = collect_data.scrap_table_from_website(URL)
    data = collect_data.extract_table_infos_into_list(table)
    data_new = collect_data.remove_total_row(data)

    assert "Outros derivados" in data_new[-1][0] and "Total" not in data_new[-1][0]

@pytest.mark.parametrize("url, str_to_check, expected_result", [
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2000&opcao=opt_02", "\n", False),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2000&opcao=opt_02", "-", False),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1999&opcao=opt_04", "Espumante", True),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1999&opcao=opt_04", "   Espumante ", False),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&subopcao=subopt_02&opcao=opt_03", "*", False),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&subopcao=subopt_01&opcao=opt_05", "64.795.326", False),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&subopcao=subopt_01&opcao=opt_05", "64795326", True),
])
def test_if_fields_are_corrected_formated(url:str, str_to_check:str, expected_result:bool):
    collect_data = EmbrapaCollect()
    data = collect_data.html_to_list(url)

    assert (any(str_to_check in subset for subset in data)) == expected_result


def test_check_if_category_is_true():
    TEST_VALUE_UPPER = "VINHO DE MESA"
    collect_data = EmbrapaCollect()
    true_category = collect_data.check_if_category(TEST_VALUE_UPPER)

    assert true_category == True

def test_check_if_category_is_false():
    TEST_VALUE_NOT_UPPER = "Tinto"
    collect_data = EmbrapaCollect()
    false_category = collect_data.check_if_category(TEST_VALUE_NOT_UPPER)

    assert false_category == False

def test_check_if_category_is_in_exception_list():
    VALUE_IN_EXCEPTION_LIST = "VINHO FRIZANTE"
    
    collect_data = EmbrapaCollect()
    
    collect_data.CATEGORY_EXCEPTION_LIST
    
    is_in_exception_list = collect_data.check_if_category_is_in_exception_list(VALUE_IN_EXCEPTION_LIST)

    assert (is_in_exception_list == True)

def test_check_if_category_is_not_in_exception_list():
    VALUE_NOT_IN_EXCEPTION_LIST = "Tinto"
    
    collect_data = EmbrapaCollect()
    
    collect_data.CATEGORY_EXCEPTION_LIST
    
    not_in_exception_list = collect_data.check_if_category_is_in_exception_list(VALUE_NOT_IN_EXCEPTION_LIST)

    assert (not_in_exception_list == False)


def test_update_category_when_is_category():
    URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_02"
    collect_data = EmbrapaCollect()
    data = collect_data.html_to_list(URL)

    (categoria, total) = collect_data.update_category(data[1])

    condition_is_category_ok = (categoria == "VINHO DE MESA") and (total == "195031611")

    try:
        (categoria, total) = collect_data.update_category(data[2])
        condition_is_not_category_ok = False
    except:
        condition_is_not_category_ok = True

    assert condition_is_category_ok and condition_is_not_category_ok


EXPECTED_OUT_IMPORTACAO = {
            'País': "Alemanha",
            'Quantidade(kg)':float("2576557"),
            'Valor(US$)':float("4539354"),
            'Tipo produto':"vinhos_de_mesa",
            'Ano': 1999
        }

EXPECTED_OUT_EXPORTACAO = {
            'País': "Argentina",
            'Quantidade(kg)':float("1477"),
            'Valor(US$)':float("2393"),
            'Tipo produto':"vinhos_de_mesa",
            'Ano': 2001
        }

@pytest.mark.parametrize("url, tipo_produto, ano, index, expected_result", [
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1999&subopcao=subopt_01&opcao=opt_05", "vinhos_de_mesa", 1999, 2, EXPECTED_OUT_IMPORTACAO), #Alemanha
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2001&subopcao=subopt_01&opcao=opt_06", "vinhos_de_mesa", 2001, 9, EXPECTED_OUT_EXPORTACAO), #Argentina
])
def test_make_entry_import_export_pages(url:str, tipo_produto:str, ano:int, index:int, expected_result:bool):
    collect_data = EmbrapaCollect()
    
    data = collect_data.html_to_list(url)
    out = collect_data.make_entry_import_export_pages(
                    data[index], tipo_produto, ano
                    )

    assert out == expected_result

EXPECTED_OUT_PRODUCAO = {
                'Produto':"Tinto",
                'Quantidade(L.)':float("162844214"),
                'Categoria': "VINHO DE MESA",
                'Total Categoria':float("195031611"),
                'Ano': 2022
            }
EXPECTED_OUT_PROCESSAMENTO = {
                'Produto':"Alicante Bouschet",
                'Quantidade(L.)':float("0"),
                'Categoria':"TINTAS",
                'Tipo produto': "viniferas",
                'Total Categoria':float("0"),
                'Ano': 2022
            }
EXPECTED_OUT_COMERCIALIZACAO = {
                'Produto':"Tinto",
                'Quantidade(L.)':float("165067340"),
                'Categoria': "VINHO DE MESA",
                'Total Categoria':float("187939996"),
                'Ano': 2022
            }

@pytest.mark.parametrize("url, tipo_produto, ano, index, expected_result", [
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_02", None, 2022, 2, EXPECTED_OUT_PRODUCAO),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_03&subopcao=subopt_01", "viniferas", 2022, 2, EXPECTED_OUT_PROCESSAMENTO),
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_04", None, 2022, 2, EXPECTED_OUT_COMERCIALIZACAO),
])
def test_make_entry_prod_processamento_comercializacao(url:str, tipo_produto:str, ano:int, index:int, expected_result:bool):
    collect_data = EmbrapaCollect()
    
    data = collect_data.html_to_list(url)
    (categoria, total) = collect_data.update_category(data[index-1])
    out = collect_data.make_entry_prod_processamento_comercializacao(
                    data[index],categoria,tipo_produto,total,ano
                    )

    assert out == expected_result

EXPECTED_JSON_OUT_PRODUCAO = {
			"Produto": "Tinto",
			"Quantidade(L.)": 15646861.0,
			"Categoria": "VINHO FINO DE MESA (VINIFERA)",
			"Total Categoria": 58733741.0,
			"Ano": 1994
		}

@pytest.mark.parametrize("url, tipo_produto, ano, index, expected_result", [
    ("http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1994&opcao=opt_02", None, 1994, 3, EXPECTED_JSON_OUT_PRODUCAO),
])
def test_get_production_commercialization_processing_page(url:str, tipo_produto:str, ano:int, index:int, expected_result:bool):
    collect_data = EmbrapaCollect()
    json = collect_data.get_production_commercialization_processing_page(url,tipo_produto,ano)
    entry = json['data'][index]

    assert entry == expected_result