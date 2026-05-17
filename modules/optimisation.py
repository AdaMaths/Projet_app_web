import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize

def optimisation_page():
    st.title("🎯 Optimisation")

    choice = st.selectbox("Fonction", ["Quadratique", "Sinus"])

    if choice == "Quadratique":
        a = st.slider("a", -5.0, 5.0, 1.0)
        b = st.slider("b", -5.0, 5.0, 0.0)
        c = st.slider("c", -5.0, 5.0, 0.0)
        func = lambda x: a*x**2 + b*x + c

    else:
        func = lambda x: np.sin(x)

    x = np.linspace(-10, 10, 500)
    y = func(x)

    res = minimize(func, x0=0)
    x_opt = res.x[0]
    y_opt = func(x_opt)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))
    fig.add_trace(go.Scatter(x=[x_opt], y=[y_opt], mode="markers"))

    st.plotly_chart(fig)

    st.success(f"Minimum: x={x_opt:.3f}, f(x)={y_opt:.3f}")