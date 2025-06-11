import streamlit as st 
import pandas as pd 
import time
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from google.genai.types import HttpOptions, ModelContent, Part, UserContent

films = pd.read_csv('TMDb_IMDb_full.csv')
actors_df = pd.read_csv("Intervenants.csv")
bridge_df = pd.read_csv('Table__Intermediare.csv.csv') 
load_dotenv(dotenv_path="pages/key.env")
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """Vous êtes un spécialiste de tout ce qui touche au cinéma et aux films. Vous donnez des réponses précises et cohérentes avec l'argumentation.
Vous donnez des suggestions basées sur ce que l'utilisateur aime, mais sur la base des ensembles de données fournis, tels que les dataframe 'films' et 'actors_df', téléchargées sur cette page, et le dataframe 'bridge_df', qui sert de pont entre les deux, sans mentionner où vous avez obtenu l'information. Si la question n'est pas en rapport avec le sujet, dites à l'utilisateur que vous n'êtes spécialisé que dans cette branche."""

chat = client.chats.create(
    model = "gemini-2.5-flash-preview-05-20",
    history = [
        UserContent(parts=[Part(text="Hello")]),
        ModelContent(parts=[Part(text="Great to meet you. What would you like to know?")])
    ]
)

chat.send_message(system_prompt)

def chatbot():
    
    st.title("🧠Le spécialiste de le Cinema e des Films🧠")
    
    st.markdown(
        """
        Bienvenue ! Je suis un spécialiste de l'art Cinematographique.
        Posez-moi vos questions sur le **Cinema**, votre  **Films preferé** et les **intervenants**.
        """
    )
    st.markdown("---")
    
    user_question = st.text_area("Votre question : ", height= 100, placeholder="Quel film conseilleriez-vous à un amateur de comédie ?")
    
    if st.button("Poser la question", help="Cliquez pour obtenir une réponse"):
        if user_question:
            with st.spinner("Analyse de votre question et préparation de la réponse..."):
                time.sleep(10)
                response = chat.send_message_stream(user_question)
            for chunk in response:
                st.write(chunk.text, end="")
