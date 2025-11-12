# Sentinela - Identity and Access Management Platform

<div align="center">

![Sentinela Logo](https://via.placeholder.com/150x150/4F46E5/FFFFFF?text=Sentinela)

**Plataforma moderna de gerenciamento de identidade e controle de acesso**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-000000?style=flat&logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192?style=flat&logo=postgresql)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Funcionalidades](#funcionalidades) •
[Demo](#demo) •
[Instalação](#instalação) •
[Documentação](#documentação) •
[Contribuir](#contribuir)

</div>

---

## Sobre o Projeto

**Sentinela** é uma plataforma completa de IAM (Identity and Access Management) desenvolvida com tecnologias modernas, oferecendo gerenciamento centralizado de aplicações, recursos e permissões de acesso.

### Por que Sentinela?

- 🔐 **Segurança em Primeiro Lugar**: Autenticação JWT robusta e criptografia de senhas
- 🚀 **Performance**: Backend assíncrono com FastAPI e frontend otimizado com Next.js 14
- 📱 **Responsivo**: Interface moderna que funciona em todos os dispositivos
- 🔧 **Extensível**: Arquitetura modular e APIs RESTful bem documentadas
- 🎯 **Fácil de Usar**: Interface intuitiva para gerenciamento de permissões

---

## Funcionalidades

### Gerenciamento de Aplicações
- ✅ Cadastro completo de aplicações
- ✅ Controle de ambientes (production, staging, development)
- ✅ Upload de logos e informações visuais
- ✅ Gestão de status (ativo, pausado, inativo)
- ✅ Busca e filtros avançados

### Gerenciamento de Recursos
- ✅ Definição de recursos por aplicação
- ✅ Tipagem customizada de recursos
- ✅ Vinculação com múltiplas ações
- ✅ Contadores de ações em tempo real
- ✅ Exclusão em cascata segura

### Gerenciamento de Ações
- ✅ CRUD completo de ações
- ✅ Tipos predefinidos (read, write, update, delete, etc.)
- ✅ Ativação/desativação dinâmica
- ✅ Filtros por recurso e status
- ✅ Visualização em grid colorido

### Autenticação e Segurança
- ✅ Login com JWT tokens
- ✅ Refresh token automático
- ✅ Proteção de rotas no frontend
- ✅ Middleware de autenticação no backend
- ✅ Hash de senhas com bcrypt
- ✅ CORS configurado

### Interface Administrativa
- ✅ Dashboard com métricas em tempo real
- ✅ Layout responsivo e moderno
- ✅ Navegação intuitiva com sidebar
- ✅ Temas visuais (preparado para dark mode)
- ✅ Componentes reutilizáveis

### API RESTful
- ✅ 18 endpoints documentados
- ✅ Swagger UI integrado
- ✅ Paginação automática
- ✅ Validação de dados com Pydantic
- ✅ Tratamento de erros padronizado

---

## Tecnologias

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional robusto
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM Python poderoso
- **[Alembic](https://alembic.sqlalchemy.org/)** - Gerenciamento de migrações
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validação de dados
- **[python-jose](https://github.com/mpdavis/python-jose)** - JWT tokens
- **[passlib](https://passlib.readthedocs.io/)** - Hash de senhas

### Frontend
- **[Next.js 14](https://nextjs.org/)** - Framework React com App Router
- **[TypeScript](https://www.typescriptlang.org/)** - Tipagem estática
- **[TailwindCSS](https://tailwindcss.com/)** - Framework CSS utilitário
- **[Lucide React](https://lucide.dev/)** - Biblioteca de ícones moderna
- **[React Context API](https://react.dev/reference/react/useContext)** - Gerenciamento de estado

---

## Instalação

### Pré-requisitos

- **Python** 3.11 ou superior
- **Node.js** 18 ou superior
- **PostgreSQL** 14 ou superior
- **Git**

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/sentinela.git
cd sentinela
```

### 2. Configure o Backend

```bash
# Entre na pasta do backend
cd policy_api

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Execute as migrações
alembic upgrade head

# (Opcional) Popule o banco com dados de exemplo
python seed_data.py

# Inicie o servidor
python -m uvicorn policy_api.src.main:app --port 8001 --reload
```

### 3. Configure o Frontend

```bash
# Em outro terminal, entre na pasta do frontend
cd sentinela-ui

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
PORT=3030 npm run dev
```

### 4. Acesse a Aplicação

- **Frontend**: http://localhost:3030
- **Backend API**: http://localhost:8001
- **Swagger Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Credenciais de Demonstração
```
Email: admin@sentinela.com
Senha: admin123
```

---

## Documentação

### Estrutura do Projeto

```
sentinela/
├── policy_api/                 # Backend FastAPI
│   ├── src/
│   │   ├── routers/           # Endpoints da API
│   │   ├── models/            # Modelos do banco de dados
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── database_pg.py     # Configuração do banco
│   │   └── main.py            # Aplicação principal
│   ├── alembic/               # Migrações do banco
│   ├── seed_data.py           # Script de seed
│   └── requirements.txt       # Dependências Python
│
├── sentinela-ui/              # Frontend Next.js
│   ├── src/
│   │   ├── app/               # Páginas (App Router)
│   │   ├── components/        # Componentes React
│   │   ├── contexts/          # React Contexts
│   │   └── lib/               # Utilitários
│   ├── public/                # Arquivos estáticos
│   └── package.json           # Dependências Node
│
├── docs/                      # Documentação adicional
├── IMPLEMENTATION.md          # Documentação de implementação
├── ROADMAP.md                 # Próximos passos
└── README.md                  # Este arquivo
```

### Documentação Detalhada

- **[Implementação Completa](./IMPLEMENTATION.md)** - Detalhes técnicos e arquitetura
- **[Roadmap](./ROADMAP.md)** - Funcionalidades futuras e melhorias planejadas
- **[API Reference](http://localhost:8001/docs)** - Documentação interativa da API

---

## API Endpoints

### Autenticação
```
POST   /api/v1/auth/login       - Login de usuário
GET    /api/v1/auth/me          - Dados do usuário atual
POST   /api/v1/auth/logout      - Logout
```

### Aplicações
```
GET    /api/v1/applications/           - Listar aplicações
POST   /api/v1/applications/           - Criar aplicação
GET    /api/v1/applications/{id}       - Detalhes da aplicação
PUT    /api/v1/applications/{id}       - Atualizar aplicação
DELETE /api/v1/applications/{id}       - Deletar aplicação
```

### Recursos
```
GET    /api/v1/resources/              - Listar recursos
POST   /api/v1/resources/              - Criar recurso
GET    /api/v1/resources/{id}          - Detalhes do recurso
PUT    /api/v1/resources/{id}          - Atualizar recurso
DELETE /api/v1/resources/{id}          - Deletar recurso
```

### Ações
```
GET    /api/v1/actions/                - Listar ações
POST   /api/v1/actions/                - Criar ação
GET    /api/v1/actions/{id}            - Detalhes da ação
PUT    /api/v1/actions/{id}            - Atualizar ação
DELETE /api/v1/actions/{id}            - Deletar ação
PATCH  /api/v1/actions/{id}/activate   - Ativar ação
PATCH  /api/v1/actions/{id}/deactivate - Desativar ação
```

---

## Contribuir

Contribuições são sempre bem-vindas! Siga os passos abaixo:

1. **Fork o projeto**
2. **Crie uma branch para sua feature** (`git checkout -b feature/MinhaFeature`)
3. **Commit suas mudanças** (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push para a branch** (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request**

### Guia de Contribuição

- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Certifique-se de que todos os testes passam
- Escreva mensagens de commit claras e descritivas

---

## Roadmap

Consulte [ROADMAP.md](./ROADMAP.md) para ver as funcionalidades planejadas e melhorias futuras.

### Próximas Funcionalidades (v2.0)

- [ ] Gerenciamento de Usuários e Grupos
- [ ] Sistema de Políticas (RBAC/ABAC)
- [ ] Auditoria e Logs de Atividades
- [ ] Notificações em Tempo Real
- [ ] Dashboard com Gráficos Interativos
- [ ] Exportação de Relatórios
- [ ] Integração com Provedores OAuth (Google, GitHub, etc.)
- [ ] Multi-tenancy
- [ ] API Rate Limiting
- [ ] Testes E2E com Playwright

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Contato e Suporte

- **Documentação**: [docs](./docs)
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/sentinela/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/sentinela/discussions)

---

## Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web incrível
- [Next.js](https://nextjs.org/) - Framework React moderno
- [TailwindCSS](https://tailwindcss.com/) - Framework CSS utilitário
- [Lucide](https://lucide.dev/) - Ícones lindos e consistentes

---

<div align="center">

**Desenvolvido com ❤️ usando FastAPI + Next.js**

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!

</div>
