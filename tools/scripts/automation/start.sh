#!/bin/bash

# Sentinela MVP - Startup Script
# This script starts all services in the correct order

set -e

echo "🚀 Starting Sentinela MVP Infrastructure..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file with default values..."
    cat > .env << EOF
# Keycloak Configuration
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin123

# Database Configuration
KEYCLOAK_DB_PASSWORD=keycloak123
POLICY_DB_PASSWORD=policy_pass

# OPAL Configuration
OPAL_AUTH_TOKEN=super-secret-token

# Application URLs
KEYCLOAK_URL=http://localhost:8080
POLICY_API_URL=http://localhost:8000
POLICY_UI_URL=http://localhost:3000
BUSINESS_API_URL=http://localhost:8001
EOF
    echo "✅ .env file created successfully!"
fi

# Start services
echo "🐳 Starting Docker containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check Keycloak
if curl -f http://localhost:8080/health/ready &> /dev/null; then
    echo "✅ Keycloak is ready"
else
    echo "❌ Keycloak is not ready"
fi

# Check Policy API
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Policy API is ready"
else
    echo "❌ Policy API is not ready"
fi

# Check OPAL Server
if curl -f http://localhost:7002/health &> /dev/null; then
    echo "✅ OPAL Server is ready"
else
    echo "❌ OPAL Server is not ready"
fi

# Check Business API
if curl -f http://localhost:8001/health &> /dev/null; then
    echo "✅ Business API is ready"
else
    echo "❌ Business API is not ready"
fi

echo ""
echo "🎉 Sentinela MVP Infrastructure is starting up!"
echo ""
echo "📋 Service URLs:"
echo "   Keycloak:        http://localhost:8080"
echo "   Policy API:      http://localhost:8000"
echo "   Policy UI:       http://localhost:3000"
echo "   OPAL Server:     http://localhost:7002"
echo "   Business API:    http://localhost:8001"
echo ""
echo "🔑 Keycloak Admin Console:"
echo "   URL:      http://localhost:8080/admin"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📊 OPAL Dashboard:"
echo "   URL:  http://localhost:8181"
echo ""
echo "🛠️  Useful Commands:"
echo "   View logs:       docker-compose logs -f [service-name]"
echo "   Stop services:   docker-compose down"
echo "   Restart service: docker-compose restart [service-name]"
echo ""