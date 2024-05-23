## Tech Challenge #1 **🧩**

🎯 Esse projeto foi desenvolvido com o objetivo de resolver um desafio de pós gradução do curso de Engenharia de Machine Learning da FIAP.

A tarefa é criar uma API que retorne os dados de vitivinicultura da Embrapa, disponíveis [aqui](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).

A API consulta as seguintes abas:

- Produção
- Processamento
- Comercialização
- Importação
- Exportação

### **Exemplo API 📝**

Exemplo referente a uma das páginas, neste caso, Produção.

---

Dado o input:

- Ano = 2009

Temos HTTP request (GET): /production/2009

Trecho de resposta da API para esta chamada:

```sh
{
	"data": [
		{
			"Produto": "Tinto",
			"Quantidade(L.)": 164143454.0,
			"Categoria": "VINHO DE MESA",
			"Total Categoria": 205418206.0,
			"Ano": 2009
		},
		{
			"Produto": "Branco",
			"Quantidade(L.)": 39211278.0,
			"Categoria": "VINHO DE MESA",
			"Total Categoria": 205418206.0,
			"Ano": 2009
		},
		{
			"Produto": "Rosado",
			"Quantidade(L.)": 2063474.0,
			"Categoria": "VINHO DE MESA",
			"Total Categoria": 205418206.0,
			"Ano": 2009
		},
      ...
}
```

### **Tecnologias utilizadas 💡**

---

O projeto foi todo desenvolvido em python, foi utilizado o framework [FAST API](https://fastapi.tiangolo.com/) para a criação da API, essa escolha se deve ao fato deste framework ser amplamente utilizado no mercado e ter a facilidade de criação automática da documentação da API. Ainda, utilizamos a biblioteca [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) para a parte de web scrapping do projeto.

### Estrutura de pastas **📂**

---

```sh
.
├── Dockerfile
├── README.md
├── requirements.txt
└── src
    ├── auths
    │   ├── auth.py
    │   ├── fake_users_db.json
    │   ├── __init__.py
    │   └── route_token_post.py
    ├── embrapa
    │   ├── __init__.py
    │   ├── static_definitions.py
    │   ├── test_web_scrapping.py
    │   └── web_scrapping.py
    ├── main.py
    └── test_main.py
```

- **auth.py:** arquivo responsável por toda a parte de autenticação da API, aqui utilizamos JWT, como sugerido.
- **Dockerfile:** contém as definições do container (Docker).
- **fake_users_db.json:** arquivo que simula um database de usuários.
- **main.py:** arquivo principal, que contém todos os endpoints da API.
- **requirements.txt:** arquivo com todos os pacotes necessários para rodar este projeto.
- **route_token_post.py:** cria a rota necessária para expor a a parte de autenticacação à API.
- **static_definitions.py:** contém todas as definições estáticas utilizadas (e.g. constantes e enum_models).
- **test_main.py:** arquivo que contém todos os testes da API.
- **test_web_scrapping.py:** arquivo que contém testes para o módulo `web_scrapping.py`.
- **web_scrapping.py:** arquivo que contém todas as funções utilizadas na API.

### Início rápido 🚀

---

1. Abra o terminal dentro do diretório do projeto.
2. Instale as dependências do projeto, aqui o ideal é ter um ambiente virtual já criado.

   `pip install -r requirements.txt`
3. Rode o comando abaixo para subir o servidor

   `uvicorn main:app --reload`
4. Se tudo funcionar corretamente, receberá o retorno abaixo.

```
INFO:     Will watch for changes in these directories: ['/home/raiane/Documentos/Projetos/tech_challenge_1']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [35496] using WatchFiles
INFO:     Started server process [35498]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

5. Acesse a API pelo link mostrado na linha 2: http://127.0.0.1:8000 e leia a documentação da API em http://127.0.0.1:8000/docs para começar a usá-la.
6. Rode o comando abaixo no diretório raíz do projeto para executar os testes:

   `pytest`

**Obs.:** É necessário realizar a autenticação para consumir a API, utilize login _admin_ e senha _admin._ Esta aplicação foi testada nas versões de python 3.10 e 3.12.

Caso não tenha nenhuma das versões acima disponível e/ou prefira rodar em docker, criamos um Dockerfile para executar a aplicação. Execute os seguintes comandos na raíz do repositório para subir a aplicação:

`docker build -t fastapi/myapp:1.0 .`

`docker run -d -p 8000:8000 fastapi/myapp:1.0 `

**Obs.:** Após rodar o último comando aparecerá um código do tipo: 6d7f3f69d0820f9c720a729bb8c4b6303cac170fe03a747aa71cd8a26f2b6e7d, utilize as primeiras três letras para rodar o comando abaixo:

`docker logs 6d7`

Se tudo der certo, o retorno desse comando será igual ao passo 4 e a aplicação estará disponível localmente da mesma maneira.

Para executar os testes basta logar no docker através do comando abaixo, após isso rodar o comando do passo 6.

`docker exec -it <container_name> bash`
