# SciPRO - Application de calcul scientifique

SciPRO est une application web de calcul scientifique composee de deux parties :

- un site vitrine Flask accessible sur `http://127.0.0.1:3000` ;
- une application interactive Streamlit accessible sur `http://127.0.0.1:5000`.

Le site Flask presente le projet et contient des boutons qui ouvrent l'application Streamlit.

## Fonctionnalites

- Profil gaussien : generation et visualisation de courbes gaussiennes.
- Simulation laser : modelisation de la dynamique laser.
- Pertes de cavite : analyse des pertes optiques dans une cavite.
- Optimisation : minimisation et optimisation de fonctions.
- Automatique : analyse de systemes et controle.
- Navier-Stokes : simulation de fluides et ecoulements.
- Data Science : exploration de donnees, regression, classification et clustering.
- Energie : analyse et prediction de donnees energetiques.
- Numerisation Hub : methodes numeriques et export de donnees.
- Integration : calculs d'integrales numeriques.
- Interpolation : interpolation et approximation de donnees.
- Equations differentielles : resolution et visualisation.
- Signal : traitement et affichage de signaux.

## Installation

Creer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement sous Windows :

```bash
venv\Scripts\activate
```

Installer les dependances :

```bash
pip install -r requirements.txt
```

## Lancement

Lancer l'application Streamlit :

```bash
python -m streamlit run streamlit_app.py --server.port=5000 --server.address=127.0.0.1 --server.headless=true
```

Lancer le site web Flask dans un autre terminal :

```bash
python website/app.py
```

Ouvrir ensuite :

- site web : `http://127.0.0.1:3000`
- application Streamlit : `http://127.0.0.1:5000`

## Structure du projet

```text
Projet_app_web/
|-- streamlit_app.py              # Application principale Streamlit
|-- website/
|   |-- app.py                    # Serveur Flask du site web
|   |-- templates/
|   |   `-- index.html            # Page du site web
|   `-- static/                   # Fichiers statiques du site
|-- modules/
|   |-- automatique.py
|   |-- cavity_losses.py
|   |-- data_science.py
|   |-- energy.py
|   |-- equ_diff.py
|   |-- gaussian.py
|   |-- integration.py
|   |-- interpolation.py
|   |-- laser_simulation.py
|   |-- navier_stokes.py
|   |-- numerisation_hub.py
|   |-- optimisation.py
|   `-- signal.py
|-- assets/
|-- data/
|-- requirements.txt
|-- requirements_streamlit.txt
`-- README.md
```

## Dependances principales

- Flask : serveur du site web.
- Streamlit : interface interactive de calcul scientifique.
- NumPy, SciPy, Pandas : calcul numerique et analyse de donnees.
- Matplotlib, Plotly, Seaborn : visualisations.
- Scikit-learn, XGBoost, Joblib : machine learning.
- OpenPyXL : lecture de fichiers Excel.

## Commandes utiles

Verifier la version de Streamlit :

```bash
python -m streamlit --version
```

Lancer Streamlit sur un autre port :

```bash
python -m streamlit run streamlit_app.py --server.port=8502
```

Lancer Flask en mode developpement :

```bash
python website/app.py
```

## Page Energie

- Ouvrir la page Energie dans la barre laterale de Streamlit.
- Charger un fichier Excel ou CSV contenant les colonnes `Ch 1` a `Ch 7`, avec `Heure` en option.
- Ou utiliser le jeu d'exemple fourni.
- Apres l'entrainement, telecharger le meilleur modele au format pickle depuis l'interface.

Fichier d'exemple : `assets/energy_sample.csv`.

## Notes

- Le port du site web Flask est `3000`.
- Le port de l'application Streamlit est `5000`.
- Si un port est deja utilise, arreter le processus concerne ou choisir un autre port.
- Le serveur Flask lance par `python website/app.py` est adapte au developpement local. Pour une mise en production, utiliser un serveur WSGI de production.
