from groq import Groq   
from app.config import settings
from typing import List, Dict

class AIService:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def get_response(self, messages: List[Dict[str, str]], temperature: float = 0.7):
           
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
        )

            return response.choices[0].message.content
        
        except Exception as e:
            print(f'Erro ao chamar IA: {e}')
            raise Exception("Erro ao processar a resposta da IA: {str(e)}")
        
ai_service = AIService()
    
