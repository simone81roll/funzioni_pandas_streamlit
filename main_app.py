import streamlit as st

st.set_page_config(page_title="Python - Funzioni Utili", page_icon="🐍", layout="wide") 

st.sidebar.image("python_logo.png", width=250) 

pages = {
    "Home":[
        st.Page("home.py", title="Home Page", icon=":material/home:"),
    ],
    "Analisi Dati":[
        st.Page("pandas_comand.py", title="Comandi Pandas", icon=":material/storage:"),
        st.Page("numpy_comand.py", title="Comandi NumPy", icon=":material/superscript:"),
        st.Page("grafici_comand.py", title="Realizzazione di grafici", icon=":material/pie_chart:"),
    ],
    "Gestione File e I/O":[
        st.Page("file_comand.py", title="Excel e CSV", icon=":material/folder_code:"),
    ],
    "Database":[
        st.Page("sqlite_comand.py", title="Principali comandi con SQLite3", icon=":material/database:"),
    ],
    "Sviluppo Web":[
        st.Page("email_comand.py", title="Invio e-mail", icon=":material/alternate_email:"),
        st.Page("jinja2_comand.py", title="HTML con Jinja2", icon=":material/code:"),    
    ],      
    "Strumenti Utili":[
        st.Page("task_comand.py", title="Task", icon=":material/checklist_rtl:"),
        st.Page("date_manipulation_comand.py", title="Manipolazione di date", icon=":material/today:"),
        st.Page("istruzioni.py", title="Info utili", icon=":material/info:"),
        st.Page("guida_deployment.py", title="Guida al deployment", icon=":material/deployed_code_update:"),
    ],      
    "Machine Learning":[
        st.Page("machine_learning_comand.py", title="Esempi pratici", icon=":material/batch_prediction:"),
    ],      
}

pg = st.navigation(pages)
pg.run()
