from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, set_seed

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Define o modelo de entrada (JSON)
class InputText(BaseModel):
    prompt: str

# Inicializa o pipeline HuggingFace para GPT-2
generator = pipeline("text-generation", model="gpt2")
set_seed(42)  # Define uma seed para resultados consistentes

@app.post("/generate")
async def generate_text(input_text: InputText):
    """
    Gera um texto baseado na frase de entrada fornecida.
    """
    prompt = input_text.prompt
    
    try:
        # Geração de texto
        output = generator(prompt, max_length=50, num_return_sequences=1)
        generated_text = output[0]['generated_text']

        # Retorna a resposta formatada como JSON
        return {"input": prompt, "output": generated_text}

    except Exception as e:
        # Tratamento de erros
        raise HTTPException(status_code=500, detail=f"Erro ao gerar texto: {str(e)}")

# Rota básica para teste
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de geração de texto com GPT-2!"}