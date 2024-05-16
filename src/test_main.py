from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#get token for test
response = client.post("/token", data={"username":"test","password":"test"})
token_test = response.json()

#test for get /
def test_get_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Esta API retorna os dados de vitivinicultura do site da Embrapa, para mais informações acesse /docs"

#tests for login

def test_login_for_access_token_successful():
    response = client.post("/token", data={"username":"test","password":"test"})
    assert response.status_code == 200  

def test_login_for_access_token_fail():
    response = client.post("/token", data={"username":"test","password":"123"})
    assert response.status_code == 401 

#test for read users

def test_read_users_me_successful():
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_users_me_fail():
    response = client.get("/users/me/", headers={"Authorization": f"Bearer aeiou"})
    assert response.status_code == 401 

#tests for export page

#range for years = 1970 - 2022
def test_read_export_page_when_year_in_range():
    response = client.get("/export/suco_de_uva/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_export_page_when_year_not_in_range():
    response = client.get("/export/suco_de_uva/2024", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

def test_read_export_page_when_product_type_exists():
    response = client.get("/export/suco_de_uva/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_export_page_when_product_type_not_exists():
    response = client.get("/export/qualquer_tipo/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

#tests for import page

#range for years = 1970 - 2022
def test_read_import_page_when_year_in_range():
    response = client.get("/import/suco_de_uva/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_import_page_when_year_not_in_range():
    response = client.get("/import/suco_de_uva/2024", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

def test_read_import_page_when_product_type_exists():
    response = client.get("/import/suco_de_uva/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_import_page_when_product_type_not_exists():
    response = client.get("/import/qualquer_tipo/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

#tests for production page

#range for years = 1970 - 2022
def test_read_production_page_when_year_in_range():
    response = client.get("/production/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_production_page_when_year_not_in_range():
    response = client.get("/production/2024", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

#tests for commercialization page

#range for years = 1970 - 2022
def test_read_commercialization_page_when_year_in_range():
    response = client.get("/commercialization/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_commercialization_page_when_year_not_in_range():
    response = client.get("/commercialization/2024", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

#tests for processing page

#range for years = 1970 - 2022
def test_read_import_page_when_year_in_range():
    response = client.get("/processing/viniferas/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_import_page_when_year_not_in_range():
    response = client.get("/processing/viniferas/2024", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422

def test_read_import_page_when_product_type_exists():
    response = client.get("/processing/viniferas/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 200  

def test_read_import_page_when_product_type_not_exists():
    response = client.get("/processing/qualquer_tipo/1994", headers={"Authorization": f"Bearer {token_test['access_token']}"})
    assert response.status_code == 422



