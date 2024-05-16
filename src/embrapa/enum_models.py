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

