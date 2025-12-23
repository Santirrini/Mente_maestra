#!/bin/bash

# Script unificado para iniciar infraestructura y backend

echo "🚀 Iniciando infraestructura (Redis)..."
./scripts/start_infra.sh

echo "🌐 Iniciando servidor FastAPI..."

# Priorizar el entorno virtual si existe
if [ -f "./.venv/bin/uvicorn" ]; then
    echo "📦 Usando entorno virtual (.venv)"
    ./.venv/bin/uvicorn synapse.api.main:app --reload
else
    echo "⚠️ .venv no encontrado, usando uvicorn global"
    uvicorn synapse.api.main:app --reload
fi
