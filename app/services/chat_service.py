from sqlalchemy.orm import Session
from typing import List, Dict
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.services.ai_service import ai_service
from datetime import datetime

class ChatService:
    """
    Serviço de chat que orquestra toda a lógica de conversa.
    """
    
    def send_message(
        self, 
        user: User, 
        message_content: str, 
        conversation_id: int = None, 
        db: Session = None
    ) -> Dict:
        """Processa mensagem do usuário e retorna resposta da IA."""
        
        if conversation_id:
            conversation = self._get_user_conversation(conversation_id, user, db)
        else:
            conversation = self._create_conversation(user, db)
        
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=message_content
        )
        db.add(user_message)
        db.commit()
        
        history = self._get_conversation_history(conversation, db, limit=10)
        
        ai_response_text = ai_service.get_response(history)
        
        assistant_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=ai_response_text
        )
        db.add(assistant_message)
        
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "conversation_id": conversation.id,
            "user_message": message_content,  
            "ai_response": ai_response_text
        }
    
    def get_user_conversations(
        self,
        user: User,
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> List[Conversation]:
        """Lista conversas do usuário (mais recentes primeiro)."""
        return db.query(Conversation).filter(
            Conversation.user_id == user.id 
        ).order_by(
            Conversation.updated_at.desc()
        ).offset(skip).limit(limit).all()  
    
    def get_conversation_messages(
        self,
        conversation_id: int, 
        user: User,
        db: Session
    ) -> List[Message]:
        """Busca mensagens de uma conversa."""
        conversation = self._get_user_conversation(conversation_id, user, db)
        
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(
            Message.created_at.asc()  
        ).all()
    
    def delete_conversation(
        self,
        conversation_id: int,  
        user: User,
        db: Session
    ) -> bool:
        """Deleta uma conversa."""
        conversation = self._get_user_conversation(conversation_id, user, db)
        
        db.delete(conversation)
        db.commit()
        return True
    
    def _get_user_conversation(
        self,
        conversation_id: int,
        user: User,
        db: Session
    ) -> Conversation:
        """
        Busca conversa que pertence ao usuário.
        Levanta ValueError se não encontrar.
        """
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id
        ).first()
        
        if not conversation:
            raise ValueError("Conversa não encontrada ou não pertence ao usuário")
        
        return conversation
    
    def _create_conversation(self, user: User, db: Session) -> Conversation:
        """Cria nova conversa."""
        conversation = Conversation(
            user_id=user.id,
            title="Nova Conversa"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    def _get_conversation_history(
        self,
        conversation: Conversation,
        db: Session,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Busca histórico e formata para IA.
        Retorna últimas N mensagens em ordem cronológica.
        """
        messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(
            Message.created_at.desc()
        ).limit(limit).all()
        
        messages = list(reversed(messages))
        
        history = []
        for msg in messages:
            history.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        return history

chat_service = ChatService()