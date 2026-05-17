import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from scipy.integrate import quad

# =========================
# MÉTHODES NUMÉRIQUES
# =========================

def trapeze(f, a, b, n):
    x = np.linspace(a, b, n)
    y = f(x)
    return np.trapz(y, x)

def simpson(f, a, b, n):
    if n % 2 == 1:
        n += 1
    x = np.linspace(a, b, n)
    y = f(x)
    h = (b - a) / (n - 1)
    return h/3 * (y[0] + y[-1] +
                  4*np.sum(y[1:-1:2]) +
                  2*np.sum(y[2:-2:2]))

def gauss_legendre(f, a, b, n=5):
    x, w = np.polynomial.legendre.leggauss(n)
    x = 0.5*(x+1)*(b-a) + a
    return np.sum(w * f(x)) * 0.5*(b-a)

def monte_carlo(f, a, b, n):
    x = np.random.uniform(a, b, n)
    return (b-a) * np.mean(f(x))

# =========================
# PAGE STREAMLIT
# =========================

def integration_page():
    st.markdown("## 🔢 Intégration Numérique - Solveur PRO")

    # =========================
    # FONCTION
    # =========================
    func_type = st.selectbox(
        "Fonction à intégrer",
        ["x²", "sin(x)", "exp(-x²)", "cos(x)", "1/x"]
    )

    a = st.number_input("Borne a", value=0.0)
    b = st.number_input("Borne b", value=1.0)

    n = st.slider("Discrétisation (n)", 10, 200, 50)

    # fonction
    if func_type == "x²":
        f = lambda x: x**2
    elif func_type == "sin(x)":
        f = np.sin
    elif func_type == "exp(-x²)":
        f = lambda x: np.exp(-x**2)
    elif func_type == "cos(x)":
        f = np.cos
    else:
        f = lambda x: np.where(np.abs(x) < 1e-8, 0, 1/x)

    # =========================
    # CHOIX MÉTHODES
    # =========================
    st.markdown("### ⚙️ Méthodes à utiliser")

    use_trap = st.checkbox("Trapèze", value=True)
    use_simp = st.checkbox("Simpson", value=True)
    use_gauss = st.checkbox("Gauss-Legendre", value=True)
    use_mc = st.checkbox("Monte Carlo", value=False)

    # =========================
    # CALCUL
    # =========================
    if st.button("🚀 Calculer intégrale"):

        ref, err_ref = quad(f, a, b)

        results = []

        x = np.linspace(a, b, 500)
        y = f(x)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, name="f(x)"))

        fig.add_trace(go.Scatter(
            x=np.concatenate([x, x[::-1]]),
            y=np.concatenate([y, np.zeros_like(y)]),
            fill="toself",
            opacity=0.3,
            name="Aire"
        ))

        # =========================
        # TRAPÈZE
        # =========================
        if use_trap:
            val = trapeze(f, a, b, n)
            err = abs(ref - val)
            results.append(["Trapèze", val, err])

        # =========================
        # SIMPSON
        # =========================
        if use_simp:
            val = simpson(f, a, b, n)
            err = abs(ref - val)
            results.append(["Simpson", val, err])

        # =========================
        # GAUSS
        # =========================
        if use_gauss:
            val = gauss_legendre(f, a, b)
            err = abs(ref - val)
            results.append(["Gauss-Legendre", val, err])

        # =========================
        # MONTE CARLO
        # =========================
        if use_mc:
            val = monte_carlo(f, a, b, n*100)
            err = abs(ref - val)
            results.append(["Monte Carlo", val, err])

        # =========================
        # AFFICHAGE
        # =========================
        df = pd.DataFrame(results, columns=["Méthode", "Valeur", "Erreur absolue"])

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📊 Résultats")

        st.dataframe(df, use_container_width=True)

        # =========================
        # ANALYSE
        # =========================
        st.markdown("### 🧠 Analyse")

        best = df.loc[df["Erreur absolue"].idxmin()]

        st.success(f"""
        ✔ Meilleure méthode : {best['Méthode']}  
        ✔ Valeur approx : {best['Valeur']:.6f}  
        ✔ Erreur : {best['Erreur absolue']:.2e}  
        ✔ Référence SciPy : {ref:.6f}
        """)

        # bar error plot
        fig2 = go.Figure()
        fig2.add_bar(x=df["Méthode"], y=df["Erreur absolue"])
        fig2.update_layout(title="Erreur des méthodes", yaxis_type="log")

        st.plotly_chart(fig2, use_container_width=True)