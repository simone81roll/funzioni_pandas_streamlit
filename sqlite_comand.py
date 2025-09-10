import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time
import sqlite3 as sq

with st.expander("**:black_square_button: Import**"):
    code = '''
    import sqlite3 as sq
    '''
    st.code(code, language="python")

#************************************************************************************************************************************************************************************
with st.expander("**:computer: Interagire con un Database SQLite**"):
    st.write(
        """
        Spesso i dati non si trovano in file, ma in un database. Pandas può leggere dati
        direttamente da un database SQL con poche righe di codice.
        
        Qui mostriamo un esempio di come connettersi a un database SQLite e caricare
        una tabella in un DataFrame.
        """
    )
    
    st.info("Nota: questo codice presuppone che esista un file di database `.db` nel percorso specificato e che contenga una tabella.")

    st.write("#### 1. Funzione per la connessione al Database")
    code_conn = '''

def get_db_connection():
    # Sostituisci con il percorso reale del tuo file .db
    path_db = "percorso/al/tuo/database.db"
    conn = sq.connect(path_db)
    return conn
    '''
    st.code(code_conn, language='python')

    st.write("#### 2. Funzione per caricare i dati")
    code_load = '''
def load_data(tab_name):
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM {tab_name}"
        df_database = pd.read_sql(query, conn)
        conn.close()
        return df_database
    except Exception as e:
        st.error(f"Errore nel caricamento dati: {e}")
        return pd.DataFrame() # Ritorna un df vuoto in caso di errore

# Esempio di utilizzo:
# nome_tabella = 'AnagraficaClienti'
# df_clienti_da_db = load_data(nome_tabella)
# st.dataframe(df_clienti_da_db)
    '''
    st.code(code_load, language='python')