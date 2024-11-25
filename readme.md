API para tradução com FastAPI
1. Projeto que implementa traduções utilizando FastAPI com modelos da OpenAI e HuggingFace
2. Requisitos Python 3.8 ou superior
3. Instalar bibliotecas necessarias utilizando pip install -r requirementes.txt
4. Configurar arquivo .env com chave da API da OpenAI
5. Iniviar execução do servidor com uvicorn app:app --reload
6. Testar endpoint em http://127.0.0.1:8000
7. Enviar requisições POST conforme exemplo http POST http://127.0.0.1:8000/translate text="Hello, world!"