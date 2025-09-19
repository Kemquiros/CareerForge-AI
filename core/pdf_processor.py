import fitz  # PyMuPDF
import google.generativeai as genai
from typing import IO

def extract_text_from_pdf_buffer(pdf_buffer: IO[bytes]) -> str:
    """
    Extrae texto de un búfer de bytes de PDF (proporcionado por st.file_uploader).
    """
    try:
        # PyMuPDF puede abrir directamente desde un stream de bytes
        document = fitz.open(stream=pdf_buffer.read(), filetype="pdf")
        full_text = ""
        for page in document:
            full_text += page.get_text("text") + "\n"
        return full_text
    except Exception as e:
        print(f"Error al procesar el búfer del PDF: {e}")
        return ""

def structure_text_as_markdown(raw_text: str) -> str:
    """
    Utiliza el modelo Gemini para convertir un bloque de texto en bruto a formato Markdown.
    """
    print("🤖 Contactando a la IA para estructurar el documento...")
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    prompt = f"""
    Eres un asistente experto en formateo de documentos. Convierte el siguiente texto,
    extraído de un CV, a un formato Markdown limpio y profesional.
    Identifica secciones (Experiencia, Educación, etc.) como encabezados (`##`),
    usa viñetas (`-`) para listas, y negritas (`**`) para cargos y empresas.
    Elimina cualquier artefacto de la extracción.

    TEXTO EN BRUTO A CONVERTIR:
    ---
    {raw_text}
    ---
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error al comunicarse con la API de Gemini: {e}")
        return "# Error en la conversión\n\nNo se pudo formatear el texto."

def convert_pdf_to_markdown(pdf_file: IO[bytes]) -> str:
    """
    Orquesta el proceso completo de conversión de un PDF en memoria a Markdown.
    """
    raw_text = extract_text_from_pdf_buffer(pdf_file)
    if not raw_text.strip():
        return ""
    
    markdown_text = structure_text_as_markdown(raw_text)
    return markdown_text
