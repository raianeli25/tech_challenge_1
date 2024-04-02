## Tech Challenge #1 **🧩**

🎯 Esse projeto foi desenvolvido com o objetivo de resolver um desafio de pós gradução do curso de Engenharia de Machine Learning da FIAP.

A tarefa é criar uma API que retorne os dados de vitivinicultura da Embrapa, disponíveis [aqui](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).

A API consulta as seguintes abas:

* Produção
* Processamento
* Comercialização
* Importação
* Exportação

### **Tecnologias utilizadas 💡**

---

O projeto foi todo desenvolvido em python, foi utilizado o framework [FAST API](https://fastapi.tiangolo.com/) para a criação da API, essa escolha se deve ao fato deste framework ser amplamente utilizado no mercado e ter a facilidade de criação automática da documentação da API. Ainda, utilizamos a biblioteca [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) para a parte de web scrapping do projeto.


### Estrutura de pastas **📂**

---

```
.
└── tech_challenge_1/
    ├── auth.py
    ├── classes.py
    ├── main.py
    ├── requirements.txt
    └── web_scrapping.py
```

* **auth.py:** arquivo responsável por toda a parte de autenticação da API, aqui utilizamos JWT, como sugerido.
* **classes.py:** todas as classes que foram definidas neste projeto estão concentradas neste arquivo.
* **main.py:** arquivo principal, que contém todos os endpoints da API.
* **requirements.txt:** arquivo com todos os pacotes necessários para rodar este projeto.
* **web_scrapping.py:** arquivo que contém todas as funções utilizadas na API.

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

**Obs.:** É necessário realizar a autenticação para consumir a API, utilize login *admin* e senha *admin.* Esta aplicação foi testada nas versões de python 3.9 e 3.10.
