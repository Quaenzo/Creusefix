import streamlit as st
import pandas as pd
import requests

# Load CSV
movies_df = pd.read_csv("TMDb_IMDb_full.csv")
actors_df = pd.read_csv("Intervenants.csv")
bridge_df = pd.read_csv('Table__Intermediare.csv.csv')
def show_details():
    st.title("🎬 Plus d'infos sur les films")

    film_id = st.query_params.get("film_id")

    if isinstance(film_id, list):
        film_id = film_id[0]

    if not film_id:
        st.error("❌ Aucun film sélectionné.")
        return

    if film_id.endswith(".0"):
        film_id = film_id[:-2]
        
    film_id = film_id

    movie_data = movies_df[movies_df["imdb_id"] == film_id]
    if movie_data.empty:
        st.error("❌ Film introuvable.")
        return

    movie_data = movie_data.iloc[0]
    selected_movie = movie_data["original_title"]
    poster_url = movie_data["poster_path"]
    overview = movie_data["overview"]
    rating = movie_data["imdb_averageRating"]

    st.image(poster_url, caption=selected_movie, use_container_width=50)
    st.markdown(f"**Note moyenne** : {rating}/10")
    st.markdown(f"**Synopsis** : {overview}")



    st.markdown("### 🎭 Acteurs & Intervenants")

    # 🔗 Estrai le persone collegate al film
    actors_ids = bridge_df[bridge_df["imdb_id"] == film_id]
    intervenants_df = pd.merge(left= actors_ids, right = actors_df, how="left", left_on='principals_id', right_on='p_imdb_id')
    if intervenants_df.empty:
        st.warning("Aucun intervenant trouvé pour ce film.")
        return
    col = st.sidebar.select_slider(
        'Select how many actors you want to see per row : ',
        options=[3,4,5,6,7,8,9,10],
        value=5 )
    intervenants_df.dropna(inplace=True)
    intervenants_df.drop_duplicates(subset=['p_imdb_id'],inplace=True)
    st.subheader('Actors :')
    for i in range(0, len(intervenants_df), col):
        cols = st.columns(col)  # Una riga con `col` colonne
        actor_subset = intervenants_df.iloc[i:i+col]
        actor_subset = actor_subset.dropna()

        for j, actor in enumerate(actor_subset.itertuples()):
            with cols[j]:
                image = getattr(actor, "profile_path", None)
                name_raw = getattr(actor, "name", "")
            
                if pd.isna(name_raw):
                    name = "Inconnu"
                    wiki_url = None
                else:
                    name = str(name_raw)
                    wiki_url = f"https://it.wikipedia.org/wiki/{name.replace(' ', '_')}"               
                    
                st.markdown(f"**🎭 {name}**")
                if image and not pd.isna(image):
                    st.image(image, width=250)
                else:
                    st.markdown("🖼️ Image non disponible")

                if wiki_url:
                    st.markdown(f"🔹 [Biographie Wikipedia]({wiki_url})")
                else:
                    st.markdown("⚠ Biographie non trouvée")