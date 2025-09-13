import streamlit as st

pages = {
    "Pandas":[
        st.Page("pandas_comand.py", title="Comandi Pandas", icon=":material/keyboard:"),
    ],
    "Numpy":[
        st.Page("numpy_comand.py", title="Comandi NumPy", icon=":material/keyboard:"),
    ],    
    "Excel e CSV":[
        st.Page("file_comand.py", title="Leggi/scrivi/salva/esporta", icon=":material/format_list_numbered:"),
    ],
    "DataBase":[
        st.Page("sqlite_comand.py", title="Principali comandi con SQLite3", icon=":material/analytics:"),
    ],
    "Varie":[
        st.Page("date_manipolation_comand.py", title="Operazioni sulle date", icon=":material/analytics:"),
        st.Page("istruzioni.py", title="Info utili", icon=":material/analytics:"),
    ],        
}

pg = st.navigation(pages)
pg.run()
