import streamlit as st
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def equ_diff_page():
    st.markdown("## 🧮 Résolution d'Équations Différentielles (PRO)")

    eq_type = st.selectbox(
        "Type d'équation",
        [
            "Décroissance exponentielle",
            "Croissance exponentielle",
            "Oscillateur harmonique",
            "Logistique (population)",
            "Système prédateur-proie"
        ]
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        y0 = st.number_input("y(0)", value=1.0)
    with col2:
        k = st.number_input("k / ω", value=0.5)
    with col3:
        tmax = st.number_input("Temps max", value=10.0)

    t = np.linspace(0, tmax, 1000)

    if st.button("🚀 Résoudre", type="primary"):

        try:

            # =========================
            # 1. DÉCROISSANCE
            # =========================
            if eq_type == "Décroissance exponentielle":

                def model(y, t):
                    return -k * y

                y = odeint(model, y0, t).flatten()
                y_exact = y0 * np.exp(-k * t)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t, y=y, name="Numérique"))
                fig.add_trace(go.Scatter(x=t, y=y_exact, name="Analytique", line=dict(dash="dash")))

                fig.update_layout(title="Décroissance exponentielle", height=500)
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 2. CROISSANCE
            # =========================
            elif eq_type == "Croissance exponentielle":

                def model(y, t):
                    return k * y

                y = odeint(model, y0, t).flatten()
                y_exact = y0 * np.exp(k * t)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t, y=y, name="Numérique"))
                fig.add_trace(go.Scatter(x=t, y=y_exact, name="Analytique", line=dict(dash="dash")))

                fig.update_layout(title="Croissance exponentielle", height=500)
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 3. OSCILLATEUR
            # =========================
            elif eq_type == "Oscillateur harmonique":

                def model(Y, t):
                    y1, y2 = Y
                    return [y2, -k**2 * y1]

                Y0 = [y0, 0]
                sol = odeint(model, Y0, t)

                y = sol[:, 0]
                v = sol[:, 1]

                fig = make_subplots(rows=2, cols=1,
                                    subplot_titles=("Position", "Vitesse"))

                fig.add_trace(go.Scatter(x=t, y=y, name="y(t)"), row=1, col=1)
                fig.add_trace(go.Scatter(x=t, y=v, name="v(t)"), row=2, col=1)

                fig.update_layout(height=600, title="Oscillateur harmonique")
                st.plotly_chart(fig, use_container_width=True)

                # phase
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=v, y=y, mode="lines"))
                fig2.update_layout(title="Portrait de phase", xaxis_title="v", yaxis_title="y")
                st.plotly_chart(fig2, use_container_width=True)

            # =========================
            # 4. LOGISTIQUE
            # =========================
            elif eq_type == "Logistique (population)":

                M = 10

                def model(y, t):
                    return k * y * (1 - y / M)

                y = odeint(model, y0, t).flatten()

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t, y=y, name="Population"))

                fig.update_layout(title="Modèle logistique", height=500)
                st.plotly_chart(fig, use_container_width=True)

                st.info(f"Capacité limite M = {M}")

            # =========================
            # 5. LOTKA-VOLTERRA
            # =========================
            elif eq_type == "Système prédateur-proie":

                a, b, c, d = 1.0, 0.1, 0.075, 1.5

                def model(Y, t):
                    x, y = Y
                    dx = a*x - b*x*y
                    dy = -c*y + d*b*x*y
                    return [dx, dy]

                Y0 = [y0, 1.0]
                sol = odeint(model, Y0, t)

                x = sol[:, 0]
                y = sol[:, 1]

                fig = make_subplots(rows=2, cols=1,
                                    subplot_titles=("Proies", "Prédateurs"))

                fig.add_trace(go.Scatter(x=t, y=x), row=1, col=1)
                fig.add_trace(go.Scatter(x=t, y=y), row=2, col=1)

                fig.update_layout(height=600, title="Lotka-Volterra")
                st.plotly_chart(fig, use_container_width=True)

                # phase
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=x, y=y))
                fig2.update_layout(title="Phase proie-prédateur",
                                   xaxis_title="Proies",
                                   yaxis_title="Prédateurs")
                st.plotly_chart(fig2, use_container_width=True)

            # =========================
            # ANALYSE GLOBALE
            # =========================
            st.success("Simulation terminée ✔")

            col1, col2, col3 = st.columns(3)
            col1.metric("y final", f"{y[-1]:.4f}")
            col2.metric("max y", f"{np.max(y):.4f}")
            col3.metric("min y", f"{np.min(y):.4f}")

        except Exception as e:
            st.error(f"Erreur : {e}")

    # =========================
    # INFO
    # =========================
    with st.expander("📖 Infos scientifiques"):
        st.markdown("""
        - Euler / odeint (LSODA adaptatif)
        - Oscillateur → solution analytique sin/cos
        - Logistique → saturation naturelle
        - Lotka-Volterra → cycle non linéaire
        """)

# lancement
equ_diff_page()