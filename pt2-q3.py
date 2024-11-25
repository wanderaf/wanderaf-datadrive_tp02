from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Define o modelo de entrada
class TranslationRequest(BaseModel):
    text: str  # Texto em inglês a ser traduzido

# Configura o pipeline HuggingFace para o modelo Helsinki-NLP
translator_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")

# Configura o LangChain com o pipeline HuggingFace
llm = HuggingFacePipeline(pipeline=translator_pipeline)

# Define o template do prompt para LangChain
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="Translate the following text to German:\n{text}"
)

# Cria a cadeia LLM com LangChain
translation_chain = LLMChain(llm=llm, prompt=prompt_template)

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Traduz o texto do inglês para o alemão.
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
    return {"message": "API de tradução com HuggingFace está ativa!"}
