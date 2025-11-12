#!/usr/bin/env python3
"""
Simple Web Interface for Sentinela Authorization System
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import requests
import json

app = Flask(__name__)

# URLs dos serviços
KEYCLOAK_URL = "http://localhost:8081"
POLICY_API_URL = "http://localhost:8000"
BUSINESS_API_URL = "http://localhost:8001"

# Template HTML simples
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinela - Sistema de Autorização</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; }
        .header h1 { text-align: center; font-size: 2rem; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .card { background: white; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .card h2 { color: #333; margin-bottom: 1rem; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem; }
        .status { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; margin: 0.5rem 0; border-radius: 4px; }
        .status.healthy { background: #d4edda; color: #155724; }
        .status.unhealthy { background: #f8d7da; color: #721c24; }
        .btn { background: #667eea; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 4px; cursor: pointer; margin: 0.25rem; }
        .btn:hover { background: #5a6fd8; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
        .form-group textarea { height: 100px; resize: vertical; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .policy-item, .document-item { background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; border-left: 4px solid #667eea; }
        .user-info { background: #e3f2fd; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; }
        .tabs { display: flex; margin-bottom: 1rem; }
        .tab { padding: 1rem; background: #e9ecef; cursor: pointer; border: 1px solid #dee2e6; border-bottom: none; }
        .tab.active { background: white; border-bottom: 1px solid white; margin-bottom: -1px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .alert { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
        .alert.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        pre { background: #f8f9fa; padding: 1rem; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Sentinela - Sistema de Autorização</h1>
        <p style="text-align: center; margin-top: 0.5rem;">Interface Administrativa</p>
    </div>
    
    <div class="container">
        <!-- Status dos Serviços -->
        <div class="card">
            <h2>🏥 Status dos Serviços</h2>
            <div id="services-status">
                <div class="status">
                    <span>🔐 Mock Keycloak</span>
                    <span id="keycloak-status">Verificando...</span>
                </div>
                <div class="status">
                    <span>📋 Policy API</span>
                    <span id="policy-status">Verificando...</span>
                </div>
                <div class="status">
                    <span>💼 Business API</span>
                    <span id="business-status">Verificando...</span>
                </div>
            </div>
            <button class="btn" onclick="refreshStatus()">🔄 Atualizar Status</button>
        </div>

        <!-- Abas de Funcionalidades -->
        <div class="tabs">
            <div class="tab active" onclick="showTab('auth')">🔐 Autenticação</div>
            <div class="tab" onclick="showTab('policies')">📋 Políticas</div>
            <div class="tab" onclick="showTab('documents')">📄 Documentos</div>
            <div class="tab" onclick="showTab('authorization')">🛡️ Autorização</div>
        </div>

        <!-- Autenticação -->
        <div id="auth-tab" class="tab-content active">
            <div class="card">
                <h2>🔐 Testar Autenticação</h2>
                <form id="auth-form">
                    <div class="form-group">
                        <label>Usuário:</label>
                        <select name="username">
                            <option value="alice">alice (Funcionária)</option>
                            <option value="bob">bob (Funcionário)</option>
                            <option value="admin">admin (Administrador)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Senha:</label>
                        <input type="password" name="password" value="alice123">
                    </div>
                    <button type="submit" class="btn">🔑 Autenticar</button>
                </form>
                <div id="auth-result"></div>
            </div>
        </div>

        <!-- Políticas -->
        <div id="policies-tab" class="tab-content">
            <div class="card">
                <h2>📋 Gerenciar Políticas</h2>
                <button class="btn" onclick="loadPolicies()">📥 Carregar Políticas</button>
                <button class="btn" onclick="showCreatePolicyForm()">➕ Criar Política</button>
                
                <div id="policies-list"></div>
                
                <div id="create-policy-form" style="display: none; margin-top: 1rem;">
                    <h3>➕ Criar Nova Política</h3>
                    <form id="policy-form">
                        <div class="form-group">
                            <label>Nome:</label>
                            <input type="text" name="name" required>
                        </div>
                        <div class="form-group">
                            <label>Descrição:</label>
                            <input type="text" name="description" required>
                        </div>
                        <div class="form-group">
                            <label>Política (Cedar):</label>
                            <textarea name="policy" placeholder="permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");" required></textarea>
                        </div>
                        <button type="submit" class="btn">💾 Criar Política</button>
                        <button type="button" class="btn btn-danger" onclick="hideCreatePolicyForm()">❌ Cancelar</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Documentos -->
        <div id="documents-tab" class="tab-content">
            <div class="card">
                <h2>📄 Documentos</h2>
                <button class="btn" onclick="loadDocuments()">📥 Carregar Documentos</button>
                <div id="documents-list"></div>
            </div>
        </div>

        <!-- Autorização -->
        <div id="authorization-tab" class="tab-content">
            <div class="card">
                <h2>🛡️ Testar Autorização</h2>
                <form id="authorization-form">
                    <div class="form-group">
                        <label>Principal:</label>
                        <select name="principal">
                            <option value="User::&quot;alice&quot;">User::"alice"</option>
                            <option value="User::&quot;bob&quot;">User::"bob"</option>
                            <option value="User::&quot;admin&quot;">User::"admin"</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Ação:</label>
                        <select name="action">
                            <option value="Action::&quot;read&quot;">Action::"read"</option>
                            <option value="Action::&quot;write&quot;">Action::"write"</option>
                            <option value="Action::&quot;delete&quot;">Action::"delete"</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Recurso:</label>
                        <select name="resource">
                            <option value="Document::&quot;public&quot;">Document::"public"</option>
                            <option value="Document::&quot;hr&quot;">Document::"hr"</option>
                            <option value="Document::&quot;secret&quot;">Document::"secret"</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">🛡️ Verificar Autorização</button>
                </form>
                <div id="authorization-result"></div>
            </div>
        </div>
    </div>

    <script>
        // Funções de navegação
        function showTab(tabName) {
            // Esconder todas as abas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Mostrar aba selecionada
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }

        // Status dos serviços
        async function refreshStatus() {
            try {
                const keycloakResponse = await fetch('http://localhost:8081/health');
                const keycloakStatus = keycloakResponse.ok ? '✅ Saudável' : '❌ Erro';
                document.getElementById('keycloak-status').textContent = keycloakStatus;
                document.getElementById('keycloak-status').parentElement.className = 'status ' + (keycloakResponse.ok ? 'healthy' : 'unhealthy');
            } catch (error) {
                document.getElementById('keycloak-status').textContent = '❌ Indisponível';
                document.getElementById('keycloak-status').parentElement.className = 'status unhealthy';
            }

            try {
                const policyResponse = await fetch('http://localhost:8000/health/');
                const policyStatus = policyResponse.ok ? '✅ Saudável' : '❌ Erro';
                document.getElementById('policy-status').textContent = policyStatus;
                document.getElementById('policy-status').parentElement.className = 'status ' + (policyResponse.ok ? 'healthy' : 'unhealthy');
            } catch (error) {
                document.getElementById('policy-status').textContent = '❌ Indisponível';
                document.getElementById('policy-status').parentElement.className = 'status unhealthy';
            }

            try {
                const businessResponse = await fetch('http://localhost:8001/health');
                const businessStatus = businessResponse.ok ? '✅ Saudável' : '❌ Erro';
                document.getElementById('business-status').textContent = businessStatus;
                document.getElementById('business-status').parentElement.className = 'status ' + (businessResponse.ok ? 'healthy' : 'unhealthy');
            } catch (error) {
                document.getElementById('business-status').textContent = '❌ Indisponível';
                document.getElementById('business-status').parentElement.className = 'status unhealthy';
            }
        }

        // Autenticação
        document.getElementById('auth-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('http://localhost:8081/realms/my-app/protocol/openid-connect/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'client_id': 'sentinela-api',
                        'client_secret': 'sentinela-secret',
                        'username': formData.get('username'),
                        'password': formData.get('password'),
                        'grant_type': 'password'
                    })
                });

                const result = await response.json();
                
                if (response.ok) {
                    const payload = JSON.parse(atob(result.access_token.split('.')[1]));
                    document.getElementById('auth-result').innerHTML = `
                        <div class="alert success">
                            <h4>✅ Autenticação Bem-Sucedida!</h4>
                            <div class="user-info">
                                <strong>Usuário:</strong> ${payload.preferred_username}<br>
                                <strong>Email:</strong> ${payload.email}<br>
                                <strong>Grupos:</strong> ${payload.groups ? payload.groups.join(', ') : 'Nenhum'}<br>
                                <strong>Token:</strong> <code>${result.access_token.substring(0, 50)}...</code>
                            </div>
                        </div>
                    `;
                } else {
                    document.getElementById('auth-result').innerHTML = `
                        <div class="alert error">
                            <h4>❌ Falha na Autenticação</h4>
                            <p>${result.error_description || 'Erro desconhecido'}</p>
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('auth-result').innerHTML = `
                    <div class="alert error">
                        <h4>❌ Erro na Requisição</h4>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        });

        // Políticas
        async function loadPolicies() {
            try {
                const response = await fetch('http://localhost:8000/policies');
                const policies = await response.json();
                
                let html = '<h3>📋 Políticas Existentes</h3>';
                if (policies.length === 0) {
                    html += '<p>Nenhuma política encontrada.</p>';
                } else {
                    policies.forEach(policy => {
                        html += `
                            <div class="policy-item">
                                <h4>${policy.name}</h4>
                                <p><strong>Descrição:</strong> ${policy.description}</p>
                                <p><strong>Política:</strong></p>
                                <pre>${policy.policy}</pre>
                            </div>
                        `;
                    });
                }
                
                document.getElementById('policies-list').innerHTML = html;
            } catch (error) {
                document.getElementById('policies-list').innerHTML = `
                    <div class="alert error">
                        <h4>❌ Erro ao Carregar Políticas</h4>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        }

        function showCreatePolicyForm() {
            document.getElementById('create-policy-form').style.display = 'block';
        }

        function hideCreatePolicyForm() {
            document.getElementById('create-policy-form').style.display = 'none';
        }

        document.getElementById('policy-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('http://localhost:8000/policies', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: formData.get('name'),
                        description: formData.get('description'),
                        policy: formData.get('policy')
                    })
                });

                if (response.ok) {
                    document.getElementById('policies-list').innerHTML = `
                        <div class="alert success">
                            <h4>✅ Política Criada com Sucesso!</h4>
                        </div>
                    `;
                    hideCreatePolicyForm();
                    loadPolicies(); // Recarregar lista
                } else {
                    const error = await response.text();
                    document.getElementById('policies-list').innerHTML = `
                        <div class="alert error">
                            <h4>❌ Erro ao Criar Política</h4>
                            <p>${error}</p>
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('policies-list').innerHTML = `
                    <div class="alert error">
                        <h4>❌ Erro na Requisição</h4>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        });

        // Documentos
        async function loadDocuments() {
            try {
                const response = await fetch('http://localhost:8001/documents');
                const data = await response.json();
                
                let html = '<h3>📄 Documentos Disponíveis</h3>';
                if (data.documents.length === 0) {
                    html += '<p>Nenhum documento encontrado.</p>';
                } else {
                    data.documents.forEach(doc => {
                        html += `
                            <div class="document-item">
                                <h4>${doc.title}</h4>
                                <p><strong>Tipo:</strong> ${doc.document_type}</p>
                                <p><strong>Classificação:</strong> ${doc.classification}</p>
                                <p><strong>Departamento:</strong> ${doc.department}</p>
                                <p><strong>Conteúdo:</strong> ${doc.content}</p>
                                <p><strong>Criado:</strong> ${new Date(doc.created_at).toLocaleString('pt-BR')}</p>
                            </div>
                        `;
                    });
                }
                
                html += `<div class="user-info"><strong>Total de Documentos:</strong> ${data.total}</div>`;
                
                document.getElementById('documents-list').innerHTML = html;
            } catch (error) {
                document.getElementById('documents-list').innerHTML = `
                    <div class="alert error">
                        <h4>❌ Erro ao Carregar Documentos</h4>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        }

        // Autorização
        document.getElementById('authorization-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('http://localhost:8001/authorize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        principal: formData.get('principal'),
                        action: formData.get('action'),
                        resource: formData.get('resource')
                    })
                });

                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('authorization-result').innerHTML = `
                        <div class="alert ${result.allow ? 'success' : 'error'}">
                            <h4>${result.allow ? '✅ PERMITIDO' : '❌ NEGADO'}</h4>
                            <div class="user-info">
                                <strong>Principal:</strong> ${result.principal}<br>
                                <strong>Ação:</strong> ${result.action}<br>
                                <strong>Recurso:</strong> ${result.resource}<br>
                                <strong>Decisão:</strong> ${result.allow ? 'ALLOW' : 'DENY'}
                            </div>
                        </div>
                    `;
                } else {
                    document.getElementById('authorization-result').innerHTML = `
                        <div class="alert error">
                            <h4>❌ Erro na Verificação</h4>
                            <p>${response.statusText}</p>
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('authorization-result').innerHTML = `
                    <div class="alert error">
                        <h4>❌ Erro na Requisição</h4>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        });

        // Carregar status inicial
        refreshStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🌐 Iniciando Interface Web do Sentinela")
    print("=" * 50)
    print("📍 Acesse em: http://localhost:5000")
    print("🔐 Funcionalidades:")
    print("   • Status dos serviços")
    print("   • Teste de autenticação")
    print("   • Gestão de políticas")
    print("   • Visualização de documentos")
    print("   • Teste de autorização")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)