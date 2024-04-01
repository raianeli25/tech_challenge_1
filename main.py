from typing import Union, Annotated
from web_scrapping import get_export_import_page, get_production_commercialization_page, get_processing_page
from classes import ModelExport, ModelImport, ModelProcessing, Token
from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import *

app = FastAPI()

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/export/{tipo_produto}/{ano}")
def read_export_page(
            tipo_produto: ModelExport,
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):
    dict_subopcao = {'vinhos_de_mesa':'subopt_01',
                     'espumantes':'subopt_02',
                     'uvas_frescas':'subopt_03',
                     'suco_de_uva':'subopt_04'}
    
    sub_opcao = dict_subopcao[tipo_produto]
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao={sub_opcao}'

    return get_export_import_page(url,tipo_produto,ano)

@app.get("/import/{tipo_produto}/{ano}")
def read_import_page(
            tipo_produto: ModelImport,
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):
    dict_subopcao = {'vinhos_de_mesa':'subopt_01',
                     'espumantes':'subopt_02',
                     'uvas_frescas':'subopt_03',
                     'uvas_passas':'subopt_04',
                     'suco_de_uva':'subopt_05'}
    
    sub_opcao = dict_subopcao[tipo_produto]
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao={sub_opcao}'

    return get_export_import_page(url,tipo_produto,ano)

@app.get("/production/{ano}")
def read_production_page(
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):

    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
    categorias_production=['VINHO DE MESA','VINHO FINO DE MESA (VINÍFERA)','SUCO','DERIVADOS']

    return get_production_commercialization_page(url,categorias_production,ano)

@app.get("/commercialization/{ano}")
def read_commercialization_page(
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):

    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04'
    categorias_commercialization=['VINHO DE MESA','VINHO  FINO DE MESA','VINHO FRIZANTE','VINHO ORGÂNICO','VINHO ESPECIAL','ESPUMANTES','SUCO DE UVAS','SUCO DE UVAS CONCENTRADO','OUTROS PRODUTOS COMERCIALIZADOS']
    
    return get_production_commercialization_page(url,categorias_commercialization,ano)

@app.get("/processing/{tipo_produto}/{ano}")
def read_processing_page(
            tipo_produto: ModelProcessing,
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):

    dict_subopcao = {
        "viniferas":["subopt_01",["TINTAS","BRANCAS E ROSADAS"]],
        "americanas_e_hibridas":["subopt_02",["TINTAS","BRANCAS E ROSADAS"]],
        "uvas_de_mesa":["subopt_03",["TINTAS","BRANCAS"]],
        "sem_classificacao":["subopt_04",["Sem classificação"]]
        }
    
    sub_opcao = dict_subopcao[tipo_produto][0]

    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao={sub_opcao}'
    categorias_processing=dict_subopcao[tipo_produto][1]
    print(url)
    return get_processing_page(url,categorias_processing,tipo_produto,ano)