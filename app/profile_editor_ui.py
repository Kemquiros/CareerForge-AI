import streamlit as st

def show_profile_editor():
    """
    Muestra una interfaz CRUD (Crear, Leer, Actualizar, Eliminar) completa
    para editar el perfil del usuario almacenado en st.session_state['profile'].
    """
    st.header("✍️ Editor del Perfil Profesional")
    st.caption("Aquí puedes ver, modificar y guardar la información de tu perfil. Estos datos son la base para todas las optimizaciones.")

    # --- Guardia de Entrada: Verifica si el perfil está cargado ---
    if 'profile' not in st.session_state or not st.session_state.get('profile'):
        st.warning("Perfil no cargado. Sube un CV o crea una entrada para comenzar.")
        # Opcionalmente, se puede ofrecer crear un perfil vacío aquí
        if st.button("Crear Perfil Vacío"):
            st.session_state['profile'] = {
                "full_name": "",
                "contact": {"email": "", "linkedin": "", "phone": ""},
                "base_summary": "",
                "experiences": []
            }
            st.rerun()
        return

    # Atajo para acceder al perfil en el estado de la sesión
    profile_data = st.session_state['profile']

    # --- Sección de Información General ---
    st.subheader("Información General")
    profile_data['full_name'] = st.text_input(
        "Nombre Completo", 
        value=profile_data.get('full_name', '')
    )
    
    contact_data = profile_data.setdefault('contact', {})
    contact_data['email'] = st.text_input("Email", value=contact_data.get('email', ''))
    contact_data['linkedin'] = st.text_input("LinkedIn", value=contact_data.get('linkedin', ''))
    contact_data['phone'] = st.text_input("Teléfono", value=contact_data.get('phone', ''))
    
    profile_data['base_summary'] = st.text_area(
        "Resumen Profesional Base", 
        value=profile_data.get('base_summary', ''), 
        height=150
    )

    st.markdown("---")
    
    # --- Sección de Experiencia Laboral (CRUD) ---
    st.subheader("Experiencia Laboral")
    
    # Iterar sobre una copia para poder modificar la lista original de forma segura
    for i, exp in enumerate(profile_data.get('experiences', [])):
        with st.container(border=True):
            st.markdown(f"**Experiencia {i+1}**")
            
            # Widgets para editar los detalles de la experiencia
            exp['role'] = st.text_input("Cargo", value=exp.get('role', ''), key=f"role_{i}")
            exp['company'] = st.text_input("Empresa", value=exp.get('company', ''), key=f"company_{i}")
            exp['period'] = st.text_input("Periodo", value=exp.get('period', ''), key=f"period_{i}")
            
            # Botón para eliminar esta experiencia específica
            if st.button("❌ Eliminar Experiencia", key=f"del_exp_{i}", use_container_width=True):
                profile_data['experiences'].pop(i)
                st.rerun()

            # Sub-sección para los logros de esta experiencia
            st.markdown("***Logros Clave***")
            for j, ach in enumerate(exp.get('achievements', [])):
                ach['description'] = st.text_area(
                    f"Descripción del Logro {j+1}", 
                    value=ach.get('description', ''), 
                    key=f"ach_desc_{i}_{j}"
                )
                if st.button("➖ Eliminar Logro", key=f"del_ach_{i}_{j}"):
                    exp['achievements'].pop(j)
                    st.rerun()

            if st.button("➕ Añadir Logro", key=f"add_ach_{i}"):
                if 'achievements' not in exp:
                    exp['achievements'] = []
                exp['achievements'].append({"description": "", "skills": []})
                st.rerun()

    # Botón para añadir una nueva experiencia a la lista
    if st.button("➕ Añadir Experiencia", use_container_width=True):
        if 'experiences' not in profile_data:
            profile_data['experiences'] = []
        profile_data['experiences'].append({
            "role": "", 
            "company": "", 
            "period": "", 
            "achievements": []
        })
        st.rerun()
