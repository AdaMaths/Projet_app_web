import streamlit as st
import numpy as np
from scipy import signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def automatique_page():
    st.markdown("## 🤖 Analyse de Systèmes Automatiques")
    
    # Sélecteur de système (identique PyQt5)
    system_type = st.selectbox(
        "Type de système",
        [
            "Premier ordre: H(s) = K/(τs+1)",
            "Second ordre: H(s) = ωn²/(s²+2ζωns+ωn²)", 
            "Intégrateur: H(s) = K/s",
            "Dérivateur: H(s) = K*s"
        ]
    )
    
    # Paramètres (3 sliders adaptatifs)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        param1 = st.number_input("**Param 1**", value=1.0, step=0.1, format="%.2f")
    with col2:
        param2 = st.number_input("**Param 2**", value=1.0, step=0.1, format="%.2f")
    with col3:
        param3 = st.number_input("**Param 3**", value=0.5, step=0.1, format="%.2f")
    
    # Labels adaptatifs selon système
    if "Premier ordre" in system_type:
        st.info(f"**K** = {param1}, **τ** = {param2}")
        num, den = [param1], [param2, 1]
    elif "Second ordre" in system_type:
        st.info(f"**ωn** = {param1}, **ζ** = {param2}")
        num, den = [param1**2], [1, 2*param2*param1, param1**2]
    elif "Intégrateur" in system_type:
        st.info(f"**K** = {param1}")
        num, den = [param1], [1, 0]
    else:  # Dérivateur
        st.info(f"**K** = {param1}")
        num, den = [param1, 0], [1]
    
    # Analyse type
    analysis_type = st.radio("Type d'analyse", ["📈 Réponse indicielle", "📊 Diagramme de Bode"], horizontal=True)
    
    # === RÉPONSE INDICIELLE ===
    if analysis_type == "📈 Réponse indicielle":
        try:
            sys = signal.TransferFunction(num, den)
            t, y = signal.step(sys, T=np.linspace(0, 10, 1000))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=y, mode='lines', 
                                   name='Réponse', line=dict(width=3, color='#1f77b4')))
            
            # Valeur finale
            final_value = y[-1] if not np.isnan(y[-1]) else "instable"
            fig.add_hline(y=final_value, line_dash="dash", 
                         annotation_text=f"Valeur finale: {final_value:.3f}")
            
            fig.update_layout(
                title="Réponse Indicielle",
                xaxis_title="Temps (s)",
                yaxis_title="Amplitude",
                height=500,
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"**Valeur finale** : {final_value:.3f}")
            
        except Exception as e:
            st.error(f"Erreur calcul : {e}")
    
    # === DIAGRAMME DE BODE ===
    elif analysis_type == "📊 Diagramme de Bode":
        try:
            sys = signal.TransferFunction(num, den)
            w, mag, phase = signal.bode(sys, 100)
            
            # Subplot Plotly (équivalent matplotlib subplot)
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Magnitude (dB)', 'Phase (deg)'),
                vertical_spacing=0.1
            )
            
            fig.add_trace(
                go.Scatter(x=w, y=mag, mode='lines', name='Magnitude',
                         line=dict(color='#ff7f0e')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=w, y=phase, mode='lines', name='Phase',
                         line=dict(color='#2ca02c')),
                row=2, col=1
            )
            
            fig.update_xaxes(type="log", row=2, col=1)
            fig.update_layout(
                title="Diagramme de Bode",
                height=600,
                template='plotly_white'
            )
            fig.update_yaxes(title_text="Magnitude (dB)", row=1, col=1)
            fig.update_yaxes(title_text="Phase (deg)", row=2, col=1)
            fig.update_xaxes(title_text="Fréquence (rad/s)", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            st.success("Diagramme de Bode calculé avec succès !")
            
        except Exception as e:
            st.error(f"Erreur Bode : {e}")
    
    # Contrôles supplémentaires
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Recalculer", type="secondary"):
            st.rerun()
    
    with col2:
        time_max = st.slider("Temps max (s)", 5.0, 50.0, 10.0)
    
    # Aide
    with st.expander("📖 Documentation"):
        st.markdown("""
        ### Systèmes supportés :
        - **1er ordre** : K/(τs+1) → Temps constant τ
        - **2nd ordre** : ωn²/(s²+2ζωns+ωn²) → Pulsation ωn, amortissement ζ
        - **Intégrateur** : K/s → Accumulation
        - **Dérivateur** : K⋅s → Prédiction
        
        **Réponse indicielle** : Réaction à échelon unitaire  
        **Bode** : Gain/Phase vs fréquence log
        """)