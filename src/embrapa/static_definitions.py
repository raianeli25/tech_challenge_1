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

    # Those constants are the column names on the raw table
    # scraped from the website
    LIT_PRODUTO = "Produto"
    LIT_QUANTIDADE_L = "Quantidade (L.)"
    LIT_CULTIVAR = "Cultivar"
    LIT_QUANTIDADE_KG = "Quantidade (Kg)"
    LIT_SEM_DEF = "Sem definição"
    LIT_PAISES = "Países"
    LIT_VALOR = "Valor (US$)"

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

    # This dict is used to retrieve the correct table header
    # for each webpage, depending uniquely on the parameters
    # 'option' and 'suboption'
    TABLE_HEADERS = {
        "producao" : {
            None : [LIT_PRODUTO, LIT_QUANTIDADE_L]
        },
        "processamento" : {
            "viniferas" : [LIT_CULTIVAR, LIT_QUANTIDADE_KG],
            "americanas_e_hibridas" : [LIT_CULTIVAR, LIT_QUANTIDADE_KG],
            "uvas_de_mesa" : [LIT_CULTIVAR, LIT_QUANTIDADE_KG],
            "sem_classificacao" : [LIT_SEM_DEF, LIT_QUANTIDADE_KG]
        },
        "comercializacao" : {
            None : [LIT_PRODUTO, LIT_QUANTIDADE_L]
        },
        "importacao" : {
            "vinhos_de_mesa" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "espumantes" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "uvas_frescas" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "uvas_passas" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "suco_de_uva" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
        },
        "exportacao" : {
            "vinhos_de_mesa" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "espumantes" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "uvas_frescas" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "suco_de_uva" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
        }
    }