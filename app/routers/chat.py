from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.chat import (
    MessageSend,
    ChatResponse,
    ConversationResponse,
    ConversationWithMessages,  
)

from app.models.conversation import Conversation 
from app.services.chat_service import chat_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send", response_model=ChatResponse)
def send_message(
    message_data: MessageSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:
        result = chat_service.send_message(
            user=current_user,
            message_content=message_data.message,
            conversation_id=message_data.conversation_id,  # ← CORRIGIDO (id minúsculo)
            db=db
        )

        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )
    
@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    conversations = chat_service.get_user_conversations(
        user=current_user,
        db=db,
        skip=skip,
        limit=limit
    )
    return conversations

@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        messages = chat_service.get_conversation_messages(
            conversation_id=conversation_id,
            user=current_user,
            db=db
        )
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "messages": messages
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:
        chat_service.delete_conversation(
            conversation_id=conversation_id,
            user=current_user,
            db=db
        )
        return None
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )