import streamlit as st
import speech_recognition as sr
import time


# Fonction pour la reconnaissance vocale
def transcribe_speech(api='google', language='en-US'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙️ Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        if api == 'google':
            text = recognizer.recognize_google(audio, language=language)
        elif api == 'sphinx':
            text = recognizer.recognize_sphinx(audio, language=language)
        else:
            raise ValueError("API non prise en charge.")

        st.write("📝 Texte reconnu :", text)
        return text
    except sr.UnknownValueError:
        st.error("❌ Impossible de reconnaître l'audio.")
    except sr.RequestError as e:
        st.error(f"⚠️ Erreur avec le service de reconnaissance vocale : {e}")
    except Exception as e:
        st.error(f"🚨 Erreur inattendue : {e}")
    return None


# Fonction pour sauvegarder le texte transcrit dans un fichier
def save_transcription(text, filename="transcription.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    st.success(f"✅ Texte enregistré dans {filename}")


# Fonction principale
def main():
    st.title("Reconnaissance Vocale avec Streamlit")

    # Choix de l'API et de la langue
    api_choice = st.selectbox("Choisissez l'API", ['google', 'sphinx'])
    language_choice = st.text_input("Entrez le code de la langue (ex: fr-FR, en-US)", 'en-US')

    # Variables pour la gestion de l'enregistrement et de l'arrêt
    if 'running' not in st.session_state:
        st.session_state.running = False

    # Logique pour démarrer la reconnaissance vocale
    if st.button("Commencer la reconnaissance vocale"):
        st.session_state.running = True
        text = transcribe_speech(api=api_choice, language=language_choice)
        if text:
            if st.button("Enregistrer le texte transcrit"):
                save_transcription(text)
        else:
            st.write("❌ Aucune transcription effectuée.")

    # Si la reconnaissance est en cours, afficher le bouton "Arrêter"
    if st.session_state.running:
        stop_button = st.button("Arrêter la reconnaissance vocale")
        if stop_button:
            st.session_state.running = False
            st.write("⏹️ Reconnaissance vocale arrêtée.")

    if not st.session_state.running:
        st.write("❗ Appuyez sur 'Commencer la reconnaissance vocale' pour démarrer.")


if __name__ == "__main__":
    main()
