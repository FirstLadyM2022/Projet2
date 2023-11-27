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
#df['genres'] = df['genres'].map({"\N" : 'Non renseigné'})
df['decennie'] = df['startYear'].apply(lambda x : x[0:3])
df['decennie'] = df['decennie'].apply(lambda x : str(x)+'0')
#df[['title', 'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'primaryName', 'category', 'job', 'characters', 'primaryTitle', 'originalTitle', 'decennie']]
isna_ = pd.DataFrame(df['averageRating'].isna().value_counts())

col1_df, col2_df = st.columns(2)

with col1_df :
  f"Voici un échantillon aléatoire de 5 films parmi la sélection initiale, qui contient {df['tconst'].nunique()} films :"
  df_sample = df[['title', 'genres', 'startYear']].sample(5)
  df_sample.set_axis(['Titre', 'Genres', 'Année'], axis = 1, inplace = True)
  df_sample

with col2_df :
  "Quelques statistiques sommaires concernant la sélection :"
  df_stats = df[['numVotes', 'averageRating']].describe()
  df_stats.drop(['count', 'std'], axis = 0, inplace = True)
  df_stats['averageRating'] = df_stats['averageRating'].round(2)
  df_stats['numVotes'] = df_stats['numVotes'].astype('int')
  df_stats.set_axis(['Nombre de votes', 'Note moyenne'], axis = 1, inplace = True)
  df_stats

f"Précision : parmi ces films, {isna_['averageRating'][1]} n'ont pas de note. Ils seront donc ignorés dans l'analyse qui suit."

st.title('Ajustement de la selection')

"Nous vous proposons d'effectuer un ajustement par la note, le nombre de votes et éventuellement le genre, et visualiser l'impact de vos choix :"

col_notes, col_votes, col_genre = st.columns(3)

with col_notes :
  note = st.slider("Choisissez la note minimum des films :", 0, 10, 0)

with col_votes :
  votes = st.slider("Choisissez le nombre de votes minimum :", 0, 5000, 0)

with col_genre :
  expdgenres = df['genres'].str.split(',')
  expdgenres = expdgenres.explode('genres')
  expdgenres = expdgenres.value_counts()
  expdgenres = pd.DataFrame(expdgenres).reset_index().sort_values('index')
  genres = expdgenres['index'].unique()
  genres = ['(tous)'] + list(genres)
  genre = st.selectbox("Genre :", genres)

if genre != "(tous)" :
  select = df[(df['averageRating'] >= note) & (df['numVotes'] >= votes) & (df['genres'].str.contains(genre))]
if genre == "(tous)" :
  select = df[(df['averageRating'] >= note) & (df['numVotes'] >= votes)]

st.title('Statistiques visuelles pour votre sélection :')

f"Les critères sélectionnés réduisent votre sélection à {select['tconst'].nunique()} films (liste sous les graphiques) :"

graph1, graph2 = st.columns(2)
graph3, graph4 = st.columns(2)

with graph1 :
  A = sns.boxplot(x=select['averageRating'])
  plt.title('Distribution en fonction de la note')
  plt.xlabel('Note moyenne')
  A.set_xticks(range(0, 11, 1))
  st.pyplot(A.figure) ; plt.close()

with graph2 :
  B = sns.barplot(x=select['decennie'].sort_values(), y=select['numVotes'], hue = select['decennie'])
  plt.title('Nombre de votes par décennie')
  plt.xlabel("")
  st.pyplot(B.figure) ; plt.close()

with graph3 :

  C = sns.scatterplot(x = select['averageRating'], y = select['numVotes'], hue = select['decennie'])
  plt.title('Nombre de votes en fonction de la note')
  plt.xlabel('Note moyenne')
  plt.ylabel('Nb de votes')
  C.set_xticks(range(0, 11, 1))
  st.pyplot(C.figure) ; plt.close()

with graph4 :
  D = sns.histplot(select['decennie'].sort_values())
  plt.title('Répartition par décennie')
  plt.xlabel("")
  plt.ylabel("Nombre de films")
  st.pyplot(D.figure) ; plt.close()

c1, c2 = st.columns([0.7, 0.3])

with c1 :

  f"Détail des films de votre sélection : ({select['tconst'].nunique()})"

  display = select[['title', 'genres', 'startYear', 'averageRating', 'numVotes']].set_axis(['Titre', 'Genres', 'Année', 'Note moyenne', 'Nombre de votes'], axis = 1)
  display

with c2 :

  st.write("Quelques statistiques sommaires :")
  stat = select[['numVotes', 'averageRating']].describe()
  stat.drop(['count', 'std'], axis = 0, inplace = True)
  stat['averageRating'] = stat['averageRating'].round(2)
  stat['numVotes'] = stat['numVotes'].astype('int')
  stat.set_axis(['Nombre de votes', 'Note moyenne'], axis = 1, inplace = True)
  stat
