import streamlit as st
import sys
import os
import json
from dotenv import load_dotenv

# Añadir el directorio raíz al path y cargar .env
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from database.database_manager import db_manager
from core.profile_parser import parse_cv_to_profile
from core.orchestrator import run_full_pipeline
from core.pdf_processor import convert_pdf_to_markdown
from app.profile_editor_ui import show_profile_editor

st.set_page_config(page_title="CareerForge AI - Final", layout="wide")
st.image("https://www.gstatic.com/lamda/images/gemini/google_gemini_lockup_white_2x_web_pLPMff.png", width=200)
st.title("🔥 CareerForge AI: Tu Co-piloto de Carrera")

# Inicialización del Perfil
if 'profile' not in st.session_state:
    st.session_state['profile'] = db_manager.load_profile() or {}

# BARRA LATERAL
with st.sidebar:
    st.header("👤 Gestión de Perfil")
    
    st.subheader("Opción 1: Cargar Perfil desde PDF (Recomendado)")
    uploaded_pdf = st.file_uploader(
        "Sube tu CV en PDF y la IA lo analizará y estructurará.",
        type=["pdf"]
    )
    if uploaded_pdf:
        if st.button("Procesar PDF con IA"):
            with st.spinner("Leyendo PDF y contactando a la IA... Este proceso puede tardar un momento."):
                # Paso 1: Convertir PDF a Markdown
                markdown_cv = convert_pdf_to_markdown(uploaded_pdf)
                
                if not markdown_cv:
                    st.error("No se pudo extraer contenido del PDF.")
                else:
                    # Paso 2: Usar el Markdown para poblar el perfil estructurado
                    st.info("PDF convertido a texto. Ahora extrayendo la estructura del perfil...")
                    parsed_data = parse_cv_to_profile(markdown_cv)
                    if parsed_data:
                        st.session_state['profile'] = parsed_data
                        db_manager.save_profile(parsed_data)
                        st.success("¡Perfil actualizado desde el PDF con éxito!")
                        st.rerun() # Recarga la app para que el editor muestre los datos
                    else:
                        st.error("No se pudo procesar la estructura del CV desde el texto convertido.")

    st.markdown("---")

    st.subheader("Opción 2: Cargar Perfil desde Texto (.txt, .md)")
    uploaded_text_cv = st.file_uploader(
        "Sube tu CV en formato de texto.",
        type=["txt", "md"]
    )
    if uploaded_text_cv:
        if st.button("Analizar archivo de texto"):
            with st.spinner("IA analizando tu CV..."):
                cv_text = uploaded_text_cv.read().decode("utf-8")
                parsed_data = parse_cv_to_profile(cv_text)
                if parsed_data:
                    st.session_state['profile'] = parsed_data
                    db_manager.save_profile(parsed_data)
                    st.success("¡Perfil actualizado desde el archivo de texto!")
                    st.rerun()
                else:
                    st.error("No se pudo procesar el archivo de texto.")
    
    st.markdown("---")

    with st.expander("Editar Perfil Manualmente"):
        show_profile_editor()
        if st.button("💾 Guardar Cambios en Perfil", type="primary"):
            db_manager.save_profile(st.session_state['profile'])
            st.success("¡Perfil guardado en la base de datos!")

# ÁREA PRINCIPAL
col1, col2 = st.columns([0.45, 0.55])

with col1:
    st.header("🎯 La Oportunidad")
    company_name = st.text_input("Nombre de la Empresa", placeholder="Ej: Google")
    job_description = st.text_area("Pega la Descripción de la Oferta Laboral", height=300)
    
    st.subheader("🧠 Tipo de Inteligencia Estratégica")
    research_type = st.radio(
        "Elige qué investigar sobre esta oportunidad:",
        ["Análisis de la Empresa", "Estimación Salarial", "Ninguna"],
        horizontal=True, key="research_choice"
    )

if st.button("Forjar Paquete de Aplicación", type="primary", use_container_width=True):
    if not st.session_state.get('profile'):
        st.error("Tu perfil está vacío. Sube un CV o edítalo manualmente primero.")
    elif not company_name or not job_description:
        st.warning("Por favor, completa el nombre de la empresa y la descripción de la oferta.")
    else:
        with st.spinner("🔥 Forjando tu futuro... La IA está trabajando intensamente..."):
            try:
                output_folder, cv_opt, cover_letter, interview_prep, research_context = run_full_pipeline(
                    profile_data=st.session_state['profile'],
                    job_description=job_description,
                    company_name=company_name,
                    research_type=research_type
                )
                st.success(f"¡Paquete generado con éxito en la carpeta: `{output_folder}`!")
                
                # Guardar resultados en el estado de la sesión para mostrarlos
                st.session_state['results'] = {
                    "cv": cv_opt, "cl": cover_letter, "ip": interview_prep, "rc": research_context
                }
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

# Mostrar resultados
if 'results' in st.session_state:
    with col2:
        st.header("📄 Tus Activos Generados")
        results = st.session_state['results']
        
        if results['rc'] != "No se seleccionó ninguna investigación.":
            with st.expander("🧠 Inteligencia Estratégica", expanded=True):
                st.markdown(results['rc'])
        
        with st.expander("📄 CV Optimizado"):
            st.markdown(results['cv'])
        with st.expander("✉️ Carta de Presentación"):
            st.markdown(results['cl'])
        with st.expander("🎙️ Preparación de Entrevista"):
            st.markdown(results['ip'])
else:
    with col2:
        st.info("Ingresa los datos de la oportunidad y haz clic en 'Forjar' para ver los resultados aquí.")
