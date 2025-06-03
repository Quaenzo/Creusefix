import streamlit as st 

def show_contact():
    st.title("📩 Contactez-nous")
    st.write("Remplissez le formulaire ci-dessous pour nous envoyer un message.")

    #Formulaire de contact
    with st.form(key="contact_form", clear_on_submit=True):
        name = st.text_input("👤 Votre Nom")
        email = st.text_input("📧 Votre Email")
        subject = st.text_input("📌 Sujet du message")
        message = st.text_area("💬 Votre Message")

        # 🔘 Bouton d’envoi
        submit_button = st.form_submit_button("Envoyer")

    #Message de confirmation
    if submit_button:
        st.success("✅ Votre message a été envoyé avec succès !")