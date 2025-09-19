from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import Runnable

def get_research_chain(research_type: str) -> Runnable:
    """
    Crea dinámicamente una cadena para investigación de empresas o salarios
    utilizando el conocimiento interno del LLM.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
    
    if research_type == "Análisis de la Empresa":
        prompt_text = """
        Actúa como un analista de negocios experto. Basado en tu conocimiento interno,
        proporciona un resumen conciso y estratégico sobre la empresa '{company_name}'.
        Cubre los siguientes puntos en formato Markdown:
        - **Productos/Servicios Principales:** ¿Qué hacen y para quién?
        - **Cultura y Valores:** ¿Cómo es trabajar allí? (innovadora, tradicional, etc.)
        - **Posición en el Mercado:** ¿Quiénes son sus principales competidores?
        - **Puntos Clave para el Candidato:** ¿Qué aspecto de la empresa debería un candidato resaltar en su aplicación?
        
        Empresa: {company_name}
        Rol de interés: {job_title}
        """
    elif research_type == "Estimación Salarial":
        prompt_text = """
        Actúa como un consultor de compensación y reclutador senior de TI.
        Basado en tu conocimiento del mercado, proporciona una estimación salarial
        para el rol de '{job_title}' en '{company_name}' o una empresa de nivel similar.
        Usa la descripción de la oferta para inferir la seniority y la ubicación.
        Presenta la información en formato Markdown:
        - **Rango Salarial Estimado (USD Anual):** Proporciona un rango probable (ej. $120,000 - $150,000 USD).
        - **Factores Clave que Afectan el Salario:** ¿Qué habilidades o experiencias de la oferta justifican estar en la parte alta del rango?
        - **Notas sobre el Mercado:** ¿Hay alta demanda para este rol? ¿Es competitivo?

        Empresa: {company_name}
        Rol de interés: {job_title}
        Descripción de la oferta: {job_description}
        """
    else:
        return Runnable.from_callable(lambda x: "No se seleccionó ninguna investigación.")

    prompt = PromptTemplate.from_template(prompt_text)
    return prompt | llm | StrOutputParser()

def get_generation_chain() -> Runnable:
    """Crea la cadena principal que genera el paquete de aplicación."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.6)
    prompt_text = """
    Eres CareerForge AI, un coach de carrera experto. Tu tarea es generar un paquete de aplicación
    completo y 'spotless' usando el contexto proporcionado.
    Genera el contenido para cada una de las 3 secciones solicitadas y sepáralas
    con los delimitadores exactos. No incluyas los títulos como 'SECCIÓN 1'.

    **CONTEXTO PROPORCIONADO:**
    1.  **Perfil del Candidato:** {profile_text}
    2.  **Oferta Laboral:** {job_description}
    3.  **Investigación Estratégica:** {research_context}

    **INSTRUCCIONES:**

    **1. Primero, genera el contenido del CV OPTIMIZADO:**
    Revisa el perfil del candidato y adáptalo a la oferta. Enfócate en reescribir los logros de la experiencia
    laboral para que resuenen con los requisitos de la oferta, usando el método STAR (Situación, Tarea, Acción, Resultado)
    y cuantificando el impacto. Crea un resumen profesional potente y directo.
    ---CV_END---

    **2. Segundo, genera el contenido de la CARTA DE PRESENTACIÓN:**
    Escribe una carta de presentación concisa y persuasiva. Usa la 'Investigación Estratégica' para personalizar
    el primer párrafo y demostrar un interés genuino. En el segundo párrafo, conecta 2-3 logros clave
    del perfil directamente con las necesidades de la oferta.
    ---CL_END---

    **3. Tercero, genera el contenido de la PREPARACIÓN PARA LA ENTREVISTA:**
    Basado en la oferta y el perfil, genera:
    - Una lista de 3 posibles preguntas de comportamiento o técnicas que probablemente le harán al candidato.
    - Una lista de 3 preguntas inteligentes que el candidato puede hacer para demostrar su interés y senior-level.
    ---IP_END---
    """
    prompt = PromptTemplate.from_template(prompt_text)
    return prompt | llm | StrOutputParser()
