import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time
import sqlite3 as sq

with st.expander("**:inbox_tray: Import**"):
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

#************************************************************************************************************************************************************************************
with st.expander("**:hammer_and_wrench: Creazione tabella all'interno del database**"):
    st.write("#### 1. Funzione per la creazione della tabella")
    st.write("- **crea_tabella_dinamica(`conn, nome_tabella, colonne`)**: Questa è la nostra nuova funzione. Accetta la connessione (conn), il nome della tabella (nome_tabella) e la definizione delle colonne (colonne). Usiamo un dizionario per le colonne, perché ci permette di associare facilmente il nome della colonna (chiave) con il suo tipo di dato (valore).")
    st.write("- **Costruzione della query:** All'interno della funzione, il ciclo for itera sul dizionario colonne. Per ogni coppia (**nome_colonna, tipo_colonna**), crea una stringa come **Data Date** e la aggiunge alla lista colonne_sql.")
    st.write('- **`", ".join(colonne_sql)`**: Questo è un metodo molto utile per unire tutti gli elementi della lista colonne_sql in una singola stringa, separandoli con una virgola e uno spazio. Il risultato sarà una stringa come "id INTEGER PRIMARY KEY AUTOINCREMENT, Data Date, ...')
    st.write('- **Query finale: Usiamo una f-string (la stringa che inizia con f"...") per inserire in modo pulito il nome della tabella e la stringa delle colonne nella query CREATE TABLE.')
    st.write('- **`if __name__ == "__main__"`**: Questo blocco di codice è una pratica comune in Python. Il codice al suo interno viene eseguito solo quando il file viene avviato direttamente, non quando viene importato come modulo in un altro script. È un ottimo modo per mostrare un esempio di utilizzo.')    
    code_create = '''
def crea_tabella_dinamica(conn, nome_tabella, colonne):
    """
    Crea una tabella in un database SQLite in modo dinamico.

    Args:
        conn: L'oggetto di connessione al database.
        nome_tabella (str): Il nome della tabella da creare.
        colonne (dict): Un dizionario dove le chiavi sono i nomi delle colonne
                        e i valori sono i tipi di dati.
                        Esempio: {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'nome': 'TEXT'}
    """
    if not conn:
        st.error("Connessione al database non valida.")
        return

    cursor = conn.cursor()
    
    # Costruisci la stringa SQL per le colonne
    colonne_sql = []
    for nome_colonna, tipo_colonna in colonne.items():
        colonne_sql.append(f"{nome_colonna} {tipo_colonna}")
    
    colonne_stringa = ", ".join(colonne_sql)

    # Costruisci la query completa
    create_table_query = f"CREATE TABLE IF NOT EXISTS {nome_tabella} ({colonne_stringa})"

    try:
        cursor.execute(create_table_query)
        conn.commit()
        st.success(f"Tabella '{nome_tabella}' creata con successo.")
    except sq.Error as e:
        st.error(f"Errore nella creazione della tabella: {e}")
    '''
    st.code(code_create, language='python')

    st.write("#### 2. Esempi di utilizzo")
    code_esempio = '''
if __name__ == "__main__":
    # 1. Ottieni la connessione al database
    conn = get_db_connection()

    if conn:
        # 2. Definisci la struttura della tabella
        struttura_report = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'Data': 'Date',
            'Chiamate_Offerte': 'INT',
            'Chiamate_Gestite': 'INT',
            'Abbandonate': 'INT',
            'Gestito_entro_30': 'INT',
            'TMG': 'INT',
            'SLA': 'REAL',
            'AR': 'REAL'
        }

        # 3. Chiama la funzione per creare la tabella
        crea_tabella_dinamica(conn, "report_giornaliero", struttura_report)

        # Esempio di creazione di un'altra tabella
        struttura_utenti = {
            'id_utente': 'INTEGER PRIMARY KEY',
            'nome_utente': 'TEXT NOT NULL',
            'email': 'TEXT NOT NULL UNIQUE'
        }
        crea_tabella_dinamica(conn, "AnagraficaClienti", struttura_utenti)
        
        # 4. Chiudi la connessione
        conn.close()
    '''
    st.code(code_esempio, language='python')




#************************************************************************************************************************************************************************************
with st.expander("**:bar_chart: Visualizza i dati**"):
    st.write("#### Funzione per la visualizzazione dei dati caricati")
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

#************************************************************************************************************************************************************************************
with st.expander("**:wastebasket: Eliminazione Record**"):
    st.write("#### 1. Eliminare tabella")
    
    code_delete_table = '''
def elimina_tabella():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {tab_name}")

    conn.commit()
    conn.close()

# Esempio di utilizzo
tab_name = 'xxxxxxxxxx'
if st.button('Elimina Tabella'):
    elimina_tabella()
    '''
    st.code(code_delete_table, language='python')


    st.write("#### 2. Eliminare tutti i record")
    
    code_delete_all = '''
def svuota_tab():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tab_name}")
    conn.commit()
    conn.close()

tab_name = 'xxxxxxxxxx'

if st.button('Svuota Tabella'):
    svuota_tabella()
    '''
    st.code(code_delete_all, language='python')

    st.write("#### 3. Eliminare dei record in base ad un elenco")

    st.write("**Panoramica della soluzione**")
    st.write("Creeremo una funzione chiamata elimina_record_dinamicamente che accetterà:")
    st.write("- **`conn:`** L'oggetto di connessione al database.")
    st.write("- **`nome_tabella:`** Il nome della tabella da cui eliminare i dati.")
    st.write("- **`nome_colonna:`** Il nome della colonna da usare come criterio di eliminazione.")
    st.write("- **`valori_da_eliminare:`** Una lista dei valori da cercare nella colonna.")
    st.write("Questa funzione creerà una query DELETE in modo sicuro e dinamico, prevenendo problemi come SQL injection.")

    code_delete = '''
def elimina_record_dinamicamente(conn, nome_tabella, nome_colonna, valori_da_eliminare):

    if not conn:
        st.error("Connessione al database non valida.")
        return

    cursor = conn.cursor()
    
    # Costruisci una stringa con i placeholder (?, ?, ...)
    placeholders = ', '.join(['?'] * len(valori_da_eliminare))
    
    # Costruisci la query di eliminazione in modo sicuro
    query = f"DELETE FROM {nome_tabella} WHERE {nome_colonna} IN ({placeholders})"
    
    try:
        cursor.execute(query, valori_da_eliminare)
        conn.commit()
        st.success(f"{cursor.rowcount} record eliminati con successo dalla tabella '{nome_tabella}'.")
    except sq.Error as e:
        st.error(f"Errore durante l'eliminazione dei record: {e}")

    '''
    st.code(code_delete, language='python')

    st.write("#### 4. Esempi di utilizzo")
    
    code_esempio = '''        

# --- Esempio di utilizzo ---
if __name__ == "__main__":
    # 1. Ottieni la connessione al database
    conn = get_db_connection()

    if conn:
        # 2. Definisci i valori da eliminare e le informazioni della tabella
        valori_file_da_eliminare = [
            'utilities_no_extralista_20250720.csv',
            'utilities_no_extralista_20250719.csv',
            'utilities_no_extralista_20250718.csv',
            'utilities_no_extralista_20250717.csv',
            'utilities_no_extralista_20250716.csv',
            'utilities_extralista_20250720.csv',
            'utilities_extralista_20250719.csv',
            'utilities_extralista_20250718.csv',
            'utilities_extralista_20250717.csv',
            'utilities_extralista_20250716.csv'
        ]

        # 3. Chiama la funzione per eliminare i record
        elimina_record_dinamicamente(conn, "CMB_utenti", "File_name", valori_file_da_eliminare)
        
        # 4. Chiudi la connessione
        conn.close()
    '''
    st.code(code_esempio, language='python')

    st.write("**Spiegazione dei passaggi**")
    st.write("- `elimina_record_dinamicamente(conn, nome_tabella, nome_colonna, valori_da_eliminare)`: Questa funzione accetta gli argomenti che rendono l'operazione flessibile: la connessione, il nome della tabella, la colonna di riferimento e la lista di valori da eliminare.")
    st.write("- `placeholders = ', '.join(['?'] * len(valori_da_eliminare))`: Questa riga crea una stringa di placeholder per i parametri della query (?). È fondamentale per evitare problemi di sicurezza (SQL injection) e gestisce automaticamente il numero corretto di placeholder in base alla lunghezza della lista valori_da_eliminare.")
    st.write("- `query = f'DELETE FROM {nome_tabella} WHERE {nome_colonna} IN ({placeholders})'`: Questa f-string crea la query SQL completa. Invece di inserire direttamente i valori nella stringa, usiamo i placeholder (?) per una gestione sicura dei parametri.")
    st.write("- `cursor.execute(query, valori_da_eliminare)`: Quando esegui la query, passi la lista valori_da_eliminare come secondo argomento al metodo execute. sqlite3 si occupa di sostituire ogni ? con il valore corrispondente dalla lista in modo sicuro.")
    st.write("- `cursor.rowcount`: Dopo aver eseguito la query, cursor.rowcount ti restituisce il numero di righe che sono state modificate o eliminate, il che è utile per dare un feedback all'utente.")
