# Guia de Migrations com Alembic

## 📋 Visão Geral

Este projeto usa **Alembic** para gerenciar migrations do banco de dados PostgreSQL.

## 🔧 Configuração

### Arquivos de Configuração:
- `alembic.ini` - Configuração principal do Alembic
- `alembic/env.py` - Script de ambiente que importa os models
- `alembic/versions/` - Diretório com as migrations

### Conexão com Banco:
```ini
# alembic.ini
sqlalchemy.url = postgresql://sentinela:sentinela_secret@localhost:5434/sentinela
```

## 🚀 Comandos Principais

### 1. Gerar Nova Migration (Autogenerate)
```bash
# Detecta automaticamente mudanças nos models
alembic revision --autogenerate -m "Descrição da mudança"

# Exemplo:
alembic revision --autogenerate -m "Add column email to applications"
```

### 2. Aplicar Migrations
```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Aplicar até uma revisão específica
alembic upgrade <revision_id>

# Aplicar apenas a próxima migration
alembic upgrade +1
```

### 3. Reverter Migrations
```bash
# Reverter todas as migrations
alembic downgrade base

# Reverter até uma revisão específica
alembic downgrade <revision_id>

# Reverter apenas a última migration
alembic downgrade -1
```

### 4. Verificar Status
```bash
# Ver revisão atual do banco
alembic current

# Ver histórico de migrations
alembic history

# Ver migrations pendentes
alembic history --verbose
```

### 5. Criar Migration Manual
```bash
# Criar migration em branco para escrever manualmente
alembic revision -m "Descrição"
```

## 📝 Estrutura de uma Migration

```python
"""Descrição da migration

Revision ID: 8cd48ec3d429
Revises:
Create Date: 2025-11-12 15:26:06.702197
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision: str = '8cd48ec3d429'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Comandos para aplicar a migration
    op.add_column('applications', sa.Column('email', sa.String(255)))

def downgrade() -> None:
    # Comandos para reverter a migration
    op.drop_column('applications', 'email')
```

## 🔄 Workflow Típico

### 1. Alterar Models
```python
# Adicione ou modifique seus models em policy_api/src/models/
class Application(Base):
    __tablename__ = "applications"

    # ... campos existentes ...
    email = Column(String(255), nullable=True)  # Nova coluna
```

### 2. Gerar Migration
```bash
alembic revision --autogenerate -m "Add email to applications"
```

### 3. Revisar Migration Gerada
```bash
# Verificar o arquivo gerado em alembic/versions/
cat policy_api/alembic/versions/xxxx_add_email_to_applications.py
```

### 4. Aplicar Migration
```bash
alembic upgrade head
```

### 5. Verificar no Banco
```bash
# Conectar ao PostgreSQL
docker compose exec postgres psql -U sentinela -d sentinela

# Verificar estrutura da tabela
\d applications
```

## ⚠️ Boas Práticas

### ✅ DO:
1. **Sempre revisar migrations autogenerate** antes de aplicar
2. **Testar migrations em ambiente de desenvolvimento** primeiro
3. **Criar backups** antes de aplicar em produção
4. **Commitar migrations** junto com mudanças de código
5. **Escrever mensagens descritivas** nas migrations

### ❌ DON'T:
1. **Não editar migrations já aplicadas** em produção
2. **Não pular migrations** - sempre aplique em ordem
3. **Não usar autogenerate sem revisar** - pode detectar mudanças indesejadas
4. **Não deletar migrations** já commitadas

## 🐛 Troubleshooting

### Erro: "Can't locate revision identified by 'xxxx'"
```bash
# Limpar o cache e aplicar novamente
alembic stamp head
```

### Erro: "Table already exists"
```bash
# Marcar a migration como aplicada sem executar
alembic stamp <revision_id>
```

### Erro: "Connection refused"
```bash
# Verificar se PostgreSQL está rodando
docker compose ps postgres

# Iniciar se necessário
docker compose up -d postgres
```

### Verificar Versão no Banco
```sql
-- No PostgreSQL
SELECT version_num FROM alembic_version;
```

## 🎯 Exemplos Práticos

### Exemplo 1: Adicionar Coluna
```python
# migration upgrade()
op.add_column('applications',
    sa.Column('support_email', sa.String(255), nullable=True)
)

# migration downgrade()
op.drop_column('applications', 'support_email')
```

### Exemplo 2: Criar Índice
```python
# migration upgrade()
op.create_index('idx_applications_email', 'applications', ['email'])

# migration downgrade()
op.drop_index('idx_applications_email', table_name='applications')
```

### Exemplo 3: Adicionar Foreign Key
```python
# migration upgrade()
op.add_column('api_keys',
    sa.Column('user_id', sa.UUID(), nullable=True)
)
op.create_foreign_key(
    'fk_api_keys_user_id', 'api_keys', 'users',
    ['user_id'], ['id']
)

# migration downgrade()
op.drop_constraint('fk_api_keys_user_id', 'api_keys', type_='foreignkey')
op.drop_column('api_keys', 'user_id')
```

### Exemplo 4: Seed Data
```python
# migration upgrade()
from sqlalchemy import table, column
from sqlalchemy import String, UUID

applications = table('applications',
    column('id', UUID),
    column('name', String),
    column('slug', String)
)

op.bulk_insert(applications, [
    {'name': 'Demo App', 'slug': 'demo-app'}
])

# migration downgrade()
op.execute("DELETE FROM applications WHERE slug = 'demo-app'")
```

## 📊 Status Atual

### Migrations Criadas:
- ✅ `8cd48ec3d429` - Initial migration: Application and APIKey tables

### Próximos Passos:
1. Aplicar migration inicial com `alembic upgrade head`
2. Sincronizar com schema existente se necessário
3. Gerar novas migrations conforme models evoluem

---

## 🔗 Referências

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
