import streamlit as st 
import pandas as pd 
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer, util
import numpy as np
import pickle
import os

@st.cache_data
def load_data():
    films = pd.read_csv('TMDb_IMDb_full.csv')
    actors_df = pd.read_csv("Intervenants.csv")
    bridge_df = pd.read_csv('Table__Intermediare.csv.csv')  
    
    # Encoding Genres
    X = films['genres'].str.get_dummies(sep=',')
    X['original_language'] = films['original_language'].replace({'en':1,'fr':0}) * 5
    
    # Normalize numeric values
    mms = MinMaxScaler()
    X['vote_normalized'] = mms.fit_transform(films[['imdb_averageRating']]) * 5
    films['popularity'] = films['popularity'].replace('Inconnu', 0)
    X['popularity'] = mms.fit_transform(films[['popularity']]) * 5
    X['runtimeMinutes'] = mms.fit_transform(films[['runtimeMinutes']])
    
    return films, X, actors_df, bridge_df


@st.cache_resource
def load_model():

    return SentenceTransformer('all-MiniLM-L6-v2')


@st.cache_data
def compute_embeddings(overview_list):

    embeddings_file = 'embeddings_cache.pkl'
    
    if os.path.exists(embeddings_file):
        with open(embeddings_file, 'rb') as f:
            embeddings = pickle.load(f)
        return embeddings
    else:
        model = load_model()
        embeddings = model.encode(overview_list, convert_to_tensor=True)
        

        with open(embeddings_file, 'wb') as f:
            pickle.dump(embeddings, f)
        
        return embeddings

def show_search():
    st.title("🔍 Trouvez des films qui vous ressemblent")
    st.write("Trouvez facilement un film en utilisant le menu déroulant ou en tapant un titre dans la barre de recherche pour vérifier s'il figure dans notre base de données. Une fois votre film sélectionné, nous vous proposons une liste de films similaires. Sous chaque affiche, vous pouvez cliquer sur un bouton pour obtenir plus d'informations détaillées sur le film : synopsis, casting, durée et plus encore. Votre prochaine soirée cinéma commence ici !")
    

    with st.spinner('Caricamento dati...'):
        films, X, actors_df, bridge_df = load_data()
    
    # Sidebar controls
    st.sidebar.header('Select the filter you want to change : ')
    rec = st.sidebar.select_slider(
        'Select how many recommendations you want :',
        options = [2, 3, 4, 5, 6, 7, 8, 9, 10],
        value=(5)
    )
    col = st.sidebar.select_slider(
        'Select how many films you want to see per row : ',
        options=[3,4,5,6,7,8,9,10],
        value=5
    )
    choice = st.radio('Select the recommendation method',
                      ['Same Genre', 'Same Context'],
                      captions=[
                          'Similarity in genres',
                          'Similarity in synopsis'
                      ],
                      )
    
    # Film selection
    option = st.selectbox('Choose a film to get recommendations: ', films['original_title'].to_list())
    
    if option:
        # Get index of selected film
        try:
            index = films[films['original_title'] == option].index[0]
        except IndexError:
            st.error("Film not found in the database")
            return
        
        if choice == 'Same Genre':
            with st.spinner('Loading reccomandations based on genres...'):
                # Training the model
                knn = NearestNeighbors(n_neighbors=rec+1, metric='euclidean')
                knn.fit(X)
                
                distances, indices = knn.kneighbors(X.iloc[[index]], n_neighbors=rec+1)
                
                # Create DataFrame with recommendations (excluding the selected film)
                df = pd.DataFrame()
                for x in indices:
                    for y in x[1:]:  # Skip first result (the film itself)
                        df = pd.concat([df, films.iloc[[y]]], ignore_index=True)
        
        else:  # Embedding method
            with st.spinner('Loading recommendations based on synopsis...'):
                try:
                    # Get selected film's imdb_id correctly
                    selected_film_imdb_id = films.loc[index, 'imdb_id']
                    
                    # Get actors for the selected film
                    actors_ids = bridge_df[bridge_df["imdb_id"] == selected_film_imdb_id]
                    
                    # Create text for ALL films, not just selected one
                    films_with_actors = []
                    for idx, film in films.iterrows():
                        film_imdb_id = film['imdb_id']
                        film_actors_ids = bridge_df[bridge_df["imdb_id"] == film_imdb_id]
                        
                        if not film_actors_ids.empty:
                            intervenants_df = pd.merge(
                                left=film_actors_ids, 
                                right=actors_df, 
                                how="left", 
                                left_on='principals_id', 
                                right_on='p_imdb_id'
                            )
                            actors_names = ', '.join(intervenants_df['name'].dropna().tolist())
                        else:
                            actors_names = "Unknown"
                        
                        # Create comprehensive text description
                        all_text = (
                            f"Keywords: {film.get('keywords', 'Unknown')}. "
                            f"Original language: {film.get('original_language', 'Unknown')}. "
                            f"Genre: {film.get('genres', 'Unknown')}. "
                            f"Actors names: {actors_names}."
                            f"Overview: {film.get('overview', 'Unknown')}" 
                        )
                        
                        films_with_actors.append({
                            'index': idx,
                            'all_text': all_text,
                            'imdb_id': film_imdb_id
                        })
                    
                    # Convert to DataFrame
                    films_text_df = pd.DataFrame(films_with_actors)
                    
                    # Filter out films without valid text
                    films_text_df = films_text_df[
                        films_text_df['all_text'].notna() & 
                        (films_text_df['all_text'].str.strip() != '')
                    ].copy()
                    
                    if films_text_df.empty:
                        st.error("No films with valid text descriptions found.")
                        return
                    
                    # Get text list for embeddings
                    text_list = films_text_df['all_text'].tolist()
                    
                    # Compute embeddings
                    embeddings = compute_embeddings(text_list)
                    
                    # Find the index of selected film in the filtered dataset
                    selected_film_row = films_text_df[films_text_df['index'] == index]
                    
                    if selected_film_row.empty:
                        st.error("Selected film doesn't have valid text description for embedding comparison.")
                        return
                    
                    # Get the position in the filtered dataset
                    selected_position = films_text_df.index[films_text_df['index'] == index].tolist()[0]
                    selected_vector = embeddings[selected_position]
                    
                    # Calculate cosine similarities
                    cosine_scores = util.cos_sim(selected_vector, embeddings)[0]
                    
                    # Convert to numpy and sort
                    cosine_scores_np = cosine_scores.cpu().numpy()
                    sorted_indices = np.argsort(-cosine_scores_np)
                    
                    # Get recommendations (excluding the selected film)
                    recommendations_positions = []
                    for idx in sorted_indices:
                        if idx != selected_position:  # Skip the selected film
                            recommendations_positions.append(idx)
                        if len(recommendations_positions) >= rec:
                            break
                    
                    # Get original film indices
                    original_indices = [films_text_df.iloc[pos]['index'] for pos in recommendations_positions]
                    
                    # Create DataFrame with recommendations
                    df = pd.DataFrame()
                    for orig_idx in original_indices:
                        df = pd.concat([df, films.iloc[[orig_idx]]], ignore_index=True)
                        
                except Exception as e:
                    st.error(f"Error in embedding method: {str(e)}")
                    return
        
        # Display recommendations
        if not df.empty:
            st.subheader('Recommended films')
            
            for i in range(0, len(df), col):
                cols = st.columns(col)
                films_subset = df.iloc[i:i+col]
                
                for j, film in enumerate(films_subset.itertuples()):
                    if j < len(cols):  # Safety check
                        with cols[j]:
                            # Handle missing poster
                            if pd.notna(film.poster_path) and film.poster_path:
                                st.image(film.poster_path, use_container_width=True)
                            else:
                                st.write("🎬 No poster available")
                            
                            st.markdown(f"""
                            **🎬 Film:** {film.original_title}  
                            **⭐ IMDb Rating:** {film.imdb_averageRating:.1f}  
                            **📅 Release Date:** {film.release_date}
                            """)
                            
                            film_url = f"/?page=Details&film_id={film.imdb_id}"
                            st.link_button(f'More details - {film.original_title}', film_url)
                            
                            yt_url = film._22
                            if isinstance(yt_url, str) and yt_url.strip() != '' and yt_url != 'Inconnu':
                                st.link_button(f'Trailer - {film.original_title}', yt_url)
        else:
            st.warning("No reccomandation found.")

def clear_cache():

    embeddings_file = 'embeddings_cache.pkl'
    if os.path.exists(embeddings_file):
        os.remove(embeddings_file)
        st.success("Cache embeddings cleaned!")

if st.sidebar.button("Clean cache embeddings"):
    clear_cache()