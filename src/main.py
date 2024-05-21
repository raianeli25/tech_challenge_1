from typing import Union, Annotated
from embrapa.web_scrapping import EmbrapaCollect
from embrapa.enum_models import ModelExport, ModelImport, ModelProcessing
from embrapa.static_definitions import EmbrapaConstants
from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auths.auth import User, get_current_active_user
from auths import route_token_post

app = FastAPI()

app.include_router(route_token_post.router)

root_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php'

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/")
async def home():
    return "Esta API retorna os dados de vitivinicultura do site da Embrapa, para mais informações acesse /docs"

@app.get("/export/{tipo_produto}/{ano}")
async def read_export_page(
            tipo_produto: ModelExport,
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):
    dict_subopcao = {'vinhos_de_mesa':'subopt_01',
                     'espumantes':'subopt_02',
                     'uvas_frescas':'subopt_03',
                     'suco_de_uva':'subopt_04'}
    
    sub_opcao = dict_subopcao[tipo_produto]
    url = f'{root_url}?ano={ano}&opcao=opt_06&subopcao={sub_opcao}'

    collect_data = EmbrapaCollect()

    return collect_data.get_export_import_page(url,tipo_produto,ano)

@app.get("/import/{tipo_produto}/{ano}")
async def read_import_page(
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
    url = f'{root_url}?ano={ano}&opcao=opt_05&subopcao={sub_opcao}'

    collect_data = EmbrapaCollect()

    return collect_data.get_export_import_page(url,tipo_produto,ano)

@app.get("/production/{ano}")
async def read_production_page(
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):

    url = f'{root_url}?ano={ano}&opcao=opt_02'
    categorias_production=['VINHO DE MESA','VINHO FINO DE MESA (VINIFERA)','SUCO','DERIVADOS']

    collect_data = EmbrapaCollect()

    return collect_data.get_production_commercialization_processing_page(url,None,ano)

@app.get("/commercialization/{ano}")
async def read_commercialization_page(
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):

    url = f'{root_url}?ano={ano}&opcao=opt_04'
    categorias_commercialization=['VINHO DE MESA','VINHO  FINO DE MESA','VINHO FRIZANTE','VINHO ORGÂNICO','VINHO ESPECIAL','ESPUMANTES','SUCO DE UVAS','SUCO DE UVAS CONCENTRADO','OUTROS PRODUTOS COMERCIALIZADOS']
    
    collect_data = EmbrapaCollect()

    return collect_data.get_production_commercialization_processing_page(url,None,ano)

@app.get("/processing/{tipo_produto}/{ano}")
async def read_processing_page(
            tipo_produto: ModelProcessing,
            ano: Annotated[int, Path(title="Ano da busca", ge=1970, le=2022)],
            token: str = Depends(get_current_active_user)
    ):

    dict_subopcao = {
        "viniferas":"subopt_01",
        "americanas_e_hibridas":"subopt_02",
        "uvas_de_mesa":"subopt_03",
        "sem_classificacao":"subopt_04"
        }
    
    sub_opcao = dict_subopcao[tipo_produto]

    url = f'{root_url}?ano={ano}&opcao=opt_03&subopcao={sub_opcao}'
    print(url)

    collect_data = EmbrapaCollect()

    return collect_data.get_production_commercialization_processing_page(url,tipo_produto,ano)