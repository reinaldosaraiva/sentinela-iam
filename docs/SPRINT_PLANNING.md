# Sentinela IAM - Sprint Planning (6 Semanas)
**Metodologia**: Agile/Scrum
**Sprint Duration**: 1 semana (5 dias úteis)
**Data Início**: 12 de Novembro de 2025
**Data Fim**: 20 de Dezembro de 2025

---

## 📊 Overview Geral

### Objetivo Principal
Transformar Sentinela em plataforma de gerenciamento centralizado de autorização para múltiplas aplicações, com foco em usabilidade e adoção rápida.

### Métricas de Sucesso
- ✅ 3 features de alta prioridade implementadas
- ✅ SDK funcional em 2 linguagens
- ✅ Documentação completa de integração
- ✅ 3 aplicações demo integradas
- ✅ Testes E2E cobrindo fluxos críticos

---

## 🎯 Sprint 1: Application Registry (12-18 Nov)
**Tema**: "Base para Multi-App"
**Objetivo**: Permitir cadastro e gerenciamento de múltiplas aplicações

### 📋 Backlog do Sprint

#### Backend (20 horas)

**1.1 Modelo de Dados - Application (3h)**
- [ ] Criar migration `create_applications_table`
  ```sql
  - id (UUID, PK)
  - name (VARCHAR 255)
  - slug (VARCHAR 100, UNIQUE)
  - description (TEXT)
  - logo_url (VARCHAR 500)
  - website_url (VARCHAR 500)
  - status (ENUM: active, paused, archived)
  - environment (ENUM: development, staging, production)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - created_by (UUID, FK)
  ```
- [ ] Criar model `Application` em SQLAlchemy/Prisma
- [ ] Adicionar validações (name required, slug unique)
- [ ] Testes unitários do modelo

**1.2 API Keys Management (4h)**
- [ ] Criar migration `create_api_keys_table`
  ```sql
  - id (UUID, PK)
  - application_id (UUID, FK)
  - name (VARCHAR 100)
  - key_prefix (VARCHAR 10) -- 'app_'
  - key_hash (VARCHAR 255) -- bcrypt
  - last_used_at (TIMESTAMP)
  - expires_at (TIMESTAMP)
  - is_active (BOOLEAN)
  - created_at (TIMESTAMP)
  ```
- [ ] Função para gerar API key segura (crypto.randomBytes)
- [ ] Endpoint POST `/applications/:id/api-keys`
- [ ] Endpoint GET `/applications/:id/api-keys` (lista com chave mascarada)
- [ ] Endpoint DELETE `/api-keys/:id`
- [ ] Endpoint POST `/api-keys/:id/rotate`
- [ ] Middleware de validação de API key
- [ ] Testes de API

**1.3 CRUD Endpoints - Applications (5h)**
- [ ] POST `/applications` - Criar aplicação
  - Validar nome único
  - Gerar slug automaticamente
  - Criar primeira API key
  - Retornar API key (única vez)
- [ ] GET `/applications` - Listar com paginação
  - Query params: page, limit, status, environment
  - Incluir métricas básicas (user_count, request_count)
- [ ] GET `/applications/:id` - Detalhes completos
  - Incluir API keys (mascaradas)
  - Incluir estatísticas
- [ ] PUT `/applications/:id` - Atualizar
  - Não permitir alterar slug
- [ ] DELETE `/applications/:id` - Soft delete
  - Arquivar em vez de deletar
  - Desativar todas as API keys
- [ ] PATCH `/applications/:id/status` - Alterar status
- [ ] Documentação OpenAPI/Swagger

**1.4 Métricas por Aplicação (3h)**
- [ ] Criar migration `application_metrics_table`
  ```sql
  - id (UUID, PK)
  - application_id (UUID, FK)
  - date (DATE)
  - total_requests (INTEGER)
  - total_users (INTEGER)
  - successful_auth (INTEGER)
  - failed_auth (INTEGER)
  - avg_response_time (FLOAT)
  ```
- [ ] Job para calcular métricas diárias
- [ ] Endpoint GET `/applications/:id/metrics`
- [ ] Gráficos de métricas (últimos 30 dias)

**1.5 Integration Guide Generator (2h)**
- [ ] Template de guia de integração por linguagem
- [ ] Endpoint GET `/applications/:id/integration-guide?lang=js`
- [ ] Gerar código de exemplo com API key
- [ ] Incluir instruções passo a passo

**1.6 Testes e Documentação (3h)**
- [ ] Testes unitários de models
- [ ] Testes de integração de APIs
- [ ] Testes de segurança (API key validation)
- [ ] Documentação de APIs (Swagger)
- [ ] Exemplos de uso (Postman collection)

#### Frontend (20 horas)

**1.7 Página /applications (6h)**
- [ ] Criar rota `/applications/page.tsx`
- [ ] Layout com grid de cards
- [ ] Card de aplicação:
  - Logo (placeholder se não houver)
  - Nome e descrição
  - Status badge (ativo/pausado)
  - Ambiente badge (dev/staging/prod)
  - Métricas (usuários, requisições)
  - Botões: Ver detalhes, Editar, Deletar
- [ ] Empty state quando não há apps
- [ ] Loading skeleton
- [ ] Error handling
- [ ] Responsivo (mobile/tablet/desktop)

**1.8 Modal Create Application (4h)**
- [ ] Componente `CreateApplicationModal.tsx`
- [ ] Formulário com validação (react-hook-form + zod):
  - Nome (required, min 3 chars)
  - Descrição (optional)
  - URL do site (optional, valid URL)
  - Upload de logo (optional, max 2MB)
  - Ambiente (select: dev/staging/prod)
- [ ] Preview do slug gerado
- [ ] Submit com loading state
- [ ] Success: Mostrar API key uma única vez
- [ ] Modal de confirmação "Save API Key"
- [ ] Copy to clipboard da API key
- [ ] Download da API key (.env format)

**1.9 Página /applications/:id (5h)**
- [ ] Rota dinâmica `/applications/[id]/page.tsx`
- [ ] Tabs:
  1. **Overview**
     - Informações gerais
     - Métricas em cards (usuários, req/dia)
     - Gráfico de requisições (recharts)
     - Status e ambiente
  2. **API Keys**
     - Lista de API keys (mascaradas)
     - Botão "Create New Key"
     - Botão "Rotate Key"
     - Botão "Delete Key"
     - Last used timestamp
  3. **Integration**
     - Guia de integração
     - Code snippets (JavaScript, Python, cURL)
     - Copy button em cada snippet
     - Link para docs completa
  4. **Settings**
     - Editar nome, descrição, logo
     - Alterar status
     - Danger zone: Delete application
- [ ] Breadcrumb navigation
- [ ] Edit in-place para campos simples

**1.10 API Keys Management UI (3h)**
- [ ] Modal `CreateApiKeyModal.tsx`
  - Nome da chave (ex: "Production Key")
  - Expiração (optional, date picker)
  - Submit e mostrar chave uma vez
- [ ] Componente `ApiKeyCard.tsx`
  - Nome da chave
  - Chave mascarada (app_***************xyz)
  - Copy button (copia chave completa do backend)
  - Last used timestamp
  - Status (ativo/expirado)
  - Actions: Rotate, Delete
- [ ] Confirmação de delete
- [ ] Toast notifications

**1.11 Integration Guide Component (2h)**
- [ ] Componente `IntegrationGuide.tsx`
- [ ] Tabs por linguagem (JS, Python, cURL, Java)
- [ ] Syntax highlighting (prism-react-renderer)
- [ ] Copy button em cada código
- [ ] Stepper (1, 2, 3) com instruções
- [ ] Link "Need help?" para docs

#### DevOps & Infra (5 horas)

**1.12 Database Setup (2h)**
- [ ] Adicionar PostgreSQL ao docker-compose
- [ ] Configurar connection pooling
- [ ] Criar script de migrations
- [ ] Seed data para desenvolvimento
- [ ] Backup strategy

**1.13 Environment Variables (1h)**
- [ ] `.env.example` atualizado
- [ ] Documentar variáveis novas
- [ ] Validação de variáveis no startup

**1.14 CI/CD (2h)**
- [ ] GitHub Actions workflow
- [ ] Run migrations automaticamente
- [ ] Build e teste de backend
- [ ] Build e teste de frontend
- [ ] Deploy preview (opcional)

### 📦 Entregáveis do Sprint 1
- [x] Application Registry completo (CRUD)
- [x] API Keys management funcional
- [x] Interface de gerenciamento de apps
- [x] Guia de integração gerado
- [x] Métricas básicas por app
- [x] 1 aplicação demo integrada

### 🎯 Definition of Done
- [ ] Todos os testes passando (unit + integration)
- [ ] Code review aprovado
- [ ] Documentação atualizada
- [ ] Demonstração funcional gravada
- [ ] Deployed em staging

---

## 🎯 Sprint 2: Resources & Actions + Roles System (19-25 Nov)
**Tema**: "RBAC Visual"
**Objetivo**: Implementar gerenciamento visual de recursos, ações e roles

### 📋 Backlog do Sprint

#### Backend (22 horas)

**2.1 Modelo de Dados - Resources (4h)**
- [ ] Migration `create_resources_table`
  ```sql
  - id (UUID, PK)
  - application_id (UUID, FK)
  - name (VARCHAR 100) -- 'Document'
  - key (VARCHAR 100) -- 'document' (lowercase)
  - description (TEXT)
  - attributes (JSONB) -- custom attributes
  - parent_id (UUID, FK) -- hierarchia
  - created_at (TIMESTAMP)
  ```
- [ ] Migration `create_actions_table`
  ```sql
  - id (UUID, PK)
  - application_id (UUID, FK)
  - name (VARCHAR 100) -- 'Read'
  - key (VARCHAR 100) -- 'read'
  - description (TEXT)
  - category (ENUM: crud, custom)
  - created_at (TIMESTAMP)
  ```
- [ ] Migration `resource_actions` (M2M)
  ```sql
  - resource_id (UUID, FK)
  - action_id (UUID, FK)
  - PRIMARY KEY (resource_id, action_id)
  ```
- [ ] Models + validações
- [ ] Testes unitários

**2.2 CRUD APIs - Resources & Actions (6h)**
- [ ] POST `/applications/:app_id/resources`
- [ ] GET `/applications/:app_id/resources`
- [ ] PUT `/resources/:id`
- [ ] DELETE `/resources/:id`
- [ ] POST `/applications/:app_id/actions`
- [ ] GET `/applications/:app_id/actions`
- [ ] POST `/resources/:id/actions` (associar ações)
- [ ] GET `/resources/:id/actions` (listar ações permitidas)
- [ ] Validação: não permitir duplicatas
- [ ] Testes de API

**2.3 Modelo de Dados - Roles & Permissions (5h)**
- [ ] Migration `create_roles_table`
  ```sql
  - id (UUID, PK)
  - application_id (UUID, FK)
  - name (VARCHAR 100)
  - key (VARCHAR 100)
  - description (TEXT)
  - parent_role_id (UUID, FK) -- herança
  - is_system (BOOLEAN) -- roles built-in
  - created_at (TIMESTAMP)
  ```
- [ ] Migration `create_permissions_table`
  ```sql
  - id (UUID, PK)
  - role_id (UUID, FK)
  - resource_id (UUID, FK)
  - action_id (UUID, FK)
  - conditions (JSONB) -- ABAC conditions
  - effect (ENUM: allow, deny)
  - created_at (TIMESTAMP)
  ```
- [ ] Migration `user_roles` (M2M)
- [ ] Migration `group_roles` (M2M)
- [ ] Models + validações
- [ ] Lógica de herança de roles
- [ ] Testes de herança

**2.4 CRUD APIs - Roles & Permissions (5h)**
- [ ] POST `/applications/:app_id/roles`
- [ ] GET `/applications/:app_id/roles` (incluir permissions)
- [ ] PUT `/roles/:id`
- [ ] DELETE `/roles/:id` (verificar se não é system role)
- [ ] POST `/roles/:id/permissions` (adicionar permissão)
- [ ] DELETE `/roles/:role_id/permissions/:perm_id`
- [ ] GET `/roles/:id/permissions/matrix` (retornar matriz)
- [ ] POST `/roles/:role_id/users/:user_id` (atribuir role)
- [ ] DELETE `/roles/:role_id/users/:user_id`
- [ ] Testes de API

**2.5 Permission Checker Service (2h)**
- [ ] Classe `PermissionChecker`
- [ ] Método `hasPermission(user, action, resource, context)`
- [ ] Resolver herança de roles
- [ ] Avaliar condições ABAC
- [ ] Cache de permissões (Redis)
- [ ] Testes unitários

#### Frontend (18 horas)

**2.6 Página /resources (5h)**
- [ ] Rota `/applications/[id]/resources/page.tsx`
- [ ] Lista de recursos com ações associadas
- [ ] Card de recurso:
  - Nome e descrição
  - Lista de ações (badges)
  - Contador de permissões usando esse recurso
  - Actions: Edit, Delete
- [ ] Modal criar recurso
- [ ] Modal associar ações
- [ ] Tree view para hierarquia (react-arborist)

**2.7 Página /actions (3h)**
- [ ] Rota `/applications/[id]/actions/page.tsx`
- [ ] Lista de ações agrupadas por categoria
- [ ] CRUD actions (similar a resources)
- [ ] Badges de categoria (CRUD vs Custom)

**2.8 Página /roles (7h)**
- [ ] Rota `/applications/[id]/roles/page.tsx`
- [ ] Card de role:
  - Nome e descrição
  - Número de permissões
  - Número de usuários com esse role
  - Badge se é system role
  - Hierarquia visual (parent → child)
- [ ] Modal criar/editar role
- [ ] Seletor de parent role

**2.9 Permission Matrix Component (3h)**
- [ ] Componente `PermissionMatrix.tsx`
- [ ] Tabela interativa:
  - Linhas: Recursos x Ações
  - Colunas: Roles
  - Células: Checkbox (allow/deny/none)
- [ ] Click para toggle permissão
- [ ] Highlight de herança (permissão vinda de parent)
- [ ] Filtros: por recurso, por role
- [ ] Export para CSV

### 📦 Entregáveis do Sprint 2
- [x] Resources & Actions management
- [x] Roles & Permissions system
- [x] Permission Matrix visual
- [x] Role inheritance funcionando
- [x] Atribuição de roles a usuários/grupos

### 🎯 Definition of Done
- [ ] Permission checker validado com testes
- [ ] Matrix interativa funcionando
- [ ] Herança de roles testada
- [ ] Documentação de RBAC

---

## 🎯 Sprint 3: Visual Policy Builder (26 Nov - 2 Dez)
**Tema**: "No-Code Policy Creation"
**Objetivo**: Editor visual para criar políticas sem escrever Cedar

### 📋 Backlog do Sprint

#### Backend (15 horas)

**3.1 Policy Templates (4h)**
- [ ] Criar tabela `policy_templates`
- [ ] Templates pré-definidos:
  - Basic RBAC
  - Time-based access
  - Attribute-based
  - Owner-only access
  - Team-based access
- [ ] Endpoint GET `/policy-templates`
- [ ] Endpoint POST `/policies/from-template`
- [ ] Variáveis substituíveis nos templates

**3.2 Policy Builder Service (6h)**
- [ ] Classe `PolicyBuilder`
- [ ] Método `buildFromBlocks(blocks)` → Cedar code
- [ ] Blocos suportados:
  - Principal block (user, group, role)
  - Action block (single, multiple, wildcard)
  - Resource block (single, multiple, wildcard)
  - Condition block (when/unless)
- [ ] Validação de blocos
- [ ] Preview de Cedar gerado
- [ ] Testes de geração

**3.3 Policy Validation Enhanced (3h)**
- [ ] Validação sintática Cedar
- [ ] Validação semântica (recursos existem?)
- [ ] Sugestões de correção
- [ ] Endpoint POST `/policies/validate`
- [ ] Retornar erros estruturados

**3.4 Policy Diff (2h)**
- [ ] Comparação entre versões
- [ ] Highlight de mudanças
- [ ] Endpoint GET `/policies/:id/diff/:version`

#### Frontend (20 horas)

**3.5 Policy Builder Canvas (10h)**
- [ ] Rota `/policies/builder/page.tsx`
- [ ] Canvas drag-and-drop (react-dnd-kit)
- [ ] Blocos disponíveis:
  - Principal selector
  - Action selector
  - Resource selector
  - Condition builder
  - Effect selector (allow/deny)
- [ ] Drag from sidebar → drop on canvas
- [ ] Conectores visuais (arrows)
- [ ] Validação em tempo real
- [ ] Preview Cedar gerado (live)
- [ ] Save como draft ou publish

**3.6 Condition Builder (5h)**
- [ ] Componente `ConditionBuilder.tsx`
- [ ] Operadores suportados:
  - Comparison: ==, !=, >, <, >=, <=
  - Logical: AND, OR, NOT
  - Membership: in, has
  - String: contains, startsWith, endsWith
- [ ] Attribute selector (user.*, resource.*, context.*)
- [ ] Value input (string, number, date, boolean)
- [ ] Nested conditions (parênteses)
- [ ] Preview da expressão

**3.7 Templates Selector (3h)**
- [ ] Sidebar com templates
- [ ] Preview de cada template
- [ ] Aplicar template (preenche canvas)
- [ ] Customizar variáveis do template

**3.8 Policy Wizard (2h)**
- [ ] Modo guiado passo a passo
- [ ] Step 1: Escolher template
- [ ] Step 2: Selecionar entidades
- [ ] Step 3: Adicionar condições
- [ ] Step 4: Review e save
- [ ] Progress indicator

### 📦 Entregáveis do Sprint 3
- [x] Policy Builder canvas funcional
- [x] 5 templates pré-definidos
- [x] Condition builder visual
- [x] Geração de Cedar code
- [x] Validação em tempo real

---

## 🎯 Sprint 4: SDKs (3-9 Dez)
**Tema**: "Integração Fácil"
**Objetivo**: SDKs funcionais em JavaScript e Python

### 📋 Backlog do Sprint

#### SDK JavaScript/TypeScript (20 horas)

**4.1 Setup do Projeto (3h)**
- [ ] Criar repo `@sentinela/sdk-js`
- [ ] Setup TypeScript + tsup
- [ ] Setup Jest + testing-library
- [ ] Setup Prettier + ESLint
- [ ] Package.json configurado
- [ ] CI/CD (GitHub Actions)

**4.2 Core Client (6h)**
- [ ] Classe `SentinelaClient`
- [ ] Constructor com options:
  ```typescript
  new SentinelaClient({
    apiKey: string,
    baseURL?: string,
    timeout?: number,
    cache?: CacheConfig
  })
  ```
- [ ] HTTP client (axios ou fetch)
- [ ] Error handling
- [ ] Retry logic
- [ ] Rate limiting
- [ ] Logging
- [ ] Testes unitários

**4.3 Authorization Methods (5h)**
- [ ] Método `check(request)`:
  ```typescript
  await client.check({
    user: string | { id, email, attributes },
    action: string,
    resource: string | { type, id, attributes },
    context?: Record<string, any>
  }): Promise<{ allowed: boolean, reason?: string }>
  ```
- [ ] Método `batchCheck(requests[])`: múltiplos checks
- [ ] Método `getUserPermissions(userId)`: lista permissões
- [ ] Método `getUserRoles(userId)`: lista roles
- [ ] Cache local de permissões (LRU)
- [ ] Testes de integração

**4.4 Sync Methods (3h)**
- [ ] Método `syncUser(user)`: criar/atualizar usuário
- [ ] Método `syncUsers(users[])`: batch sync
- [ ] Método `deleteUser(userId)`
- [ ] Método `assignRole(userId, roleId)`
- [ ] Método `removeRole(userId, roleId)`
- [ ] Testes

**4.5 React Hooks (3h)**
- [ ] Hook `usePermission(action, resource)`:
  ```typescript
  const { permitted, loading, error } = usePermission('read', 'doc:123');
  ```
- [ ] Hook `useUser()`: current user context
- [ ] Component `<IfPermitted>`:
  ```jsx
  <IfPermitted action="delete" resource="doc:123">
    <button>Delete</button>
  </IfPermitted>
  ```
- [ ] Provider `<SentinelaProvider client={client}>`
- [ ] Testes com React Testing Library

#### SDK Python (15 horas)

**4.6 Setup do Projeto (2h)**
- [ ] Criar repo `sentinela-python-sdk`
- [ ] Setup Poetry ou UV
- [ ] Setup pytest
- [ ] Setup black + ruff
- [ ] CI/CD

**4.7 Core Client (5h)**
- [ ] Classe `SentinelaClient`
- [ ] HTTP client (httpx async)
- [ ] Error handling
- [ ] Retry logic
- [ ] Type hints (Pydantic models)
- [ ] Testes unitários

**4.8 Authorization Methods (4h)**
- [ ] Método `check()`
- [ ] Método `batch_check()`
- [ ] Método `get_user_permissions()`
- [ ] Método `get_user_roles()`
- [ ] Cache com TTL (cachetools)
- [ ] Testes

**4.9 Sync Methods (2h)**
- [ ] Método `sync_user()`
- [ ] Método `sync_users()`
- [ ] Método `delete_user()`
- [ ] Método `assign_role()`
- [ ] Método `remove_role()`

**4.10 Framework Integrations (2h)**
- [ ] Decorator para Flask: `@require_permission`
- [ ] Decorator para FastAPI: `@require_permission`
- [ ] Middleware para Django
- [ ] Exemplos de uso

#### Documentação (5 horas)

**4.11 SDK Documentation (5h)**
- [ ] README completo para cada SDK
- [ ] Getting started guides
- [ ] API Reference (auto-generated)
- [ ] Exemplos de código
- [ ] Migration guides
- [ ] Troubleshooting
- [ ] Changelog

### 📦 Entregáveis do Sprint 4
- [x] SDK JavaScript publicado no NPM
- [x] SDK Python publicado no PyPI
- [x] React hooks funcionando
- [x] Decorators Flask/FastAPI
- [x] Documentação completa

---

## 🎯 Sprint 5: Multi-Tenancy (10-16 Dez)
**Tema**: "Organizações"
**Objetivo**: Suporte para múltiplos tenants isolados

### 📋 Backlog do Sprint

#### Backend (18 horas)

**5.1 Modelo de Dados - Organizations (4h)**
- [ ] Migration `create_organizations_table`
  ```sql
  - id (UUID, PK)
  - name (VARCHAR 255)
  - slug (VARCHAR 100, UNIQUE)
  - logo_url (VARCHAR 500)
  - plan (ENUM: free, starter, pro, enterprise)
  - status (ENUM: active, suspended, deleted)
  - settings (JSONB)
  - created_at (TIMESTAMP)
  ```
- [ ] Migration `organization_members`
- [ ] Migration adicionar `organization_id` em:
  - applications
  - users
  - groups
  - policies
  - resources
  - actions
  - roles
- [ ] Models + constraints

**5.2 Tenant Isolation Middleware (5h)**
- [ ] Middleware para extrair tenant_id do request
- [ ] Tenant context manager
- [ ] Query filters automáticos (SQLAlchemy)
- [ ] Validação de acesso cross-tenant
- [ ] Testes de isolamento

**5.3 Organization Management APIs (5h)**
- [ ] CRUD completo de organizations
- [ ] Membership management
- [ ] Roles por organização (owner, admin, member)
- [ ] Invite system (send invite, accept invite)
- [ ] Switch organization (GET `/me/organizations`)
- [ ] Testes

**5.4 Billing & Plans (4h)**
- [ ] Modelo de planos
- [ ] Limites por plano (apps, users, requests)
- [ ] Enforcement de limites
- [ ] Upgrade/downgrade flow
- [ ] Usage tracking

#### Frontend (17 horas)

**5.5 Organization Selector (4h)**
- [ ] Dropdown no header
- [ ] Lista de organizações do usuário
- [ ] Switch organization (salvar em localStorage)
- [ ] Indicador visual da org atual
- [ ] Loading state

**5.6 Página /organizations (5h)**
- [ ] Lista de organizações
- [ ] Create organization modal
- [ ] Settings por organização
- [ ] Members management
- [ ] Invite members
- [ ] Billing info

**5.7 Organization Settings (5h)**
- [ ] General settings
- [ ] Members & Roles
- [ ] Billing & Plan
- [ ] Usage & Limits
- [ ] Danger zone (delete org)

**5.8 Onboarding Flow (3h)**
- [ ] Wizard de criação de org
- [ ] Step 1: Nome e logo
- [ ] Step 2: Criar primeira aplicação
- [ ] Step 3: Convidar membros
- [ ] Step 4: Integration guide

### 📦 Entregáveis do Sprint 5
- [x] Multi-tenancy funcional
- [x] Isolamento total de dados
- [x] Organization switcher
- [x] Billing & plans básico
- [x] Onboarding flow

---

## 🎯 Sprint 6: Polish & Testing (17-20 Dez)
**Tema**: "Qualidade e Estabilidade"
**Objetivo**: Testes, documentação e melhorias finais

### 📋 Backlog do Sprint

#### Testing (15 horas)

**6.1 Testes E2E (8h)**
- [ ] Setup Playwright ou Cypress
- [ ] Fluxo: Criar conta → Criar org → Criar app
- [ ] Fluxo: Criar recurso → Criar ação → Criar role
- [ ] Fluxo: Criar política visual → Testar autorização
- [ ] Fluxo: Integrar SDK → Validar check
- [ ] Smoke tests de todas as páginas
- [ ] CI/CD integration

**6.2 Performance Testing (3h)**
- [ ] Load testing com k6
- [ ] Cenário: 100 req/s de authorization checks
- [ ] Cenário: 10 req/s de policy updates
- [ ] Identificar bottlenecks
- [ ] Otimizações (índices, cache)

**6.3 Security Testing (4h)**
- [ ] OWASP ZAP scan
- [ ] SQL injection tests
- [ ] XSS tests
- [ ] CSRF tests
- [ ] Authentication bypass tests
- [ ] Fix vulnerabilities encontradas

#### Documentation (10 horas)

**6.4 User Documentation (5h)**
- [ ] Getting Started Guide
- [ ] Concepts (Resources, Actions, Roles, Policies)
- [ ] Tutorials:
  - Integrar primeira aplicação
  - Criar seu primeiro role
  - Testar políticas no playground
- [ ] Video tutorials (Loom)
- [ ] FAQ

**6.5 Developer Documentation (5h)**
- [ ] Architecture overview
- [ ] API Reference (Swagger UI)
- [ ] SDK References
- [ ] Best practices
- [ ] Migration guides (de outras soluções)
- [ ] Contributing guide

#### Final Polish (10 horas)

**6.6 UI/UX Improvements (5h)**
- [ ] Adicionar micro-interactions
- [ ] Loading skeletons em todas as páginas
- [ ] Empty states melhores
- [ ] Error pages (404, 500)
- [ ] Toast notifications padronizadas
- [ ] Acessibilidade (ARIA labels)
- [ ] Dark mode fixes

**6.7 Performance Optimizations (3h)**
- [ ] Code splitting (React.lazy)
- [ ] Image optimization
- [ ] Bundle size analysis
- [ ] CDN para assets estáticos
- [ ] Service worker (PWA)

**6.8 Demo Applications (2h)**
- [ ] App demo 1: Blog com comments
- [ ] App demo 2: Project management tool
- [ ] App demo 3: E-commerce admin
- [ ] Deploy demos publicly

### 📦 Entregáveis do Sprint 6
- [x] Testes E2E cobrindo fluxos críticos
- [x] Documentação completa
- [x] Performance otimizado
- [x] Security hardened
- [x] 3 demos funcionais

---

## 📊 Métricas de Acompanhamento

### Daily Standup Questions
1. O que fiz ontem?
2. O que farei hoje?
3. Tenho algum bloqueio?

### Sprint Metrics
- **Velocity**: Story points completados
- **Burndown**: Progresso diário
- **Bug count**: Bugs abertos vs fechados
- **Test coverage**: % de código testado
- **Technical debt**: Horas estimadas

### Weekly Review
- Demo das features completadas
- Retrospectiva: O que funcionou? O que melhorar?
- Ajuste de prioridades

---

## 🎯 Definition of Ready (DoR)

Antes de iniciar uma tarefa:
- [ ] User story clara e compreendida
- [ ] Critérios de aceite definidos
- [ ] Dependências identificadas
- [ ] Estimativa de esforço feita
- [ ] Mockups/wireframes disponíveis (se UI)

## ✅ Definition of Done (DoD)

Uma tarefa está completa quando:
- [ ] Código implementado e commitado
- [ ] Testes unitários passando
- [ ] Testes de integração passando (se aplicável)
- [ ] Code review aprovado
- [ ] Documentação atualizada
- [ ] Deployed em staging
- [ ] QA validou funcionamento
- [ ] Product owner aceitou

---

## 🚧 Riscos e Mitigações

### Riscos Identificados

**1. Complexidade do Policy Builder**
- **Probabilidade**: Alta
- **Impacto**: Médio
- **Mitigação**: Começar com MVP simples, iterar baseado em feedback

**2. Performance de Authorization Checks**
- **Probabilidade**: Média
- **Impacto**: Alto
- **Mitigação**: Implementar cache desde o início, load testing early

**3. Migração de dados para Multi-Tenancy**
- **Probabilidade**: Baixa
- **Impacto**: Alto
- **Mitigação**: Planejar migration strategy, backup de dados

**4. Adoção dos SDKs**
- **Probabilidade**: Média
- **Impacto**: Médio
- **Mitigação**: Documentação excelente, exemplos claros, suporte ativo

---

## 📅 Calendário de Entregas

| Sprint | Datas | Entregável Principal | Demo Date |
|--------|-------|---------------------|-----------|
| Sprint 1 | 12-18 Nov | Application Registry | 18 Nov |
| Sprint 2 | 19-25 Nov | RBAC Visual | 25 Nov |
| Sprint 3 | 26 Nov-2 Dez | Policy Builder | 2 Dez |
| Sprint 4 | 3-9 Dez | SDKs JS + Python | 9 Dez |
| Sprint 5 | 10-16 Dez | Multi-Tenancy | 16 Dez |
| Sprint 6 | 17-20 Dez | Polish + Testing | 20 Dez |

**🎉 Launch Date: 20 de Dezembro de 2025**

---

## 🎯 Próximos Passos Imediatos

### Esta Semana (Começar AGORA):
1. [ ] Setup PostgreSQL no projeto
2. [ ] Criar primeira migration (applications table)
3. [ ] Implementar POST /applications endpoint
4. [ ] Criar página /applications no frontend
5. [ ] Deploy em staging

### Amanhã (13 Nov):
- [ ] Standup meeting às 9:00
- [ ] Pair programming: API Keys management
- [ ] Code review: Application model
- [ ] Update sprint board

---

**Status**: 🚀 Pronto para iniciar Sprint 1
**Última atualização**: 12 de Novembro de 2025
**Próxima revisão**: 18 de Novembro de 2025 (Sprint Review)
