import streamlit as st
import streamlit.components.v1 as components

try:
    with open("streamlit_deployment_guide.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Mostra l'HTML all'interno dell'app Streamlit
    components.html(html_content, height=1200, scrolling=True)

except FileNotFoundError:
    st.error("Errore: Il file 'streamlit_deployment_guide.html' non è stato trovato. Assicurati che si trovi nella stessa cartella dello script.")
except Exception as e:
    st.error(f"Si è verificato un errore: {e}")