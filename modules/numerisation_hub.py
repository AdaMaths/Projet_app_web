import streamlit as st

def numerisation_hub_page():

    st.title("🔢 Hub de Numérisation Scientifique")

    st.markdown("""
    ### Modules disponibles
    Choisissez un domaine scientifique :
    """)

    col1, col2, col3 = st.columns(3)

    modules = [
        ("⚙️ Optimisation", col1),
        ("🤖 Automatique", col1),
        ("📈 Intégration", col2),
        ("🔄 Interpolation", col2),
        ("📐 Éq. Diff", col3),
        ("📡 Signal", col3),
    ]

    for module_name, column in modules:
        with column:
            if st.button(module_name, use_container_width=True):
                st.session_state["page"] = module_name
                st.rerun()

    st.markdown("---")

    st.info("""
    Ce hub centralise :
    - les méthodes numériques,
    - les calculs scientifiques,
    - les outils d'analyse,
    - les simulations physiques.
    """)