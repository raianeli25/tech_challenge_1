from enum import Enum

class ModelExport(str, Enum):
    vinhos_de_mesa = "vinhos_de_mesa"
    espumantes = "espumantes"
    uvas_frescas = "uvas_frescas"
    suco_de_uva = "suco_de_uva"

class ModelImport(str, Enum):
    vinhos_de_mesa = "vinhos_de_mesa"
    espumantes = "espumantes"
    uvas_frescas = "uvas_frescas"
    suco_de_uva = "suco_de_uva"
    uvas_passas = 'uvas_passas'

class ModelProcessing(str, Enum):
    viniferas = "viniferas"
    americanas_e_hibridas = "americanas_e_hibridas"
    uvas_de_mesa = "uvas_de_mesa"
    sem_classificacao = "sem_classificacao"

class EmbrapaConstants():
    """
    This Class has some important constant definitions regarding
    Embrapa Website.
    """

    # This is the base URL, without query parameters
    URL_INDEX = "http://vitibrasil.cnpuv.embrapa.br/index.php?"

    # Those constants represent de query parameters
    REQ_YEAR = "ano="
    REQ_OPTION = "opcao=opt_"
    REQ_SUBOPTION = "subopcao=subopt_"

    # The range of admissible values for "year" on a page request
    START_YEAR = 1970
    LAST_YEAR = 2022

    # When Scraping the page, some NULL values are filled with 
    # either '-' or '*'. Such strings are replaced by whatever
    # value is entered on the following constant.
    VALUE_TO_REPLACE_NULL_CHAR = '0'

    # This dict is used to map the option names with
    # with the option parameters value.
    # Example: to request the page from "Produção" Data, we need the URL
    # "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    # which is composed by URL_INDEX+REQ_OPTION+OPTIONS_DICT[producao]
    OPTIONS_DICT = {
        "producao" : "02",
        "processamento" : "03",
        "comercializacao" : "04",
        "importacao" : "05",
        "exportacao" : "06"
    }

    # Same as for OPTIONS_DICT, but now for suboptions
    SUBOPTIONS_DICT = {
        "processamento" : {
            "viniferas" : "01",
            "americanas_e_hibridas" : "02",
            "uvas_de_mesa" : "03",
            "sem_classificacao" : "04"
        },
        "importacao" : {
            "vinhos_de_mesa" : "01",
            "espumantes" : "02",
            "uvas_frescas" : "03",
            "uvas_passas" : "04",
            "suco_de_uva" : "05"
        },
        "exportacao" : {
            "vinhos_de_mesa" : "01",
            "espumantes" : "02",
            "uvas_frescas" : "03",
            "suco_de_uva" : "04"
        }
    }

    CATEGORY_EXCEPTION_LIST = [
        "VINHO FRIZANTE", "VINHO ORGÂNICO", "SUCO DE UVAS CONCENTRADO"
    ]