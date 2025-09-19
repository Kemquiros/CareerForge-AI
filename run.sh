#!/bin/bash

# Este script automatiza el proceso de arranque de la aplicación CareerForge AI.
# 1. Activa el entorno virtual de Python.
# 2. Inicia la aplicación Streamlit.

# Imprime un mensaje de bienvenida
echo "🚀 Iniciando CareerForge AI..."

# Define la ruta al activador del entorno virtual
VENV_ACTIVATE=".venv/Scripts/activate"

# Verifica si el entorno virtual existe
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "❌ Error: Entorno virtual no encontrado."
    echo "Por favor, ejecuta 'python -m venv .venv' para crearlo y 'pip install -r requirements.txt' para instalar las dependencias."
    exit 1
fi

# Activa el entorno virtual
source "$VENV_ACTIVATE"

# Informa al usuario que el entorno está activado y la app se está iniciando
echo "✅ Entorno virtual activado."
echo "🌐 Lanzando la aplicación en tu navegador..."

# Ejecuta la aplicación Streamlit
# Usamos exec para que el proceso de Streamlit reemplace al del script.
# Esto es una práctica limpia para la gestión de procesos.
exec streamlit run app/main_ui.py
