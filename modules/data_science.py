import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# =========================================================
# PAGE DATA SCIENCE
# =========================================================

def data_science_page():

    st.title("📊 Data Science & Machine Learning")

    st.markdown("""
    Analyse complète du dataset Advertising.csv :
    - statistiques,
    - visualisations,
    - corrélations,
    - régression linéaire,
    - random forest,
    - prédictions.
    """)

    # =====================================================
    # CHARGEMENT FICHIER
    # =====================================================

    uploaded_file = st.file_uploader(
        "Importer un fichier CSV ou Excel",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        try:

            # =============================================
            # LECTURE FICHIER
            # =============================================

            if uploaded_file.name.endswith(".csv"):

                df = pd.read_csv(uploaded_file)

            else:

                df = pd.read_excel(uploaded_file)

            # =============================================
            # SUPPRESSION AUTOMATIQUE
            # DES COLONNES UNNAMED
            # =============================================

            df = df.loc[
                :,
                ~df.columns.str.contains("^Unnamed")
            ]

            st.success("✅ Fichier chargé avec succès")

            # =============================================
            # APERÇU
            # =============================================

            st.subheader("📋 Aperçu des données")

            st.dataframe(
                df,
                use_container_width=True
            )

            # =============================================
            # INFOS GÉNÉRALES
            # =============================================

            st.subheader("📌 Informations générales")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Lignes", df.shape[0])

            with col2:
                st.metric("Colonnes", df.shape[1])

            with col3:
                st.metric(
                    "Valeurs manquantes",
                    int(df.isnull().sum().sum())
                )

            with col4:
                st.metric(
                    "Variables numériques",
                    len(
                        df.select_dtypes(
                            include=np.number
                        ).columns
                    )
                )

            # =============================================
            # TYPES
            # =============================================

            st.subheader("🧾 Types des colonnes")

            dtype_df = pd.DataFrame({

                "Colonne": df.columns,

                "Type": df.dtypes.astype(str)

            })

            st.dataframe(
                dtype_df,
                use_container_width=True
            )

            # =============================================
            # VALEURS MANQUANTES
            # =============================================

            st.subheader("⚠️ Valeurs manquantes")

            missing_df = pd.DataFrame({

                "Colonne": df.columns,

                "Valeurs manquantes": df.isnull().sum()

            })

            st.dataframe(
                missing_df,
                use_container_width=True
            )

            # =============================================
            # STATISTIQUES
            # =============================================

            st.subheader("📈 Statistiques descriptives")

            st.dataframe(
                df.describe(),
                use_container_width=True
            )

            # =============================================
            # VARIABLES NUMÉRIQUES
            # =============================================

            numeric_cols = list(
                df.select_dtypes(
                    include=np.number
                ).columns
            )

            if len(numeric_cols) == 0:

                st.error(
                    "❌ Aucune colonne numérique détectée"
                )

                return

            # =============================================
            # VISUALISATION
            # =============================================

            st.subheader("📊 Visualisation des données")

            graph_type = st.radio(
                "Type de graphique",
                [
                    "Scatter",
                    "Courbe",
                    "Histogramme",
                    "Boxplot"
                ],
                horizontal=True
            )

            # =============================================
            # CHOIX VARIABLES
            # =============================================

            colx, coly = st.columns(2)

            with colx:

                x_axis = st.selectbox(
                    "Variable X",
                    numeric_cols,
                    index=0
                )

            with coly:

                y_axis = st.selectbox(
                    "Variable Y",
                    numeric_cols,
                    index=min(
                        1,
                        len(numeric_cols)-1
                    )
                )

            # =============================================
            # SCATTER
            # =============================================

            if graph_type == "Scatter":

                fig = px.scatter(
                    df,
                    x=x_axis,
                    y=y_axis,
                    trendline="ols",
                    title=f"{x_axis} vs {y_axis}",
                    color=y_axis
                )

            # =============================================
            # COURBE
            # =============================================

            elif graph_type == "Courbe":

                fig = px.line(
                    df,
                    x=x_axis,
                    y=y_axis,
                    markers=True,
                    title=f"{x_axis} vs {y_axis}"
                )

            # =============================================
            # HISTOGRAMME
            # =============================================

            elif graph_type == "Histogramme":

                fig = px.histogram(
                    df,
                    x=x_axis,
                    nbins=30,
                    title=f"Distribution de {x_axis}",
                    color_discrete_sequence=["orange"]
                )

            # =============================================
            # BOXPLOT
            # =============================================

            else:

                fig = px.box(
                    df,
                    y=y_axis,
                    title=f"Boxplot de {y_axis}",
                    color_discrete_sequence=["green"]
                )

            fig.update_layout(
                template="plotly_white",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =============================================
            # COMBINAISONS DIRECTES
            # =============================================

            st.subheader("📌 Relations importantes")

            c1, c2, c3 = st.columns(3)

            with c1:

                if "TV" in df.columns and "Radio" in df.columns:

                    fig_tv_radio = px.scatter(
                        df,
                        x="TV",
                        y="Radio",
                        trendline="ols",
                        title="TV vs Radio"
                    )

                    st.plotly_chart(
                        fig_tv_radio,
                        use_container_width=True
                    )

            with c2:

                if "TV" in df.columns and "Newspaper" in df.columns:

                    fig_tv_news = px.scatter(
                        df,
                        x="TV",
                        y="Newspaper",
                        trendline="ols",
                        title="TV vs Newspaper"
                    )

                    st.plotly_chart(
                        fig_tv_news,
                        use_container_width=True
                    )

            with c3:

                if "Radio" in df.columns and "Newspaper" in df.columns:

                    fig_radio_news = px.scatter(
                        df,
                        x="Radio",
                        y="Newspaper",
                        trendline="ols",
                        title="Radio vs Newspaper"
                    )

                    st.plotly_chart(
                        fig_radio_news,
                        use_container_width=True
                    )

            # =============================================
            # MATRICE CORRÉLATION
            # =============================================

            st.subheader("🔥 Matrice de corrélation")

            corr = df.corr(numeric_only=True)

            fig_corr = px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                title="Corrélations"
            )

            fig_corr.update_layout(
                height=700
            )

            st.plotly_chart(
                fig_corr,
                use_container_width=True
            )

            # =============================================
            # MACHINE LEARNING
            # =============================================

            st.subheader("🤖 Machine Learning")

            # =============================================
            # CHOIX MODELE
            # =============================================

            model_choice = st.selectbox(
                "Choisir un modèle",
                [
                    "Régression Linéaire",
                    "Random Forest"
                ]
            )

            # =============================================
            # VARIABLE CIBLE
            # =============================================

            target = st.selectbox(
                "Variable cible",
                numeric_cols,
                index=len(numeric_cols)-1
            )

            # =============================================
            # FEATURES
            # =============================================

            features = st.multiselect(
                "Variables explicatives",
                [
                    c for c in numeric_cols
                    if c != target
                ],
                default=[
                    c for c in numeric_cols
                    if c != target
                ]
            )

            if len(features) > 0:

                X = df[features]

                y = df[target]

                # =========================================
                # TEST SIZE
                # =========================================

                test_size = st.slider(
                    "Taille ensemble test",
                    0.1,
                    0.5,
                    0.2
                )

                # =========================================
                # RANDOM FOREST PARAMS
                # =========================================

                n_estimators = 100

                if model_choice == "Random Forest":

                    n_estimators = st.slider(
                        "Nombre d'arbres",
                        10,
                        500,
                        100
                    )

                # =========================================
                # SPLIT
                # =========================================

                X_train, X_test, y_train, y_test = train_test_split(
                    X,
                    y,
                    test_size=test_size,
                    random_state=42
                )

                # =========================================
                # MODELE
                # =========================================

                if model_choice == "Régression Linéaire":

                    model = LinearRegression()

                else:

                    model = RandomForestRegressor(
                        n_estimators=n_estimators,
                        random_state=42
                    )

                # =========================================
                # TRAIN
                # =========================================

                model.fit(
                    X_train,
                    y_train
                )

                predictions = model.predict(
                    X_test
                )

                # =========================================
                # METRICS
                # =========================================

                mse = mean_squared_error(
                    y_test,
                    predictions
                )

                mae = mean_absolute_error(
                    y_test,
                    predictions
                )

                r2 = r2_score(
                    y_test,
                    predictions
                )

                st.subheader("📊 Performances du modèle")

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric("R²", f"{r2:.4f}")

                with c2:
                    st.metric("MAE", f"{mae:.4f}")

                with c3:
                    st.metric("MSE", f"{mse:.4f}")

                # =========================================
                # RÉEL VS PRÉDIT
                # =========================================

                st.subheader("🎯 Réel vs Prédit")

                fig_pred = go.Figure()

                fig_pred.add_trace(
                    go.Scatter(
                        x=y_test,
                        y=predictions,
                        mode='markers',
                        name='Prédictions'
                    )
                )

                fig_pred.add_trace(
                    go.Scatter(
                        x=[
                            y_test.min(),
                            y_test.max()
                        ],
                        y=[
                            y_test.min(),
                            y_test.max()
                        ],
                        mode='lines',
                        name='Parfait'
                    )
                )

                fig_pred.update_layout(
                    title="Valeurs réelles vs prédites",
                    xaxis_title="Réel",
                    yaxis_title="Prédit",
                    height=600,
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig_pred,
                    use_container_width=True
                )

                # =========================================
                # IMPORTANCE VARIABLES
                # =========================================

                st.subheader("📌 Importance des variables")

                # =========================================
                # REGRESSION LINEAIRE
                # =========================================

                if model_choice == "Régression Linéaire":

                    coef_df = pd.DataFrame({

                        "Variable": features,

                        "Coefficient": model.coef_

                    })

                    st.dataframe(
                        coef_df,
                        use_container_width=True
                    )

                    # EQUATION

                    equation = (
                        f"y = {model.intercept_:.3f}"
                    )

                    for i, col in enumerate(features):

                        equation += (
                            f" + ({model.coef_[i]:.3f})×{col}"
                        )

                    st.subheader(
                        "🧮 Équation du modèle"
                    )

                    st.code(equation)

                # =========================================
                # RANDOM FOREST
                # =========================================

                else:

                    importance_df = pd.DataFrame({

                        "Variable": features,

                        "Importance": model.feature_importances_

                    })

                    importance_df = importance_df.sort_values(
                        by="Importance",
                        ascending=False
                    )

                    st.dataframe(
                        importance_df,
                        use_container_width=True
                    )

                    fig_importance = px.bar(
                        importance_df,
                        x="Variable",
                        y="Importance",
                        title="Importance des variables"
                    )

                    st.plotly_chart(
                        fig_importance,
                        use_container_width=True
                    )

                # =========================================
                # PREDICTION UTILISATEUR
                # =========================================

                st.subheader("🧠 Faire une prédiction")

                st.write(
                    "Entrer les valeurs des variables explicatives :"
                )

                input_data = {}

                cols = st.columns(2)

                for i, feature in enumerate(features):

                    with cols[i % 2]:

                        input_data[feature] = st.number_input(
                            feature,
                            value=float(
                                df[feature].mean()
                            ),
                            step=0.1
                        )

                # =========================================
                # BOUTON UNIQUE
                # =========================================

                predict_button = st.button(
                    "🚀 Lancer la prédiction"
                )

                if predict_button:

                    input_df = pd.DataFrame(
                        [input_data]
                    )

                    prediction = model.predict(
                        input_df
                    )[0]

                    st.success(
                        f"✅ Valeur prédite : {prediction:.4f}"
                    )

                    st.balloons()

            # =============================================
            # EXPORT
            # =============================================

            st.subheader("💾 Export des données")

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Télécharger CSV",
                csv,
                "export_dataset.csv",
                "text/csv"
            )

        except Exception as e:

            st.error(f"❌ Erreur : {e}")

    else:

        st.info("""
        👆 Importez un fichier CSV ou Excel
        """)