import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import interp1d, CubicSpline
from numpy.polynomial.polynomial import Polynomial
import pandas as pd

def interpolation_page():
    st.markdown("## 🔗 Interpolation de Données")
    
    # Sélecteur méthode (identique PyQt5)
    method = st.selectbox(
        "Méthode d'interpolation",
        [
            "Linéaire", "Cubique (Spline)", "Lagrange", 
            "Nearest (Plus proche)", "Polynôme ordre N"
        ]
    )
    
    # === SAISIE DONNÉES (comme PyQt5) ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Points de données**")
        x_data_str = st.text_input("**x** (séparés par virgule)", "0,1,2,3,4")
        y_data_str = st.text_input("**y**", "0,1,4,9,16")
        
        # Parsing
        try:
            x_data = np.array([float(xi.strip()) for xi in x_data_str.split(',')])
            y_data = np.array([float(yi.strip()) for yi in y_data_str.split(',')])
            
            if len(x_data) != len(y_data):
                st.error("❌ x et y doivent avoir la même taille")
                st.stop()
                
            st.success(f"✓ **{len(x_data)} points** chargés")
            
        except:
            st.error("❌ Format invalide (utilisez: 0,1,2,3)")
            st.stop()
    
    # Paramètres avancés
    col1, col2 = st.columns(2)
    with col1:
        n_points = st.slider("**Points interpolés**", 50, 500, 300)
        x_min, x_max = x_data.min(), x_data.max()
    
    with col2:
        if method == "Polynôme ordre N":
            poly_order = st.slider("**Ordre polynôme**", 1, min(10, len(x_data)-1), 3)
    
    # Calcul interpolation
    x_interp = np.linspace(x_min, x_max, n_points)
    
    try:
        if method == "Linéaire":
            f = interp1d(x_data, y_data, kind='linear', fill_value="extrapolate")
            y_interp = f(x_interp)
            title = "Interpolation linéaire"
        
        elif method == "Cubique (Spline)":
            f = CubicSpline(x_data, y_data)
            y_interp = f(x_interp)
            title = "Spline cubique C²"
        
        elif method == "Lagrange":
            # Polynôme de Lagrange
            p = Polynomial.fit(x_data, y_data, deg=len(x_data)-1)
            y_interp = p(x_interp)
            title = f"Polynôme de Lagrange (degré {len(x_data)-1})"
        
        elif method == "Nearest (Plus proche)":
            f = interp1d(x_data, y_data, kind='nearest', fill_value="extrapolate")
            y_interp = f(x_interp)
            title = "Plus proche voisin"
        
        else:  # Polynôme ordre N
            p = Polynomial.fit(x_data, y_data, deg=poly_order)
            y_interp = p(x_interp)
            title = f"Polynôme degré {poly_order}"
    
    except Exception as e:
        st.error(f"❌ Erreur calcul: {e}")
        st.stop()
    
    # === GRAPHIQUE IDENTIQUE PyQt5 ===
    fig = go.Figure()
    
    # Points originaux (cercles rouges)
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers',
                           marker=dict(size=12, color='red', symbol='circle'),
                           name='Points donnés', line=dict(width=2)))
    
    # Courbe interpolée (ligne bleue)
    fig.add_trace(go.Scatter(x=x_interp, y=y_interp, mode='lines',
                           line=dict(color='#1f77b4', width=4),
                           name='Interpolation'))
    
    fig.update_layout(
        title=title,
        xaxis_title="x", yaxis_title="y",
        height=500, template='plotly_white',
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # === RÉSULTATS ===
    st.markdown("### 📋 Résultats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("**Points originaux**", len(x_data))
    with col2:
        st.metric("**Points interpolés**", n_points)
    with col3:
        st.metric("**Intervalle**", f"[{x_min:.2f}, {x_max:.2f}]")
    
    # Tableau précision
    errors = np.abs(y_data - np.interp(x_data, x_interp, y_interp))
    st.metric("**Erreur max**", f"{np.max(errors):.4f}")
    
    # === ANALYSE ERREUR ===
    st.markdown("### 📊 Analyse d'erreur")
    fig_error = go.Figure()
    fig_error.add_trace(go.Scatter(x=x_data, y=errors, mode='markers+lines',
                                 marker=dict(color='orange', size=8),
                                 line=dict(color='orange', width=2),
                                 name='Erreur absolue'))
    fig_error.update_layout(title="Erreur d'interpolation |y - y_interp|",
                          height=300)
    st.plotly_chart(fig_error, use_container_width=True)
    
    # === EXEMPLES PRÉDÉFINIS ===
    st.markdown("---")
    example_data = {
        "Parabole": ("0,1,2,3,4", "0,1,4,9,16"),
        "Sinus": ("0,0.5,1,1.5,2", "0,0.48,0.84,0.997,0.909"),
        "Bruit": ("0,1,2,3,4", "1.1,2.0,3.9,9.2,15.8")
    }
    
    selected_example = st.selectbox("📈 Exemple rapide", list(example_data.keys()))
    if st.button("🔥 Charger exemple"):
        x_str, y_str = example_data[selected_example]
        st.session_state.x_str = x_str
        st.session_state.y_str = y_str
        st.rerun()
    
    # Sauvegarde
    df_interp = pd.DataFrame({'x': x_interp, 'y_interp': y_interp})
    csv = df_interp.to_csv(index=False).encode()
    st.download_button("💾 Exporter CSV", csv, "interpolation.csv", "text/csv")
    
    # Aide
    with st.expander("📖 Théorie"):
        st.markdown("""
        **Linéaire** : Segments droits (simple, stable)  
        **Spline cubique** : C² continue (lisse, naturel)  
        **Lagrange** : Polynôme exact aux points (oscille Runge)  
        **Nearest** : Escaliers (classification)
        
        **Spline > Linéaire** pour données lisses
        """)

# Persistance exemples
if 'x_str' in st.session_state:
    st.text_input("x", value=st.session_state.x_str, key="persistent_x")
    st.text_input("y", value=st.session_state.y_str, key="persistent_y")