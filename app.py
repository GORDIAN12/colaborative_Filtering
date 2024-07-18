import requests
import pickle
import pandas as pd
import streamlit as st

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=YOU_API_KEY".format(movie_id)

    data = requests.get(url)
    data = data.json()

    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path

    return full_path

def recommend(movie):
    index=movies[movies['title']==movie].index[0]

    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1],)

    recommended_movie_names=[]
    recommended_movie_posters=[]

    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names ,recommended_movie_posters

st.header('Movie Recommendations')
movies=pd.read_pickle('movie_list.pkl')
similarity=pd.read_pickle('similarity.pkl')

movie_list=movies['title'].values
selected_movies=st.selectbox(
    "Selecciona la pelicula de la lista",
    movie_list
)

import streamlit as st

if st.button('Recomendar la pelicula'):
    recommend_movie_names,recommend_movie_posters=recommend(selected_movies)
    cols=st.columns(5)

    for i, col in enumerate(cols):
        col.text(recommend_movie_names[i])
        col.image(recommend_movie_posters[i])
