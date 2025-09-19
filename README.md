# CareerForge AI 🔥

*Tu Co-piloto de Carrera Potenciado por IA para Forjar tu Futuro Profesional.*

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-estable-brightgreen.svg)

---

**CareerForge AI** es una herramienta estratégica que transforma tu perfil profesional y una oferta de trabajo en un paquete de aplicación completo y personalizado (CV, Carta de Presentación, Preparación de Entrevista), aumentando drásticamente tus probabilidades de conseguir una entrevista.

## ✨ Características Principales

* **Perfil Profesional Dinámico:** Analiza tu CV con IA para crear un perfil profesional estructurado.
* **Editor de Perfil (CRUD):** Modifica tu perfil desde una interfaz gráfica intuitiva, almacenado en una base de datos local SQLite.
* **Inteligencia Estratégica:** Elige entre un **Análisis de la Empresa** o una **Estimación Salarial** para cada aplicación.
* **Generación de Paquete Completo:** Obtén un CV optimizado, una carta de presentación personalizada y una guía de entrevista.
* **Mínima Configuración:** Solo necesitas una clave de API de Google Gemini.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para tener CareerForge AI funcionando en tu máquina.

### Prerrequisitos

* **Python 3.9+**
* **Git**
* **Clave de API de Google Gemini:** Obtenla en [Google AI Studio](https://aistudio.google.com/).

### Pasos de Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/kemquiros/careerforge-ai.git](https://github.com/tu-usuario/careerforge-ai.git)
    cd careerforge-ai
    ```

2.  **Crear y Activar un Entorno Virtual (`venv`):**
    ```bash
    # Crear el entorno
    python -m venv .venv
    
    # Activar en macOS / Linux
    source .venv/bin/activate
    
    # Activar en Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```
    > ✨ Verás `(venv)` al principio de la línea de tu terminal si la activación fue exitosa.

3.  **Instalar las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de la Clave de API

1.  **Crear tu archivo `.env`:**
    Este proyecto usa un archivo de plantilla llamado `.env.template` para gestionar las claves de API. **Copia este archivo** para crear tu propio archivo de configuración local `.env`.

    * **En macOS / Linux:**
        ```bash
        cp .env.template .env
        ```
    * **En Windows:**
        ```bash
        copy .env.template .env
        ```

2.  **Añadir tu Clave de API:**
    Abre el nuevo archivo `.env` que acabas de crear y pega tu clave de API de Google Gemini donde se indica.
    ```env
    GOOGLE_API_KEY="TU_API_KEY_DE_GEMINI_VA_AQUI"
    ```
    > ⚠️ **Importante:** El archivo `.env` está incluido en `.gitignore` y nunca debe ser compartido ni subido a un repositorio.

---

## ▶️ Cómo Usar la Aplicación

1.  **Ejecutar la Aplicación:**
    Asegúrate de que tu entorno virtual (`venv`) esté activado y, desde la carpeta raíz del proyecto, ejecuta el siguiente comando:
    ```bash
    streamlit run app/main_ui.py
    ```
    La aplicación se abrirá automáticamente en una nueva pestaña de tu navegador web.

2.  **Flujo de Trabajo:**
    * **Carga tu Perfil:** Usa la barra lateral para subir tu CV y poblar tu perfil profesional.
    * **Introduce la Oferta:** En el área principal, pega los detalles de la oferta de trabajo.
    * **Elige tu Estrategia:** Selecciona si quieres investigar la empresa o el salario.
    * **Forja tu Aplicación:** Haz clic en el botón principal y observa cómo la IA crea tu paquete de aplicación.

---

## 📄 Licencia

Este proyecto está distribuido bajo la Licencia MIT. Es una licencia permisiva que te permite hacer casi cualquier cosa con el código, siempre y cuando incluyas el aviso de derechos de autor original.

<details>
<summary><strong>Consulta el archivo `LICENSE` para más detalles.</strong></summary>
</details>