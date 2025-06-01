import streamlit as st 
import random
import pandas as pd 

films = pd.read_csv('TMDb_IMDb_full.csv')
def show_home():
    st.title('🏠 Welcome to the Homepage')
    
    st.session_state.random_indices = None

    # Refresh button
    if st.button("🎲 Discover other films"):
        st.session_state.random_indices = random.sample(range(len(films)), 5)

    # Visualize films

        random_films = films.sample(5, random_state=random.randint(1,len(films)))
        random_films = random_films.reset_index()
        st.subheader('Some films')
        cols = st.columns(5)
        for i in range(0,5):
            image = random_films.loc[i,'poster_path']
            name = random_films.loc[i,'original_title']
            rating = int(random_films.loc[i,"imdb_averageRating"])
            release_date = random_films.loc[i,"release_date"]
            with cols[i]:
                st.image(image)
                st.markdown(f"""
                **🎬 Nom du film :** {name}  
                **⭐ Note IMDb :** {rating}  
                **📅 Date de sortie :** {release_date}
                """)

