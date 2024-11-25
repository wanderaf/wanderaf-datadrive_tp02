from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Configuração da API OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Define o modelo de entrada
class TranslationRequest(BaseModel):
    text: str  # Texto em inglês a ser traduzido

# Configura o modelo OpenAI via LangChain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define o template do prompt para tradução
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="Translate the following text to French:\n{text}"
)

# Cria a cadeia LLM com o modelo e o prompt
translation_chain = LLMChain(llm=llm, prompt=prompt_template)

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Traduz o texto do inglês para o francês.
    """
    input_text = request.text
    try:
        # Executa a tradução usando LangChain
        translated_text = translation_chain.run({"text": input_text})
        return {"input_text": input_text, "translated_text": translated_text}
    except Exception as e:
        return {"error": str(e)}

# Rota básica para teste
@app.get("/")
async def root():
    return {"message": "API de tradução com OpenAI está ativa!"}