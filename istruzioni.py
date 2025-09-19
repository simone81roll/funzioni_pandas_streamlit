import streamlit as st

st.subheader("ℹ️ Info Utili: Gestione del Progetto Python")
st.write(
    """
    Un buon progetto Python non si basa solo su un codice funzionante, ma anche su una struttura solida e riproducibile.
    Queste sono alcune pratiche fondamentali per gestire il tuo ambiente di sviluppo.
    """
)
st.write("---")

st.subheader("1. Come Creare un Ambiente Virtuale (`venv`)")
st.write(
    """
    **Cos'è?** Immagina un ambiente virtuale come una **scatola isolata** per ogni tuo progetto Python. All'interno di questa scatola, puoi installare le librerie che ti servono senza creare conflitti con altri progetti. È una pratica essenziale.
    """
)

st.write("#### Passo A: Creare l'ambiente")
st.write("Apri un terminale (o Prompt dei comandi su Windows) nella cartella del tuo progetto ed esegui questo comando. Di solito, l'ambiente viene chiamato `venv`.")
code_venv_create = "python -m venv venv"
st.code(code_venv_create, language='bash')

st.write("#### Passo B: Attivare l'ambiente")
st.write("L'attivazione va fatta ogni volta che inizi a lavorare sul progetto. Il comando cambia a seconda del tuo sistema operativo.")

st.write("**Su Windows (Prompt dei comandi):**")
code_venv_win = "venv\\Scripts\\activate"
st.code(code_venv_win, language='bash')

st.write("**Su macOS e Linux:**")
code_venv_unix = "source venv/bin/activate"
st.code(code_venv_unix, language='bash')
st.info("💡 Noterai che il nome dell'ambiente (`venv`) appare all'inizio della riga del terminale, a indicare che è attivo.")

st.write("#### Passo C: Disattivare l'ambiente")
st.write("Quando hai finito di lavorare, puoi disattivare l'ambiente con un semplice comando:")
code_venv_deactivate = "deactivate"
st.code(code_venv_deactivate, language='bash')

st.write("---")

st.subheader("2. Istruzioni per Creare il File `requirements.txt`")
st.write(
    """
    **Cos'è?** Il file `requirements.txt` è la **lista della spesa** del tuo progetto. Elenca tutte le librerie esterne necessarie (es. `streamlit`, `pandas`) con le loro versioni esatte. Questo permette a chiunque altro di ricreare il tuo ambiente di lavoro perfettamente.
    """
)

st.write("#### Passo A: Generare il file")
st.write("**Assicurati che il tuo ambiente virtuale sia attivo**, poi esegui questo comando. Creerà un file `requirements.txt` nella tua cartella.")
code_req_create = "pip freeze > requirements.txt"
st.code(code_req_create, language='bash')

st.write("#### Passo B: Installare le librerie da un file esistente")
st.write("Quando condividi il tuo progetto, un altro utente (o un servizio di hosting come Streamlit Community Cloud) userà questo comando per installare tutte le dipendenze necessarie in un colpo solo.")
code_req_install = "pip install -r requirements.txt"
st.code(code_req_install, language='bash')

st.write("---")

st.subheader("3. Link Utili 🔗")
st.write("Ecco una raccolta di link alle documentazioni ufficiali e a risorse utili che abbiamo menzionato in questa guida.")
st.markdown(
    """
    - **[Documentazione Ufficiale di Streamlit](https://docs.streamlit.io/)**: Il punto di partenza per tutto ciò che riguarda Streamlit.
    - **[Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)**: Un riassunto incredibilmente utile di tutti i comandi principali.
    - **[Documentazione di Pandas](https://pandas.pydata.org/docs/)**: Per ogni dubbio sulla manipolazione dei dati.
    - **[Documentazione di Plotly Express](https://plotly.com/python/plotly-express/)**: Gallerie di esempi per ogni tipo di grafico.
    - **[Guida Utente di Scikit-learn](https://scikit-learn.org/stable/user_guide.html)**: Per approfondire gli algoritmi di machine learning.
    - **[Documentazione Ufficiale di venv](https://docs.python.org/3/library/venv.html)**: Per conoscere tutti i dettagli sugli ambienti virtuali.
    """
)

st.write("---")

st.subheader("4. Sezione download 📥")
st.write("Download di applicativi utili per la gestione")
st.markdown(
    """
    - **[Sublime Text](https://www.sublimetext.com/download)**: Editor di testo per codice e markup.
    - **[DB Browser for SQLite](https://sqlitebrowser.org/dl/)**: Uno strumento visuale e open source per creare, cercare e modificare file di database SQLite.
    """
)