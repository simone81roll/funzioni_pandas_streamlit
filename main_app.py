import streamlit as st

st.set_page_config(page_title="Python - Funzioni Utili", page_icon="🐍", layout="wide") 

st.sidebar.image("python_logo.png", width=250) 

pages = {
    "Home":[
        st.Page("home.py", title="Home Page", icon=":material/home:"),
    ],
    "Pandas":[
        st.Page("pandas_comand.py", title="Comandi Pandas", icon=":material/data_table:"),
    ],
    "Numpy":[
        st.Page("numpy_comand.py", title="Comandi NumPy", icon=":material/calculate:"),
    ],    
    "Excel e CSV":[
        st.Page("file_comand.py", title="Leggi/scrivi/salva/esporta", icon=":material/folder:"),
    ],
    "DataBase":[
        st.Page("sqlite_comand.py", title="Principali comandi con SQLite3", icon=":material/database:"),
    ],
    "HTML":[
        st.Page("jinja2_comand.py", title="Principali comandi con Jinja2", icon=":material/code:"),
    ],   
    "e-mail":[
        st.Page("email_comand.py", title="Principali comandi per l'invio di mail", icon=":material/alternate_email:"),
    ],      
    "Grafici":[
        st.Page("grafici_comand.py", title="Realizzazione di grafici", icon=":material/pie_chart:"),
    ],   
    "Machine Learning":[
        st.Page("machine_learning_comand.py", title="Esempi pratici di Machine Learning", icon=":material/batch_prediction:"),
    ],            
    "Varie":[
        st.Page("date_manipolation_comand.py", title="Operazioni sulle date", icon=":material/today:"), # Ho corretto il typo qui
        st.Page("istruzioni.py", title="Info utili", icon=":material/info:"),
    ],        
}

pg = st.navigation(pages)
pg.run()
