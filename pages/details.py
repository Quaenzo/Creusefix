# import streamlit as st
# import pandas as pd
# import requests


# # ✅ Charger les fichiers CSV
# movies_df = pd.read_csv("TMDb_IMDb_full.csv")
# actors_df = pd.read_csv("Intervenants.csv")
# def show_details():
#     st.title("🎬 Plus d'infos sur les films")


#     # ✅ Sélectionner un film dans une liste déroulante
#     selected_movie = st.selectbox("Choisis un film :", movies_df["original_title"].unique())

#     # ✅ Filtrer les données pour le film sélectionné
#     movie_data = movies_df[movies_df["original_title"] == selected_movie].iloc[0]
#     poster_url = movie_data["poster_path"]  # Vérifie que cette colonne contient bien une URL complète
#     overview = movie_data["overview"]
#     rating = movie_data["imdb_averageRating"]

#     # ✅ Afficher l'affiche et les informations du film
#     #st.image(poster_url, caption=selected_movie, use_column_width=200)
#     st.image(poster_url, caption=selected_movie, use_container_width=50)
#     st.markdown(f"**Note moyenne** : {rating}/10")
#     st.markdown(f"**Synopsis** : {overview}")


#     st.markdown("### 🎭 Acteurs")

#     # ✅ Créer des colonnes pour afficher les acteurs en ligne
#     cols = st.columns(4)  # Ajuste selon le nombre d'acteurs à afficher

#     for index, row in actors_df.iterrows():
#         with cols[index % 4]:  # Répartit les acteurs sur plusieurs colonnes
#             st.image(row["profile_path"], width=150)  # ✅ Réduit la taille des images
#             st.markdown(f"**🎭 {row['name']}**")
#             st.markdown(f"🔹 [Voir sur Wikipedia]({row['wikipedia_url']})")



#     # ✅ Afficher les intervenants
#     st.markdown("### 🎭 Acteurs & Intervenants")

#     # ✅ Filtrer les acteurs du film sélectionné
#     actors = actors_df[actors_df["original_title"] == selected_movie]

#     for _, row in actors.iterrows():
#         actor_name = row["name"]
#         wiki_url = row["wikipedia_url"]

#         st.markdown(f"**🎭 {actor_name}**")
#         if pd.notna(wiki_url):  # Vérifie que le lien existe
#             st.markdown(f"🔹 [Biographie Wikipedia]({wiki_url})")
#         else:
#             st.markdown("⚠ Biographie non trouvée")

#     # ✅ Afficher plusieurs affiches aléatoires
#     st.markdown("### 🎬 Autres Films Disponibles")

#     # ✅ Créer des colonnes pour afficher plusieurs affiches
#     cols = st.columns(4)  # Ajuste selon le nombre d'affiches

#     for index, row in movies_df.sample(8).iterrows():  # Affiche 8 films aléatoires
#         with cols[index % 4]:  # Répartit les affiches sur 4 colonnes
#             st.image(row["poster_path"], caption=row["original_title"], use_column_width=True)
import streamlit as st
import pandas as pd
import requests

# ✅ Carica i file CSV
movies_df = pd.read_csv("TMDb_IMDb_full.csv")
actors_df = pd.read_csv("Intervenants.csv")
def show_details():
    st.title("🎬 Plus d'infos sur les films")

    film_id = st.query_params.get("film_id")

    if isinstance(film_id, list):
        film_id = film_id[0]

    if not film_id:
        st.error("❌ Aucun film sélectionné.")
        return

    # Rimuovi eventuale .0 finale (tipico float convertito in stringa)
    if film_id.endswith(".0"):
        film_id = film_id[:-2]

    if not film_id.isdigit():
        st.error(f"❌ ID du film non valide: '{film_id}'")
        return

    film_id = int(film_id)
    #st.write(f"✅ film_id convertito in int: {film_id}")

# def show_details():
#     st.title("🎬 Plus d'infos sur les films")

#     # ✅ Ottieni l'ID film dall'URL
#     film_id = st.query_params.get("film_id")

# # Se il parametro è una lista, prendi il primo valore
#     if isinstance(film_id, list):
#         film_id = film_id[0]

#     # Verifica se il valore è valido
#     if not film_id or not film_id.isdigit():
#         st.error("❌ ID du film non valide ou manquant.")
#         return

#     film_id = int(film_id)

#     if not film_id:
#         st.error("❌ Aucun film sélectionné.")
#         return

#     try:
#         film_id = int(film_id)
#     except ValueError:
#         st.error("❌ ID du film non valide.")
#         return

    # ✅ Filtra il film tramite l'ID
    movie_data = movies_df[movies_df["tmdb_id"] == film_id]
    if movie_data.empty:
        st.error("❌ Film introuvable.")
        return

    movie_data = movie_data.iloc[0]
    selected_movie = movie_data["original_title"]
    poster_url = movie_data["poster_path"]
    overview = movie_data["overview"]
    rating = movie_data["imdb_averageRating"]

    # ✅ Visualizza poster e informazioni
    st.image(poster_url, caption=selected_movie, use_container_width=50)
    st.markdown(f"**Note moyenne** : {rating}/10")
    st.markdown(f"**Synopsis** : {overview}")

    # # ✅ Sezione attori (generica)
    # st.markdown("### 🎭 Acteurs")
    # cols = st.columns(4)
    # for index, row in actors_df.iterrows():
    #     with cols[index % 4]:
    #         st.image(row["profile_path"], width=150)
    #         st.markdown(f"**🎭 {row['name']}**")
    #         url = 'https://it.wikipedia.org/wiki/' + row['name']
    #         st.markdown(f"🔹 [Voir sur Wikipedia]({url})")

    # ✅ Attori specifici del film
    st.markdown("### 🎭 Acteurs & Intervenants")
    actors = actors_df[actors_df["original_title"] == selected_movie]
    for _, row in actors.iterrows():
        actor_name = row["name"]
        url = 'https://it.wikipedia.org/wiki/' + row['name']
        wiki_url = url
        st.markdown(f"**🎭 {actor_name}**")
        if pd.notna(wiki_url):
            st.markdown(f"🔹 [Biographie Wikipedia]({wiki_url})")
        else:
            st.markdown("⚠ Biographie non trouvée")

    # # ✅ Altri film casuali
    # st.markdown("### 🎬 Autres Films Disponibles")
    # cols = st.columns(4)
    # for index, row in movies_df.sample(8).iterrows():
    #     with cols[index % 4]:
    #         st.image(row["poster_path"], caption=row["original_title"], use_column_width=True)
