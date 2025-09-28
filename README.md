# FastAPI Chat + MongoDB Atlas

Este projeto é um sistema de chat minimalista utilizando FastAPI, MongoDB Atlas e WebSockets. Seguindo boas práticas de desenvolvimento.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar a aplicação localmente:

### 1. Configuração do MongoDB Atlas

1.  Crie um cluster gratuito no **MongoDB Atlas** (https://cloud.mongodb.com).
2.  Em **Database Access**, crie um usuário e senha para o banco de dados.
3.  Em **Network Access**, adicione seu endereço IP atual (ou `0.0.0.0/0` para permitir acesso de qualquer lugar, **apenas para testes**).
4.  Copie a **Connection String** (URI) do seu cluster. Certifique-se de selecionar o driver `Python` e a versão apropriada (geralmente `4.0 or later`). A string deve ser similar a `mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<AppName>`.

### 2. Configuração do Ambiente Local

1.  **Crie o arquivo `.env`**: Faça uma cópia do arquivo `.env.example` (se existir) ou crie um novo arquivo chamado `.env` na raiz do projeto.
2.  **Preencha o `.env`**: Cole sua Connection String do MongoDB Atlas no arquivo `.env` na variável `MONGO_URL`. Você também pode configurar `APP_HOST` e `APP_PORT` se desejar.

    Exemplo de `.env`:
    ```
    MONGO_URL="mongodb+srv://seu_usuario:sua_senha@seu_cluster.mongodb.net/?retryWrites=true&w=majority&appName=seu_app"
    APP_HOST="0.0.0.0"
    APP_PORT="8000"
    ```

### 3. Instalação e Execução

1.  **Crie e ative um ambiente virtual**:

    ```bash
    python -m venv .venv
    # .venv\Scripts\activate    # Windows
    ```

2.  **Instale as dependências**: Certifique-se de ter um arquivo `requirements.txt` com as dependências necessárias (fastapi, uvicorn, motor, python-dotenv, pydantic). Se não tiver, crie um com:

    ```bash
    pip install fastapi uvicorn motor python-dotenv pydantic
    pip freeze > requirements.txt
    ```
    Então, instale:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação**: Inicie o servidor FastAPI:

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    (Ou use `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` se `uvicorn` não estiver no PATH)

### 4. Acessando a Aplicação

Após iniciar o servidor, você pode acessar:

-   **Cliente Web Simples**: `http://localhost:8000`
-   **Documentação Interativa (Swagger UI)**: `http://localhost:8000/docs`
-   **Documentação Alternativa (ReDoc)**: `http://localhost:8000/redoc`

## 🔗 Endpoints Principais

-   **WebSocket**: `ws://localhost:8000/ws/{room}`
-   **Histórico REST**: `GET /rooms/{room}/messages?limit=20&before_id=...`
-   **Enviar Mensagem (REST)**: `POST /rooms/{room}/messages`

> **Observação**: A primeira conexão ou envio de mensagem para uma nova sala criará a coleção `messages` automaticamente no seu MongoDB Atlas.
