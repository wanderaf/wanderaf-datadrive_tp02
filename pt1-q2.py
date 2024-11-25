from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Modelo de entrada (JSON)
class TranslationRequest(BaseModel):
    text: str  # Texto em inglês a ser traduzido

# Inicializa o pipeline HuggingFace para tradução
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Traduz um texto do inglês para o francês.
    """
    try:
        # Recupera o texto do corpo da requisição
        input_text = request.text

        # Traduz o texto
        translation = translator(input_text, max_length=400)
        translated_text = translation[0]["translation_text"]

        # Retorna o texto traduzido
        return {"input": input_text, "translated_text": translated_text}

    except Exception as e:
        # Tratamento de erros
        raise HTTPException(status_code=500, detail=f"Erro ao traduzir o texto: {str(e)}")

# Rota básica para teste
@app.get("/")
async def root():
    return {"message": "API de tradução Inglês-Francês está ativa!"}
