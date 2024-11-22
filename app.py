import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Chargement des données
df = pd.read_excel("GRDF 20241118.xlsx")

# Sélection et modification des colonnes nécessaires
df2 = df[['N° PCE', 'Date de relevé', 'Energie consommée (kWh)']].copy()
df2['Horodate'] = pd.to_datetime(df2['Date de relevé'], format='%d/%m/%Y')

# Remplacement des identifiants par des noms de sites
mapping = {
    "GI153881": 'PTWE89',
    "GI087131": 'PTWE35',
    "GI060319": 'PTWE42 Andrézieux',
}

df2['Site'] = df2['N° PCE'].map(mapping)
df2 = df2.drop(columns=['N° PCE'])
df_grdf_filtered = df2[['Site', 'Date de relevé', 'Energie consommée (kWh)']]

# Calcul de la consommation mensuelle par site et par année
df2['Année'] = df2['Horodate'].dt.year
df2['Mois'] = df2['Horodate'].dt.month

# Filtrer pour enlever novembre (11) et décembre (12)
df2 = df2[~df2['Mois'].isin([11, 12])]

# Calcul de la consommation mensuelle (en kWh)
df3 = df2.groupby(['Année', 'Mois', 'Site'])['Energie consommée (kWh)'].sum()  # Somme par mois, en kWh
df3 = df3.reset_index()

# Streamlit: Choisir le site à afficher
sites = df3['Site'].unique()
site_selection = st.selectbox('Choisissez un site', sites)

# Filtrer les données en fonction du site sélectionné
df_filtered = df3[df3['Site'] == site_selection]

# Créer un histogramme avec Plotly
fig = px.bar(df_filtered, x='Mois', y='Energie consommée (kWh)',
             color='Année', barmode='group',
             labels={'Mois': 'Mois', 'Energie consommée (kWh)': 'Consommation (kWh)'},
             title=f'Consommation d\'énergie mensuelle pour {site_selection}')

# Afficher l'histogramme interactif dans Streamlit
st.plotly_chart(fig)

# Afficher les données sous-jacentes (facultatif)
st.write(df_filtered)
