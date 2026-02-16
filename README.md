# 🤖 Chatbot AI API

API REST de chatbot conversacional com IA generativa (Llama 3.3) desenvolvida com FastAPI e arquitetura em camadas.

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![Groq](https://img.shields.io/badge/Groq-AI-orange)

---

## 📋 Sobre o Projeto

Chatbot inteligente que utiliza o modelo **Llama 3.3 70B** via Groq API para gerar respostas contextuais. A aplicação mantém histórico de conversas e permite múltiplas sessões por usuário.

### ✨ Funcionalidades

- 🤖 **Respostas com IA generativa** usando Llama 3.3
- 💬 **Histórico contextual** - A IA lembra das mensagens anteriores
- 📚 **Múltiplas conversas** por usuário
- 🔐 **Autenticação JWT** com sistema de permissões
- 🏗️ **Arquitetura em camadas** (Router → Service → AI Service)
- 📦 **Docker Compose** para orquestração completa
- 📖 **Documentação automática** (Swagger/OpenAPI)

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem principal
- **FastAPI** - Framework web moderno e performático
- **SQLAlchemy** - ORM para manipulação do banco
- **Pydantic** - Validação de dados

### Banco de Dados
- **PostgreSQL 15** - Banco relacional
- **Alembic** - Migrations (opcional)

### IA & Integrações
- **Groq API** - Acesso ao modelo Llama 3.3
- **Llama 3.3 70B Versatile** - Modelo de linguagem

### DevOps
- **Docker & Docker Compose** - Containerização
- **Uvicorn** - Servidor ASGI

### Segurança
- **JWT** - Autenticação via tokens
- **Bcrypt** - Hash de senhas

---

## 🏗️ Arquitetura
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ↓
┌─────────────────────┐
│   Router (chat.py)  │  ← Recebe requests HTTP
└──────┬──────────────┘
       │
       ↓
┌──────────────────────┐
│  Chat Service        │  ← Orquestra lógica de negócio
└──────┬───────────────┘
       │
       ├──→ [Database] ← Salva/busca conversas
       │
       └──→ [AI Service] ← Chama Groq API
              │
              └──→ [Groq/Llama 3.3] ← Gera resposta
```

### Camadas da Aplicação

1. **Router** - Endpoints da API
2. **Service** - Lógica de negócio
3. **AI Service** - Comunicação com IA
4. **Models** - Entidades do banco
5. **Schemas** - Validação com Pydantic

---

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Conta no [Groq](https://console.groq.com) (gratuita)
- Python 3.11+ (para execução local)

---

### 🐳 Execução com Docker (Recomendado)

#### 1. Clone o repositório
```bash
git clone https://github.com/AnthonyTavian/chatbot-ai-api.git
cd chatbot-ai-api
```

#### 2. Configure variáveis de ambiente

Crie um arquivo `.env` na raiz:
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/chatbot

# JWT
SECRET_KEY=sua-chave-secreta-super-segura-mude-isto
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq AI
GROQ_API_KEY=sua-groq-api-key-aqui

# App
APP_NAME=Chatbot AI API
APP_VERSION=1.0.0
```

**📌 Como obter a GROQ_API_KEY:**
1. Acesse [console.groq.com](https://console.groq.com)
2. Crie uma conta (gratuita)
3. Vá em "API Keys"
4. Crie uma nova chave
5. Cole no `.env`

#### 3. Suba os containers
```bash
docker-compose up -d
```

#### 4. Acesse a documentação
```
http://localhost:8000/docs
```

---

### 💻 Execução Local (sem Docker)

#### 1. Instale as dependências
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Configure PostgreSQL local
```bash
# Instale PostgreSQL ou use Docker só pro banco:
docker run -d \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=chatbot \
  -p 5432:5432 \
  postgres:15-alpine
```

#### 3. Configure `.env`
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/chatbot
SECRET_KEY=sua-chave-secreta
GROQ_API_KEY=sua-groq-api-key
```

#### 4. Execute
```bash
uvicorn app.main:app --reload
```

---

## 📚 Documentação da API

### Autenticação

#### Registrar usuário
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "full_name": "Nome Completo",
  "password": "senha123"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Ver perfil
```http
GET /auth/me
Authorization: Bearer {token}
```

---

### Chat

#### Enviar mensagem
```http
POST /chat/send
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "Olá! Qual é o seu nome?",
  "conversation_id": null
}
```

**Primeira mensagem:** Deixe `conversation_id` como `null` (cria nova conversa)

**Continuar conversa:** Use o `conversation_id` retornado

**Resposta:**
```json
{
  "conversation_id": 1,
  "user_message": "Olá! Qual é o seu nome?",
  "ai_response": "Olá! Eu sou um modelo de linguagem..."
}
```

#### Listar conversas
```http
GET /chat/conversations?skip=0&limit=20
Authorization: Bearer {token}
```

#### Ver conversa completa
```http
GET /chat/conversations/{conversation_id}
Authorization: Bearer {token}
```

#### Deletar conversa
```http
DELETE /chat/conversations/{conversation_id}
Authorization: Bearer {token}
```

---

## 🗂️ Estrutura do Projeto
```
chatbot-ai-api/
├── app/
│   ├── models/           # Entidades do banco (SQLAlchemy)
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── schemas/          # Validação de dados (Pydantic)
│   │   ├── user.py
│   │   └── chat.py
│   ├── routers/          # Endpoints da API
│   │   ├── auth.py
│   │   └── chat.py
│   ├── services/         # Lógica de negócio
│   │   ├── ai_service.py
│   │   └── chat_service.py
│   ├── utils/            # Funções auxiliares
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── config.py         # Configurações
│   ├── database.py       # Conexão com banco
│   └── main.py           # Aplicação principal
├── docker-compose.yml    # Orquestração Docker
├── Dockerfile            # Imagem da API
├── requirements.txt      # Dependências Python
└── README.md
```

---

## 🧪 Testando a API

### 1. Crie um usuário
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@teste.com",
    "full_name": "Teste User",
    "password": "123456"
  }'
```

### 2. Faça login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@teste.com",
    "password": "123456"
  }'
```

### 3. Envie mensagem para IA
```bash
curl -X POST http://localhost:8000/chat/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "message": "Explique o que é FastAPI em 3 linhas"
  }'
```

---

## 🎯 Próximas Melhorias

- [ ] Testes automatizados (Pytest)
- [ ] CI/CD com GitHub Actions
- [ ] Deploy em produção (Railway/Render)
- [ ] Rate limiting por usuário
- [ ] Streaming de respostas (WebSockets)
- [ ] Upload de arquivos para contexto
- [ ] Múltiplos modelos de IA
- [ ] Sistema de feedback de respostas

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Anthony Tavian de Castro Alves**

- GitHub: [@AnthonyTavian](https://github.com/AnthonyTavian)
- LinkedIn: [Anthony Tavian](https://www.linkedin.com/in/anthonytavian/)

---

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!