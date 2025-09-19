import os
import json
from datetime import datetime
from typing import Dict, Any, Tuple
from unidecode import unidecode

from core.chains import get_research_chain, get_generation_chain

def create_output_folder(company_name: str) -> str:
    """Crea una carpeta de salida única y segura para la aplicación."""
    safe_company_name = unidecode(company_name).replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    folder_name = f"{safe_company_name}_{date_str}"
    
    output_path = os.path.join("outputs", folder_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path

def run_full_pipeline(
    profile_data: Dict[str, Any],
    job_description: str,
    company_name: str,
    research_type: str
) -> Tuple[str, str, str, str, str]:
    """
    Ejecuta el pipeline completo: investigar, generar y guardar los resultados.
    """
    job_title = job_description.split('\n')[0].strip()

    # Módulo 1: Investigación
    print(f"Ejecutando investigación: {research_type}...")
    research_chain = get_research_chain(research_type)
    research_context = research_chain.invoke({
        "company_name": company_name,
        "job_title": job_title,
        "job_description": job_description
    })
    print("Investigación completada.")

    # Módulo 2: Generación
    print("Generando el paquete de aplicación...")
    generation_chain = get_generation_chain()
    profile_text = json.dumps(profile_data, indent=2, ensure_ascii=False)
    
    full_package_str = generation_chain.invoke({
        "profile_text": profile_text,
        "job_description": job_description,
        "research_context": research_context
    })
    print("Paquete de aplicación generado.")

    # Módulo 3: Procesamiento y Guardado (LÓGICA MEJORADA)
    print("Procesando y guardando archivos...")
    output_folder = create_output_folder(company_name)
    
    try:
        # Dividir el string una sola vez usando todos los delimitadores posibles
        parts = full_package_str.split('---CV_END---')
        cv_opt = parts[0].strip()
        
        rest_parts = parts[1].split('---CL_END---')
        cover_letter = rest_parts[0].strip()

        rest_parts = rest_parts[1].split('---IP_END---')
        interview_prep = rest_parts[0].strip()

        # Asegurarse de que no queden vacíos
        if not cv_opt and not cover_letter and not interview_prep:
            raise ValueError("Todas las secciones parseadas están vacías.")

    except (ValueError, IndexError) as e:
        print(f"Advertencia: No se pudo parsear la salida del LLM con los delimitadores. Error: {e}. Se guardará la salida cruda.")
        cv_opt = "Error: No se pudo parsear la sección del CV."
        cover_letter = "Error: No se pudo parsear la sección de la Carta de Presentación."
        interview_prep = "Error: No se pudo parsear la sección de Preparación de Entrevista."
        with open(os.path.join(output_folder, "debug_raw_output.txt"), "w", encoding='utf-8') as f:
            f.write(full_package_str)

    # Guardar cada documento en su propio archivo
    with open(os.path.join(output_folder, "Investigacion.md"), "w", encoding='utf-8') as f:
        f.write(research_context)
    with open(os.path.join(output_folder, "CV_Optimizado.md"), "w", encoding='utf-8') as f:
        f.write(cv_opt)
    with open(os.path.join(output_folder, "Carta_Presentacion.md"), "w", encoding='utf-8') as f:
        f.write(cover_letter)
    with open(os.path.join(output_folder, "Preparacion_Entrevista.md"), "w", encoding='utf-8') as f:
        f.write(interview_prep)
        
    print(f"Archivos guardados con éxito en: {output_folder}")
        
    return output_folder, cv_opt, cover_letter, interview_prep, research_context
