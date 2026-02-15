from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.models import User, Conversation, Message  
from app.routers import auth, chat  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API de Chatbot com IA Generativa"
)

app.include_router(auth.router)
app.include_router(chat.router)  

@app.get("/")
def read_root():
    return {
        "message": "Chatbot AI API está rodando!",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}