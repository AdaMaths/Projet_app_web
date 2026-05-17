import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# =========================
# 🔬 OBSTACLE (CYLINDRE)
# =========================
def build_obstacle(nx, ny):
    cx, cy = nx // 4, ny // 2
    r = min(nx, ny) // 10

    obs = np.zeros((ny, nx))
    for i in range(ny):
        for j in range(nx):
            if (j - cx)**2 + (i - cy)**2 < r**2:
                obs[i, j] = 1
    return obs


# =========================
# 🌊 LAPLACIEN
# =========================
def laplacian(f):
    return (
        np.roll(f, 1, axis=0) +
        np.roll(f, -1, axis=0) +
        np.roll(f, 1, axis=1) +
        np.roll(f, -1, axis=1) -
        4 * f
    )


# =========================
# 🔬 NAVIER-STOKES STEP
# =========================
def step(u, v, p, nu, dt, obstacle):

    # gradients
    du_dx = np.gradient(u, axis=1)
    du_dy = np.gradient(u, axis=0)
    dv_dx = np.gradient(v, axis=1)
    dv_dy = np.gradient(v, axis=0)

    # convection
    u_conv = u - dt * (u * du_dx + v * du_dy)
    v_conv = v - dt * (u * dv_dx + v * dv_dy)

    # diffusion (viscosité)
    u_star = u_conv + nu * laplacian(u) * dt
    v_star = v_conv + nu * laplacian(v) * dt

    # pression (Poisson simplifié)
    div = np.gradient(u_star, axis=1) + np.gradient(v_star, axis=0)

    p = 0.25 * (
        np.roll(p, 1, axis=0) +
        np.roll(p, -1, axis=0) +
        np.roll(p, 1, axis=1) +
        np.roll(p, -1, axis=1) -
        div
    )

    # projection
    u = u_star - np.gradient(p, axis=1)
    v = v_star - np.gradient(p, axis=0)

    # obstacle (no slip)
    u[obstacle == 1] = 0
    v[obstacle == 1] = 0

    return u, v, p


# =========================
# 🤖 IA SIMPLE (PRÉDICTION)
# =========================
def predict(history):
    return np.mean(history[-5:], axis=0)


# =========================
# 🚀 STREAMLIT APP
# =========================
def navier_stokes_page():

    st.title("🌊 Navier–Stokes CFD (vortex + IA)")

    # ================= PARAMS =================
    col1, col2, col3 = st.columns(3)

    with col1:
        nx = st.slider("Grid X", 30, 100, 60)
        ny = st.slider("Grid Y", 30, 100, 60)

    with col2:
        nu = st.slider("Viscosité ν", 0.001, 0.2, 0.02)
        dt = st.slider("Time step", 0.001, 0.05, 0.01)

    with col3:
        steps = st.slider("Steps", 10, 200, 60)
        use_ai = st.checkbox("🤖 IA prediction")

    # ================= INIT =================
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))

    obstacle = build_obstacle(nx, ny)

    # vortex initial
    y = np.linspace(0, 1, ny)
    u += np.sin(2 * np.pi * y[:, None])

    history = []

    # ================= RUN =================
    if st.button("🚀 Lancer simulation"):

        placeholder = st.empty()

        for i in range(steps):

            u, v, p = step(u, v, p, nu, dt, obstacle)

            history.append(u.copy())
            if len(history) > 10:
                history.pop(0)

            u_pred = predict(history) if use_ai and len(history) > 5 else np.zeros_like(u)

            # ================= PLOT =================
            fig = go.Figure()

            fig.add_trace(go.Heatmap(
                z=u,
                colorscale="Turbo",
                name="Vitesse U"
            ))

            fig.add_trace(go.Contour(
                z=obstacle,
                colorscale="Greys",
                showscale=False,
                opacity=0.5
            ))

            fig.update_layout(
                title=f"Navier-Stokes CFD step {i}",
                height=600
            )

            placeholder.plotly_chart(fig, use_container_width=True)

            time.sleep(0.03)

        st.success("Simulation terminée")

        # ================= STATS =================
        st.subheader("📊 Analyse")

        st.metric("Vitesse max", float(np.max(u)))
        st.metric("Vorticité approx", float(np.std(u)))

        st.line_chart(np.mean(np.abs(u), axis=0))