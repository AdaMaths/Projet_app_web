import streamlit as st
import numpy as np
from scipy import signal
from numpy.fft import fft, fftfreq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# =========================
# 📡 SIGNAL PAGE (AMÉLIORÉE)
# =========================

def signal_page():

    st.title("📡 Traitement du Signal (DSP avancé)")

    # ================= PARAMS =================
    signal_type = st.selectbox(
        "Type de signal",
        ["Sinus", "Carré", "Triangle", "Dent de scie", "Chirp", "Bruit blanc"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        freq = st.number_input("Fréquence (Hz)", 1.0, 200.0, 5.0)

    with col2:
        amp = st.number_input("Amplitude", 0.1, 10.0, 1.0)

    with col3:
        duration = st.number_input("Durée (s)", 0.5, 5.0, 2.0)

    fs = st.slider("Fréquence d'échantillonnage (Hz)", 500, 10000, 2000)

    analyse = st.radio(
        "Analyse",
        ["Signal temporel", "FFT", "Spectrogramme"],
        horizontal=True
    )

    # ================= GENERATION =================
    def generate():

        t = np.linspace(0, duration, int(fs * duration))

        if signal_type == "Sinus":
            s = amp * np.sin(2 * np.pi * freq * t)

        elif signal_type == "Carré":
            s = amp * signal.square(2 * np.pi * freq * t)

        elif signal_type == "Triangle":
            s = amp * signal.sawtooth(2 * np.pi * freq * t, 0.5)

        elif signal_type == "Dent de scie":
            s = amp * signal.sawtooth(2 * np.pi * freq * t)

        elif signal_type == "Chirp":
            s = amp * signal.chirp(t, freq, duration, freq * 5)

        else:
            s = amp * np.random.normal(0, 1, len(t))

        return t, s

    # ================= FFT =================
    def compute_fft(s):
        N = len(s)
        yf = fft(s)
        xf = fftfreq(N, 1/fs)

        mask = xf > 0
        return xf[mask], (2.0/N) * np.abs(yf[mask])

    # ================= RUN =================
    if st.button("🚀 Générer signal"):

        t, s = generate()

        st.session_state.t = t
        st.session_state.s = s

        # ================= DISPLAY =================
        if analyse == "Signal temporel":

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=s, mode="lines"))

            fig.update_layout(
                title="Signal temporel",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        # ================= FFT =================
        elif analyse == "FFT":

            xf, yf = compute_fft(s)

            fig = make_subplots(rows=2, cols=1)

            fig.add_trace(
                go.Scatter(x=t, y=s, name="Signal"),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(x=xf, y=yf, name="FFT"),
                row=2, col=1
            )

            fig.update_layout(height=600, title="Analyse fréquentielle")

            st.plotly_chart(fig, use_container_width=True)

            # fréquence dominante
            f_dom = xf[np.argmax(yf)]
            st.metric("Fréquence dominante", f"{f_dom:.2f} Hz")

        # ================= SPECTROGRAMME =================
        else:

            f, tt, Sxx = signal.spectrogram(s, fs)

            fig = go.Figure(data=go.Heatmap(
                z=10 * np.log10(Sxx + 1e-10),
                x=tt,
                y=f,
                colorscale="Turbo"
            ))

            fig.update_layout(
                title="Spectrogramme (temps-fréquence)",
                xaxis_title="Temps",
                yaxis_title="Fréquence"
            )

            st.plotly_chart(fig, use_container_width=True)

    # ================= METRICS =================
    if "s" in st.session_state:

        s = st.session_state.s

        st.subheader("📊 Analyse rapide")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("RMS", f"{np.sqrt(np.mean(s**2)):.3f}")

        with col2:
            st.metric("Max amplitude", f"{np.max(s):.3f}")

        with col3:
            st.metric("Énergie", f"{np.sum(s**2):.2f}")

    # ================= EXPORT =================
    if "s" in st.session_state:

        df = pd.DataFrame({
            "time": st.session_state.t,
            "signal": st.session_state.s
        })

        csv = df.to_csv(index=False).encode()

        st.download_button(
            "💾 Export CSV",
            csv,
            "signal.csv",
            "text/csv"
        )

    # ================= THEORIE =================
    with st.expander("📖 Théorie DSP"):
        st.markdown("""
        - FFT = transformation temps → fréquence  
        - Spectrogramme = FFT glissante  
        - Carré → harmoniques impaires  
        - Chirp → fréquence variable  
        """)