import streamlit as st

col1, col2 = st.columns([2, 1])  # Suddivisione delle colonne per un layout bilanciato
with col1:
    st.title("Benvenuto!")
    st.write("Questa applicazione è una guida rapida ai comandi e alle librerie più utili per l'analisi dati con Python.")
    
    st.subheader("Informazioni principali")
    st.write("Esplora le sezioni nel menu a sinistra per scoprire comandi per la manipolazione dati, la visualizzazione e molto altro.")
    st.info("💡 Usa il menu a sinistra per navigare tra le diverse sezioni.")

with col2:
    # 3. Gestione e ridimensionamento dell'immagine
    st.image("python_data_analyst.png", width=300)

# 5. Sezione Informazioni e Crediti con st.tabs
tab1, tab2 = st.tabs(["Informazioni", "Crediti"])
with tab1:
    st.header("Sezione Informazioni")
    st.write("Qui troverai dettagli utili sui vari comandi Python e sulle librerie più importanti")
with tab2:
    st.header("Sezione Crediti")
    st.write("App creata da **Simo Spirit**")
