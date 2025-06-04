import streamlit as st 
import pandas as pd 
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
# Imports
from sentence_transformers import SentenceTransformer, util
import pandas as pd 
import numpy as np 



films = pd.read_csv('TMDb_IMDb_full.csv')
# Encoding Genres
X = films['genres'].str.get_dummies(sep=',')
X['original_language'] = films['original_language'].replace({'en':1,'fr':0}) * 5
# Normalize numeric values
mms = MinMaxScaler()
X['vote_normalized'] = mms.fit_transform(films[['imdb_averageRating']]) * 5
films['popularity'] = films['popularity'].replace('Inconnu', 0)
X['popularity'] = mms.fit_transform(films[['popularity']]) * 5
X['runtimeMinutes'] = mms.fit_transform(films[['runtimeMinutes']])



def show_search():
    st.title("🔍 Trouvez des films qui vous ressemblent")
    st.write('Trouvez facilement un film en utilisant le menu déroulant ou en tapant un titre dans la barre de recherche pour vérifier s’il figure dans notre base de données. Une fois votre film sélectionné, nous vous proposons une liste de films similaires. Sous chaque affiche, vous pouvez cliquer sur un bouton pour obtenir plus d’informations détaillées sur le film : synopsis, casting, durée et plus encore. Votre prochaine soirée cinéma commence ici !')
    st.sidebar.header('Select the filter you want to change : ')
    rec = st.sidebar.select_slider(
        'Select how many reccomandations you want :',
        options = [2, 3, 4, 5, 6, 7, 8, 9, 10],
        value=(6)
    )
    col = st.sidebar.select_slider(
        'Select how many films you want to see per row : ',
        options=[3,4,5,6,7,8,9,10],
        value=5
    )
    choice = st.radio('Select the reccomendation method',
                      ['NearestNeighbors', 'Embeding'],
                      captions=[
                          'Similarity in genres',
                          'Similarity in synopsis'
                      ],
                      )
    
    # Training the model
    knn = NearestNeighbors(n_neighbors=rec, metric='euclidean')
    knn.fit(X)
    option = st.selectbox('Choose a film to get reccomandations: ',films['original_title'].to_list())
    sinossi_list = films['overview'].tolist()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Get index film test
    index = films[films['original_title'] == option].index[0]
    if choice == 'NearestNeighbors':
        distances, indices = knn.kneighbors(X.iloc[[index]], n_neighbors=rec)
        for x in indices:
            for y in x[1:]:
                print(films.loc[y,'original_title'])
        df = pd.DataFrame()
        for x in indices:
            for y in x[1:]:
                df = pd.concat([df,films.iloc[[y]]])
        st.subheader('Reccomended films')
        df = df.reset_index(drop=True)
        for i in range(0, len(df), col):
            cols = st.columns(col)  # Una riga con `col` colonne
            films_subset = df.iloc[i:i+col]
            for j, film in enumerate(films_subset.itertuples()):
                with cols[j]:
                    st.image(film.poster_path)
                    st.markdown(f"""
                    **🎬 Film:** {film.original_title}  
                    **⭐ IMDb Rating:** {int(film.imdb_averageRating)}  
                    **📅 Release Date:** {film.release_date}
                    """)
                    film_url = f"/?page=Details&film_id={film.imdb_id}"
                    st.link_button(f'More details - {film.original_title}',film_url)
    else :
        embeddings = model.encode(sinossi_list, convert_to_tensor=True)
        selected_vector = embeddings[index]
        cosine_scores = util.cos_sim(selected_vector, embeddings)[0]
        cosine_scores_np = cosine_scores.cpu().numpy()
        sorted_index = np.argsort(-cosine_scores_np)
        reccomendations = [i for i in sorted_index if i != index][:rec-1]
        df = pd.DataFrame()
        for x in reccomendations:
                df = pd.concat([df,films.iloc[[int(x)]]], ignore_index=True)
        st.subheader('Reccomended films')
        df = df.reset_index(drop=True)
        for i in range(0, len(df), col):
            cols = st.columns(col)  # Una riga con `col` colonne
            films_subset = df.iloc[i:i+col]
            for j, film in enumerate(films_subset.itertuples()):
                with cols[j]:
                    st.image(film.poster_path)
                    st.markdown(f"""
                    **🎬 Film:** {film.original_title}  
                    **⭐ IMDb Rating:** {int(film.imdb_averageRating)}  
                    **📅 Release Date:** {film.release_date}
                    """)
                    film_url = f"/?page=Details&film_id={film.imdb_id}"
                    st.link_button(f'More details - {film.original_title}',film_url)
