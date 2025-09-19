# -*- coding: utf-8 -*-

"""
Módulo responsable de convertir el texto no estructurado de un CV
en un objeto de perfil de usuario estructurado y validado usando Pydantic y LangChain.
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI

# ----------------------------------------------------------------------------
# 1. DEFINICIÓN DE LOS MODELOS DE DATOS (EL ESQUEMA)
# Usamos Pydantic para definir la estructura de datos deseada.
# Todos los campos son 'Optional' para hacer el parser robusto a información faltante.
# ----------------------------------------------------------------------------

class Contact(BaseModel):
    """Modelo para la información de contacto del usuario."""
    email: Optional[str] = Field(default=None, description="Email del usuario (opcional)")
    linkedin: Optional[str] = Field(default=None, description="URL del perfil de LinkedIn (opcional)")
    phone: Optional[str] = Field(default=None, description="Número de teléfono (opcional)")

class Achievement(BaseModel):
    """Modelo para un logro específico dentro de una experiencia laboral."""
    description: Optional[str] = Field(default=None, description="Descripción de un logro (opcional).")
    skills: Optional[List[str]] = Field(default=None, description="Lista de habilidades usadas (opcional).")

class Experience(BaseModel):
    """Modelo para una experiencia laboral completa."""
    role: Optional[str] = Field(default=None, description="Cargo o rol desempeñado (opcional).")
    company: Optional[str] = Field(default=None, description="Nombre de la empresa (opcional).")
    period: Optional[str] = Field(default=None, description="Periodo de tiempo en el puesto (opcional).")
    achievements: Optional[List[Achievement]] = Field(default=None, description="Lista de logros (opcional).")

class UserProfile(BaseModel):
    """Modelo raíz que representa el perfil completo y estructurado del usuario."""
    full_name: Optional[str] = Field(default=None, description="Nombre completo del usuario (opcional).")
    contact: Optional[Contact] = Field(default=None, description="Información de contacto (opcional).")
    base_summary: Optional[str] = Field(default=None, description="Resumen profesional (opcional).")
    experiences: Optional[List[Experience]] = Field(default=None, description="Lista de experiencias laborales (opcional).")
    skills_inventory: Optional[Dict[str, List[str]]] = Field(default=None, description="Diccionario de habilidades (opcional).")


# ----------------------------------------------------------------------------
# 2. LÓGICA DE LA CADENA DE IA
# Funciones que ensamblan y ejecutan la cadena de LangChain para el parsing.
# ----------------------------------------------------------------------------

def get_cv_parser_chain() -> any:
    """
    Construye y devuelve una cadena de LangChain que toma texto y devuelve un objeto UserProfile.
    """
    parser = PydanticOutputParser(pydantic_object=UserProfile)

    prompt = PromptTemplate(
        template="""
        Analiza el siguiente texto de un CV y extráelo a la estructura JSON solicitada.
        Eres un experto en reclutamiento, por lo que debes ser muy preciso.
        Si no encuentras información para un campo específico, omítelo o establece su valor en null. No inventes información.

        {format_instructions}

        CV TEXT:
        ---
        {cv_text}
        ---
        """,
        input_variables=["cv_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.0)

    return prompt | llm | parser

def parse_cv_to_profile(cv_text: str) -> Optional[Dict]:
    """
    Función de interfaz pública que toma el texto de un CV y devuelve un diccionario estructurado.

    Args:
        cv_text: El contenido de texto en bruto de un CV.

    Returns:
        Un diccionario con la estructura de UserProfile, o None si ocurre un error.
    """
    if not cv_text or not cv_text.strip():
        print("Advertencia: Se intentó parsear un texto de CV vacío.")
        return None
        
    try:
        parser_chain = get_cv_parser_chain()
        parsed_profile = parser_chain.invoke({"cv_text": cv_text})
        return parsed_profile.dict()
    except Exception as e:
        # Captura cualquier error durante el parsing y lo reporta, evitando que la app falle.
        print(f"Error al parsear el CV: {e}")
        return None
