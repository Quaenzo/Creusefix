import streamlit as st 
import random
import pandas as pd 

films = pd.read_csv('TMDb_IMDb_full.csv')
def show_home():
    st.title('🏠 Bienvenue sur Creusefix – Votre guide cinéma personnalisé')
    st.write('''Découvrez Creusefix, le moteur de recommandation de films conçu pour les amoureux du cinéma en Creuse. Entrez un film que vous aimez, et laissez notre système intelligent vous proposer des films similaires qui correspondent à vos goûts.
                    Envie de découvrir quelque chose de nouveau ?
                    En bas de la page, cliquez sur le bouton pour obtenir une sélection aléatoire de 5 films tirés de notre base de données – avec titre, note et date de sortie. Une manière rapide et amusante d’explorer notre catalogue !''')
    st.session_state.random_indices = None

    # Bottone per aggiornare
    if st.button("🎲 Discover other films"):
        st.session_state.random_indices = random.sample(range(len(films)), 5)

    # Visualizzazione film

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

