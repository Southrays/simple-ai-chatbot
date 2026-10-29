from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_layer.routes import chat, chat_with_user_level_memory

app = FastAPI(title="Simple AI Chatbot API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(chat.router)
app.include_router(chat_with_user_level_memory.router)


@app.get("/", tags=["health"])
def root():
    return {"message": "Simple AI Chatbot API is running."}
