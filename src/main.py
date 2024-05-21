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
            ano: Annotated[int, Path(title="Ano da busca", ge=EmbrapaConstants.START_YEAR, le=EmbrapaConstants.LAST_YEAR)],
            token: str = Depends(get_current_active_user)
    ):

    collect_data = EmbrapaCollect()
    url = collect_data.parsing_url(opt_arg="exportacao",subopt_arg=tipo_produto,ano_arg=ano)

    return collect_data.get_export_import_page(url,tipo_produto,ano)

@app.get("/import/{tipo_produto}/{ano}")
async def read_import_page(
            tipo_produto: ModelImport,
            ano: Annotated[int, Path(title="Ano da busca", ge=EmbrapaConstants.START_YEAR, le=EmbrapaConstants.LAST_YEAR)],
            token: str = Depends(get_current_active_user)
    ):

    collect_data = EmbrapaCollect()
    url = collect_data.parsing_url(opt_arg="importacao",subopt_arg=tipo_produto,ano_arg=ano)

    return collect_data.get_export_import_page(url,tipo_produto,ano)

@app.get("/production/{ano}")
async def read_production_page(
            ano: Annotated[int, Path(title="Ano da busca", ge=EmbrapaConstants.START_YEAR, le=EmbrapaConstants.LAST_YEAR)],
            token: str = Depends(get_current_active_user)
    ):

    collect_data = EmbrapaCollect()
    url = collect_data.parsing_url(opt_arg="producao",subopt_arg=None,ano_arg=ano)

    return collect_data.get_production_commercialization_processing_page(url,None,ano)

@app.get("/commercialization/{ano}")
async def read_commercialization_page(
            ano: Annotated[int, Path(title="Ano da busca", ge=EmbrapaConstants.START_YEAR, le=EmbrapaConstants.LAST_YEAR)],
            token: str = Depends(get_current_active_user)
    ):

    collect_data = EmbrapaCollect()
    url = collect_data.parsing_url(opt_arg="comercializacao",subopt_arg=None,ano_arg=ano)

    return collect_data.get_production_commercialization_processing_page(url,None,ano)

@app.get("/processing/{tipo_produto}/{ano}")
async def read_processing_page(
            tipo_produto: ModelProcessing,
            ano: Annotated[int, Path(title="Ano da busca", ge=EmbrapaConstants.START_YEAR, le=EmbrapaConstants.LAST_YEAR)],
            token: str = Depends(get_current_active_user)
    ):

    collect_data = EmbrapaCollect()
    url = collect_data.parsing_url(opt_arg="processamento",subopt_arg=tipo_produto,ano_arg=ano)

    return collect_data.get_production_commercialization_processing_page(url,tipo_produto,ano)