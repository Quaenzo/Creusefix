import streamlit as st 



def show_about():
    st.title("ℹ️ About our team")
    cols = st.columns(2)
    with cols[0]:
        st.write("""Bienvenue sur le Streamlit de notre projet 👨‍👨‍👧‍👦

Nous sommes CulturAgency Harmony et notre équipe est composée de :

Anne-Laure : Product Owner

Seydoux : Scrum Master

Ben : Developer Python

Fabiano : Code reviewer

Nous avons été contactés par un directeur de cinéma éprouvant des difficultés à relancer son activité. L'établissement étant situé dans la Creuse, il nous a demandé conseil pour avoir une liste de recommandations de films à diffuser à un large public.
Pour ce faire, nous avons établi un plan d'action en trois étapes :

Récupération des databases sur le site internet IMDb et TMDb afin d'avoir un large éventail de données sur les films. Un tri a été fait avec Visual Studio Code parmi toutes ses informations pour récupérer celles qui nous seront utiles par rapport au public visé.

Création d'un algorithme de Machine Learning qui sortira une liste de films en fonction des paramètres établis par le client.
Importation des données sur PowerBI pour avoir une visualisation des données triées. Cela permettra également d'avoir une interface propre pour permettre au client de saisir ses paramètres et ainsi d'avoir sa recommandation de films. 

Nous nous sommes servis de plusieurs bibliothèques sous Python comme Pandas pour faire du nettoyage et filtrage de données parmi les databases à disposition. Nous avons utilisé la méthode des proches voisins comme algorithme d'apprentissage automatique supervisé pour la partie Machine Learning. Il a été nécessaire de faire des choix dans l'utilisation des données pour que le système soit simple d'utilisation et pertinent pour le client.""")
    with cols[1]:
        st.image('images/Logo.png',width=500)
        
