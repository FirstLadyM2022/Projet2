import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

title1, title2 = st.columns(2)

with title1 :
  st.title('Projet 2 : Système de recommandation de films')
with title2 :
  "Olmira, Mireille, Maxime, Julie" 
  st.image('logo_WCS.png')

#####


st.title('Première partie : Analyse de données')

st.write("Il nous a été demandé premièrement de nettoyer et analyser une base de données contenant les caractérisqtiques de nombreux films, et d'en extraire une selection à proposer à un cinéma Français en perte de vitesse.")

st.title('Filtrer sur les notes et les votes attribués aux films')

st.write("Après un premier niveau de filtrage, nous vous proposons d'affiner la sélection en choisissant une note minimum ainsi qu'un nombre de votes minimum pour les films qui seront retenus.")
st.write("La sélection présentée ici répond aux critères suivants : Retrait des films pour adultes, année supérieure ou égale à 1980, version du film destinée à la France.")

#Chargement du DataFrame étudié :
df = pd.read_csv('final0.csv')
df.drop(df.loc[df["genres"].str.contains('Adult')].index, inplace=True)

col1_df, col2_df = st.columns(2)

with col1_df :
  f"Voici un échantillon aléatoire de 5 films parmi la sélection initiale, qui contient {df['tconst'].nunique()} films :"
  df_sample = df[['title', 'genres', 'startYear']].sample(5)
  df_sample

with col2_df :
  "Quelques statistiques sommaires concernant la sélection :"
  df_stats = df[['numVotes', 'averageRating']].describe()
  df_stats.drop(['count', 'std'], axis = 0, inplace = True)
  df_stats['averageRating'] = df_stats['averageRating'].round(2)
  df_stats['numVotes'] = df_stats['numVotes'].astype('int')
  df_stats

"Nous vous proposons d'effectuer un ajustement par la note et le nombre de votes, et visualiser l'impact de vos choix :"

col_notes, col_votes, col_genre = st.columns(3)

with col_notes :
  note = st.slider("Choisissez la note minimum des films :", 0, 10, 0)

with col_votes :
  votes = st.slider("Choisissez le nombre de votes minimum :", 0, 5000, 0)

with col_genre :
  expdgenres = df['genres'].str.split(',')
  expdgenres = expdgenres.explode('genres')
  expdgenres = expdgenres.value_counts()
  expdgenres = pd.DataFrame(expdgenres).reset_index()
  genres = expdgenres['index'].unique()
  genres = list(genres) + ['(tous)']
  genre = st.selectbox("Genre :", genres)

if genre != "(tous)" :
  select = df[(df['averageRating'] >= note) & (df['numVotes'] >= votes) & (df['genres'].str.contains(genre))]
if genre == "(tous)" :
  select = df[(df['averageRating'] >= note) & (df['numVotes'] >= votes)]
st.write(len(select))

f"Les critères sélectionnés réduisent votre sélection à ces {select['tconst'].nunique()} films :"

select[['title', 'genres', 'startYear', 'averageRating', 'numVotes']]

st.title('Statistiques visuelles pour votre sélection :')

graph1, graph2, graph3, graph4 = st.columns(4)

with graph1 :
  sns.boxplot(x=select['averageRating']).figure ; plt.close()
with graph2 :
  sns.boxplot(x=select['numVotes']).figure ; plt.close()
with graph3 :
  sns.scatterplot(x = select['averageRating'], y = select['numVotes']).figure ; plt.close()
with graph4 :
  sns.histplot(select['averageRating'], bins=10).figure ; plt.close()
