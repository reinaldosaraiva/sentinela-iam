# Documentação de Implementação - Sentinela IAM

**Data:** 12 de Novembro de 2025
**Versão:** 1.0.0

## Índice
- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Configuração e Execução](#configuração-e-execução)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Visão Geral

**Sentinela** é uma plataforma completa de Identity and Access Management (IAM) desenvolvida com arquitetura moderna, separando backend (FastAPI) e frontend (Next.js 14).

### Objetivos do Projeto
- Gerenciamento centralizado de aplicações, recursos e ações
- Controle de acesso baseado em políticas (Policy-Based Access Control)
- Interface moderna e responsiva para administração
- API RESTful completa e documentada
- Autenticação JWT segura

---

## Arquitetura

### Backend (Policy API)
```
FastAPI + PostgreSQL + SQLAlchemy
├── Autenticação JWT
├── CORS configurado
├── ORM com SQLAlchemy
└── Documentação automática (Swagger/OpenAPI)
```

### Frontend (Sentinela UI)
```
Next.js 14 (App Router) + TypeScript + TailwindCSS
├── Componentes React modernos
├── Autenticação com Context API
├── Cliente HTTP centralizado (apiClient)
└── Rotas protegidas
```

---

## Funcionalidades Implementadas

### 1. Autenticação e Autorização
- [x] **Sistema de Login JWT**
  - Endpoint: `POST /api/v1/auth/login`
  - Token JWT com expiração configurável
  - Refresh token support
  - Logout seguro

- [x] **Proteção de Rotas**
  - Componente `ProtectedRoute` no frontend
  - Middleware de autenticação no backend
  - Verificação automática de token
  - Redirecionamento para login quando não autenticado

- [x] **Gerenciamento de Sessão**
  - AuthContext global no frontend
  - Persistência de token em memória
  - Auto-logout em caso de token inválido

### 2. Gerenciamento de Aplicações
- [x] **CRUD Completo de Aplicações**
  - Listagem paginada com filtros
  - Criação de novas aplicações
  - Edição de aplicações existentes
  - Exclusão de aplicações
  - Upload de logo (URL)

- [x] **Campos de Aplicação**
  - Nome e Slug únicos
  - Descrição
  - Logo URL
  - Website URL
  - Status (active/inactive/paused)
  - Ambiente (production/staging/development)
  - Timestamps automáticos

- [x] **Interface de Aplicações**
  - Grid view responsivo
  - Busca em tempo real
  - Filtros por status e ambiente
  - Cards com preview visual
  - Estatísticas por aplicação

### 3. Gerenciamento de Recursos
- [x] **CRUD Completo de Recursos**
  - Listagem com contagem de ações associadas
  - Criação vinculada a aplicações
  - Edição de recursos
  - Exclusão em cascata (remove ações associadas)

- [x] **Campos de Recurso**
  - Nome e tipo do recurso
  - Descrição opcional
  - Vinculação com aplicação
  - Status ativo/inativo
  - Contagem de ações

- [x] **Interface de Recursos**
  - Lista expandível mostrando ações
  - Validação de tipos (lowercase, hyphens)
  - Dropdown de aplicações
  - Preview de ações inline

### 4. Gerenciamento de Ações
- [x] **CRUD Completo de Ações**
  - Listagem com informações do recurso
  - Criação vinculada a recursos
  - Toggle ativo/inativo
  - Exclusão de ações

- [x] **Campos de Ação**
  - Tipo de ação (read, write, update, delete, etc.)
  - Nome descritivo
  - Descrição opcional
  - Status ativo/inativo
  - Vinculação com recurso

- [x] **Interface de Ações**
  - Grid view com cards coloridos por tipo
  - Filtros por recurso e status
  - Busca multi-campo
  - Badges de status visual
  - Link para recurso associado

### 5. Dashboard Administrativo
- [x] **Dashboard Principal**
  - Estatísticas em tempo real
  - Cards com métricas principais
  - Gráficos de distribuição
  - Navegação rápida

- [x] **Layout Responsivo**
  - Sidebar com navegação
  - Header com perfil do usuário
  - Suporte mobile completo
  - Dark mode ready (estrutura preparada)

### 6. API Backend

#### Endpoints de Autenticação
```
POST   /api/v1/auth/login       - Autenticar usuário
GET    /api/v1/auth/me          - Dados do usuário atual
POST   /api/v1/auth/logout      - Logout
```

#### Endpoints de Aplicações
```
GET    /api/v1/applications/           - Listar aplicações
POST   /api/v1/applications/           - Criar aplicação
GET    /api/v1/applications/{id}       - Detalhes da aplicação
PUT    /api/v1/applications/{id}       - Atualizar aplicação
DELETE /api/v1/applications/{id}       - Deletar aplicação
```

#### Endpoints de Recursos
```
GET    /api/v1/resources/              - Listar recursos
POST   /api/v1/resources/              - Criar recurso
GET    /api/v1/resources/{id}          - Detalhes do recurso
PUT    /api/v1/resources/{id}          - Atualizar recurso
DELETE /api/v1/resources/{id}          - Deletar recurso (cascata)
```

#### Endpoints de Ações
```
GET    /api/v1/actions/                - Listar ações
POST   /api/v1/actions/                - Criar ação
GET    /api/v1/actions/{id}            - Detalhes da ação
PUT    /api/v1/actions/{id}            - Atualizar ação
DELETE /api/v1/actions/{id}            - Deletar ação
PATCH  /api/v1/actions/{id}/activate   - Ativar ação
PATCH  /api/v1/actions/{id}/deactivate - Desativar ação
```

### 7. Database e Models

#### Schema do Banco de Dados
- **Applications**: Aplicações registradas no sistema
- **Resources**: Recursos gerenciados por aplicação
- **Actions**: Ações disponíveis por recurso
- **Users**: Usuários do sistema
- **API Keys**: Chaves de API para aplicações

#### Relacionamentos
```
Application 1 ──→ N Resources
Resource    1 ──→ N Actions
Application 1 ──→ N API Keys
```

### 8. Ferramentas de Desenvolvimento

- [x] **Seed Data Script**
  - Script Python para popular banco com dados de exemplo
  - 5 aplicações de demonstração
  - 9 recursos distribuídos
  - ~50 ações com tipos variados
  - 3 API Keys de exemplo
  - Execução: `python seed_data.py`

- [x] **Documentação Automática**
  - Swagger UI em `/docs`
  - ReDoc em `/redoc`
  - Schemas OpenAPI 3.0
  - Exemplos de requisições

---

## Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.11+ | Linguagem principal |
| FastAPI | 0.104+ | Framework web |
| PostgreSQL | 14+ | Banco de dados |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.12+ | Migrações |
| Pydantic | 2.0+ | Validação de dados |
| python-jose | 3.3+ | JWT tokens |
| passlib | 1.7+ | Hash de senhas |
| uvicorn | 0.24+ | ASGI server |

### Frontend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Next.js | 14.0.0 | Framework React |
| React | 18.2+ | Biblioteca UI |
| TypeScript | 5.0+ | Tipagem estática |
| TailwindCSS | 3.3+ | Estilização |
| Lucide React | 0.292+ | Ícones |

---

## Configuração e Execução

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup

1. **Criar ambiente virtual:**
```bash
cd policy_api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente:**
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost/sentinela
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Executar migrações:**
```bash
alembic upgrade head
```

5. **Popular banco com dados de exemplo:**
```bash
python seed_data.py
```

6. **Iniciar servidor:**
```bash
python -m uvicorn policy_api.src.main:app --port 8001 --reload
```

### Frontend Setup

1. **Instalar dependências:**
```bash
cd sentinela-ui
npm install
```

2. **Iniciar servidor de desenvolvimento:**
```bash
PORT=3030 npm run dev
```

3. **Acessar aplicação:**
- Frontend: http://localhost:3030
- Backend API: http://localhost:8001
- Swagger Docs: http://localhost:8001/docs

### Credenciais Padrão
```
Email: admin@sentinela.com
Senha: admin123
```

---

## Estrutura do Projeto

```
sentinela/
├── policy_api/                 # Backend FastAPI
│   ├── src/
│   │   ├── routers/           # Endpoints da API
│   │   │   ├── auth.py
│   │   │   ├── applications.py
│   │   │   ├── resources.py
│   │   │   └── actions.py
│   │   ├── models/            # Modelos SQLAlchemy
│   │   │   ├── application.py
│   │   │   ├── resource.py
│   │   │   ├── action.py
│   │   │   └── user.py
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── database_pg.py     # Configuração DB
│   │   └── main.py            # App principal
│   ├── alembic/               # Migrações
│   ├── seed_data.py           # Script de seed
│   └── requirements.txt
│
├── sentinela-ui/              # Frontend Next.js
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   │   ├── login/
│   │   │   ├── applications/
│   │   │   ├── resources/
│   │   │   ├── actions/
│   │   │   └── dashboard/
│   │   ├── components/        # Componentes React
│   │   │   ├── DashboardLayout.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── contexts/          # React Contexts
│   │   │   └── AuthContext.tsx
│   │   └── lib/               # Utilidades
│   │       ├── api.ts         # Cliente HTTP
│   │       └── auth.ts        # Serviços de auth
│   ├── public/
│   └── package.json
│
├── IMPLEMENTATION.md          # Este arquivo
├── ROADMAP.md                 # Próximos passos
└── README.md                  # Documentação principal
```

---

## Destaques Técnicos

### 1. Autenticação JWT Segura
- Tokens assinados com HS256
- Expiração configurável
- Validação em todas as rotas protegidas
- Logout com invalidação de token

### 2. CORS Configurado
- Permite comunicação entre frontend (porta 3030) e backend (porta 8001)
- Suporte para credenciais
- Headers customizados permitidos

### 3. Cliente HTTP Centralizado
- `apiClient` com injeção automática de token
- Tratamento centralizado de erros
- Logging de requisições
- Retry logic preparado

### 4. Validação de Dados
- Pydantic schemas no backend
- TypeScript interfaces no frontend
- Validação em tempo real nos formulários
- Mensagens de erro amigáveis

### 5. Database com Relacionamentos
- Foreign keys com CASCADE
- Índices para performance
- Timestamps automáticos
- Soft delete preparado

---

## Problemas Resolvidos

### 1. CORS Authentication Blocking
**Problema:** Frontend não conseguia autenticar devido a CORS
**Solução:** Adicionado `http://localhost:3030` aos allowed origins

### 2. AuthContext Not Updating
**Problema:** Login page não atualizava contexto React
**Solução:** Migrado de `authService.login()` para `AuthContext.login()`

### 3. Unauthenticated API Calls
**Problema:** Resources/Actions pages usando fetch() sem autenticação
**Solução:** Migrado todos endpoints para usar `apiClient` centralizado

### 4. Next.js Cache Corruption
**Problema:** Erros de compilação falsos devido a cache corrompido
**Solução:** Clear de `.next/` folder e rebuild completo

---

## Métricas do Projeto

- **Linhas de Código (Backend):** ~2,500
- **Linhas de Código (Frontend):** ~3,500
- **Endpoints de API:** 18
- **Componentes React:** 12
- **Modelos de Dados:** 5
- **Tempo de Desenvolvimento:** 1 dia intensivo

---

## Próximos Passos

Consulte [ROADMAP.md](./ROADMAP.md) para funcionalidades planejadas e melhorias futuras.

---

**Desenvolvido com ❤️ usando FastAPI + Next.js**
