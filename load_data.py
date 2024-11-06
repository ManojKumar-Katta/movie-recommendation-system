import pickle
import streamlit as st
import requests

# Define a ground truth dictionary for evaluation (this should be created from actual data)
# Format example: {"Movie Title 1": ["Relevant Movie 1", "Relevant Movie 2"], "Movie Title 2": [...]}
ground_truth = {
    "Avatar": ["Ender's Game", "Apollo 18"],
    "Tangled": ["Frozen", "Aladdin"],
    # Add more known relationships here for validation
}
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "default_poster.jpg"  # Default image if poster is missing
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "default_poster.jpg"  # Default image in case of error
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Accuracy and Precision Evaluation
def evaluate_recommender():
    precision_at_k = []
    hit_rate_count = 0

    for movie, relevant_movies in ground_truth.items():
        if movie in movies['title'].values:
            recommended_names, _ = recommend(movie)
            relevant_set = set(relevant_movies)
            recommended_set = set(recommended_names)

            # Calculate precision@K
            true_positives = len(recommended_set & relevant_set)
            precision = true_positives / len(recommended_set) if recommended_set else 0
            precision_at_k.append(precision)

            # Calculate hit rate
            if true_positives > 0:
                hit_rate_count += 1

    # Calculate overall metrics
    avg_precision_at_k = sum(precision_at_k) / len(precision_at_k) if precision_at_k else 0
    hit_rate = hit_rate_count / len(ground_truth) if ground_truth else 0

    return avg_precision_at_k, hit_rate

# Streamlit App UI
st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

    # Display evaluation metrics
    avg_precision, hit_rate = evaluate_recommender()
    st.write(f"Average Precision@5: {avg_precision:.2f}")
    st.write(f"Hit Rate: {hit_rate:.2f}")
