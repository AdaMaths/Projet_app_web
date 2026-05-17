from typing import Dict, Tuple
import pickle

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

try:
    from xgboost import XGBRegressor
    _HAS_XGB = True
except ImportError:
    XGBRegressor = None
    _HAS_XGB = False


def _to_minutes(x):
    """Convertit un horaire (hh:mm:ss ou nombre) en minutes (float)."""
    import datetime
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, datetime.timedelta):
        return x.total_seconds() / 60.0
    if isinstance(x, np.timedelta64):
        try:
            return pd.to_timedelta(x).total_seconds() / 60.0
        except Exception:
            return np.nan
    if isinstance(x, (datetime.time, datetime.datetime)):
        return x.hour * 60 + x.minute + x.second / 60
    if isinstance(x, str):
        parts = x.split(':')
        try:
            parts = [float(p) for p in parts]
            if len(parts) == 3:
                h, m, s = parts
            elif len(parts) == 2:
                h, m = parts
                s = 0
            else:
                return float(x)
            return h * 60 + m + s / 60
        except Exception:
            try:
                return float(x)
            except Exception:
                return np.nan
    return np.nan


def load_dataframe(uploaded_file) -> pd.DataFrame:
    """Charge un DataFrame depuis un fichier uploadé (Excel ou CSV)."""
    if uploaded_file is None:
        raise ValueError("Aucun fichier fourni")
    name = getattr(uploaded_file, 'name', '')
    if name.lower().endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file)
    else:
        return pd.read_csv(uploaded_file)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et prépare le DataFrame pour l'entraînement.

    - Supprime espaces sur noms de colonnes
    - Convertit colonnes numériques
    - Convertit 'Date' en chaîne standard
    - Convertit 'Heure' en minutes si présente
    - Crée `Energy_Gap` si `Ch 6` et `Ch 7` existent
    - Retourne DataFrame nettoyé
    """
    df = df.copy()
    df.columns = df.columns.str.strip()

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    if 'Heure' in df.columns:
        df['Heure'] = df['Heure'].apply(_to_minutes)

    # Convertir colonnes numériques (sauf Date/Heure)
    for col in df.columns:
        if col.lower() not in ('heure', 'date'):
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculer Energy_Gap si possible
    if 'Ch 6' in df.columns and 'Ch 7' in df.columns:
        df['Energy_Gap'] = df['Ch 7'] - df['Ch 6']

    # Drop lignes complètement vides
    df = df.dropna(how='all')

    return df


def train_and_evaluate(df: pd.DataFrame, target: str = 'Energy_Gap') -> Tuple[pd.DataFrame, Dict]:
    """Entraîne plusieurs modèles et renvoie les métriques et objets modèles.

    Retourne (results_df, model_objects)
    """
    if target not in df.columns:
        raise ValueError(f"La colonne cible '{target}' est introuvable dans le dataset")

    features = [c for c in df.columns if c != target]
    X = df[features].select_dtypes(include=[np.number]).dropna()
    y = df.loc[X.index, target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    if _HAS_XGB:
        models['XGBoost'] = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

    results = []
    model_objects = {}
    predictions = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)

        results.append({'Modèle': name, 'R2': float(r2), 'RMSE': float(rmse), 'MAE': float(mae)})
        model_objects[name] = model
        predictions[name] = (y_test, y_pred)

    results_df = pd.DataFrame(results).sort_values('R2', ascending=False).reset_index(drop=True)
    return results_df, {'models': model_objects, 'predictions': predictions}


def sample_dataset(n: int = 200) -> pd.DataFrame:
    """Génère un jeu d'exemple synthétique avec colonnes Ch 1..Ch 7 et Heure."""
    rng = np.random.default_rng(42)
    heures = (rng.integers(0, 24, size=n) + rng.random(n)).round(3)
    data = {
        'Heure': [f"{int(h)}:{int((h-int(h))*60):02d}:00" for h in heures],
        'Ch 1': rng.normal(100, 10, n),
        'Ch 2': rng.normal(50, 8, n),
        'Ch 3': rng.normal(30, 5, n),
        'Ch 4': rng.normal(20, 4, n),
        'Ch 5': rng.normal(10, 3, n),
        'Ch 6': rng.normal(60, 7, n),
        'Ch 7': rng.normal(65, 7, n),
    }
    df = pd.DataFrame(data)
    df['Ch 7'] = df['Ch 6'] + rng.normal(5, 3, n)  # garantir un gap moyen
    df['Energy_Gap'] = df['Ch 7'] - df['Ch 6']
    return df


def energy_page():
    """Page Streamlit intégrée depuis `streamlit_app.py`."""
    st.header("⚡ Module Énergie")

    st.markdown("Chargez un fichier Excel/CSV contenant les colonnes `Ch 1`..`Ch 7` et optionnellement `Heure`.")
    use_sample = st.checkbox("Utiliser un jeu d'exemple")

    if use_sample:
        df = sample_dataset()
        csv = df.to_csv(index=False).encode('utf-8')
        st.success("Jeu d'exemple chargé")
        st.download_button("Télécharger le jeu d'exemple (CSV)", data=csv, file_name='energy_sample.csv', mime='text/csv')
    else:
        uploaded = st.file_uploader("Télécharger le fichier (Excel ou CSV)", type=['csv', 'xls', 'xlsx'])

        if uploaded is None:
            st.info("Aucun fichier chargé — chargez vos données pour entraîner les modèles.")
            return

        try:
            df = load_dataframe(uploaded)
        except Exception as e:
            st.error(f"Impossible de lire le fichier : {e}")
            return

    st.write("Aperçu des données brutes :")
    st.dataframe(df.head())

    df_clean = preprocess(df)
    st.write("Aperçu après prétraitement :")
    st.dataframe(df_clean.head())

    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        st.subheader("Matrice de corrélation")
        corr = df_clean[numeric_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', square=True, linewidths=0.5, cbar_kws={'shrink': 0.75}, ax=ax_corr)
        ax_corr.set_title('Corrélation des variables numériques')
        st.pyplot(fig_corr)
    else:
        st.info("Pas assez de colonnes numériques pour afficher une matrice de corrélation.")

    if 'Energy_Gap' not in df_clean.columns:
        if 'Ch 6' in df_clean.columns and 'Ch 7' in df_clean.columns:
            df_clean['Energy_Gap'] = df_clean['Ch 7'] - df_clean['Ch 6']
            st.success("'Energy_Gap' créée automatiquement à partir de 'Ch 6' et 'Ch 7'.")
        else:
            st.error("Colonnes 'Ch 6' et/ou 'Ch 7' manquantes. Impossible de calculer 'Energy_Gap'.")
            return

    try:
        results_df, meta = train_and_evaluate(df_clean, target='Energy_Gap')
    except Exception as e:
        st.error(f"Erreur lors de l'entraînement : {e}")
        return

    st.subheader("Comparaison des modèles")
    st.dataframe(results_df)

    # Afficher graphiques de prédiction pour chaque modèle
    for name, (y_test, y_pred) in meta['predictions'].items():
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(y_test, y_pred, alpha=0.6)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        ax.set_title(f"{name} — RMSE: {rmse:.2f}")
        ax.set_xlabel('Réel')
        ax.set_ylabel('Prédit')
        st.pyplot(fig)

    # Sauvegarder le meilleur modèle
    best_name = results_df.loc[0, 'Modèle']
    best_model = meta['models'][best_name]
    # Sauvegarde sur disque
    path = 'modules/meilleur_modele_energie.pkl'
    joblib.dump(best_model, path)

    # Préparer le téléchargement direct depuis l'UI
    try:
        pickle_bytes = pickle.dumps(best_model)
        st.download_button("Télécharger le meilleur modèle", data=pickle_bytes,
                           file_name='meilleur_modele_energie.pkl', mime='application/octet-stream')
    except Exception:
        st.warning("Téléchargement direct indisponible pour ce type de modèle.")

    st.success(f"Meilleur modèle : {best_name} — sauvegardé sous {path}")






