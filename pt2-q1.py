from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Define o modelo de entrada
class ChatRequest(BaseModel):
    user_input: str  # Mensagem enviada pelo usuário

# Configura o FakeListLLM com respostas predefinidas
responses = [
    "Hello! How can I assist you today?",
    "I'm just a bot, but I'm functioning perfectly!",
    "I'm sorry, I don't understand your question.",
]
fake_llm = FakeListLLM(responses=responses)

# Define o template do prompt
prompt_template = PromptTemplate(input_variables=["user_input"], template="{user_input}")
chat_chain = LLMChain(llm=fake_llm, prompt=prompt_template)

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    """
    Simula uma conversa com o chatbot.
    """
    user_input = request.user_input
    response = chat_chain.run({"user_input": user_input})
    return {"user_input": user_input, "bot_response": response}

# Rota básica para teste
@app.get("/")
async def root():
    return {"message": "Chatbot com Fake LLM está ativo!"}