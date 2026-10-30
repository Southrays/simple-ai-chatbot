from contextlib import asynccontextmanager
from pathlib import Path

from ai_layer.prompts.prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from api_layer.routes import chat_with_database

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
CHECKPOINT_DB_PATH = BASE_DIR / "database" / "checkpoints.sqlite"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSqliteSaver.from_conn_string(
        str(CHECKPOINT_DB_PATH)
    ) as checkpointer:

        await checkpointer.setup()

        agent = create_agent(
            model="gpt-4o",
            tools=[],
            system_prompt=SYSTEM_PROMPT,
            checkpointer=checkpointer,
        )

        app.state.agent = agent

        yield

app = FastAPI(title="Simple AI Chatbot API", version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(chat_with_database.router)


@app.get("/", tags=["health"])
def root():
    return {"message": "Simple AI Chatbot API is running."}
