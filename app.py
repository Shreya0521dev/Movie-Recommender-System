import streamlit as st
import pickle
import pandas as pd
import requests


st.set_page_config(
    page_title="Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CUSTOM CSS
st.markdown("""
<style>

.stApp{
    background:#0b0b0b;
}

html, body, [class*="css"]{
    color:white;
}

h1,h2,h3,h4,h5{
    color:white;
}
.hero{
    background: linear-gradient(90deg,#141414,#1f1f1f,#141414);
    padding:40px;
    border-radius:20px;
    text-align:center;
    margin-bottom:30px;
}

.hero h1{
    color:#E50914;
    text-align: center;
    font-size: 50px;
}
.hero p{
    color:#d1d1d1;
    font-size:20px;
     text-align:center;
    margin-bottom:30px;
}
.movie-card {
    border-radius: 15px;
    overflow: hidden;
    transition: 0.3s;
    padding: 10px;
    background-color: #1c1c1c;
}

.movie-card:hover {
    transform: scale(1.05);
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    border: none;
    height: 3em;
    width: 200px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7988c98e8730b6218f68a236655c5746&language=en-US'

    try:
        # Added a 5-second timeout so it doesn't hang forever
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    except (requests.exceptions.ConnectTimeout, requests.exceptions.RequestException):
        # Fallback URL if the network is down or times out
        return "https://via.placeholder.com/500x750.png?text=Poster+Not+Found"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie.append(movies.iloc[i[0]].title)

        # fetch poster from api
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie, recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pickle', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("""
<div class="hero">
    <h1>🎬 Movie Recommender System</h1>
    <p>
        Discover amazing movies powered by AI recommendations.<br>
        Search your favourite movie and get similar movie suggestions instantly.
    </p>
</div>
""", unsafe_allow_html=True)
selected_movie = st.selectbox(
"Enter the movie name",
movies['title'].values
)
if st.button("Recommend"):

    names,posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


