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
with st.expander("**:hammer_and_wrench: Creazione tabella all'interno del database (CREATE TABLE)**"):
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
with st.expander("**:bar_chart: Visualizza i dati (SELECT)**"):
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

#***********************************************************************************************************************************************************************************

with st.expander("**:heavy_plus_sign: Inserimento di Dati (INSERT)**"):
    st.write(
        """
        Una volta creata una tabella, è necessario popolarla con i dati.
        Questa sezione mostra come inserire una o più righe in modo dinamico e sicuro,
        partendo da una lista di dati.
        """
    )
    
    st.write("#### 1. Funzione per l'inserimento dinamico")
    st.info(
        """
        La funzione `insert_data_dinamicamente` è progettata per essere molto efficiente. 
        Utilizza `cursor.executemany()`, che è il metodo ottimale per inserire
        più righe in una singola operazione, riducendo il carico sul database.
        """
    )

    def insert_data_dinamicamente(conn, nome_tabella, dati_da_inserire):

        if not conn or not dati_da_inserire:
            st.warning("Connessione non valida o nessun dato da inserire.")
            return

        cursor = conn.cursor()
        
        # Prendi i nomi delle colonne dal primo dizionario
        colonne = dati_da_inserire[0].keys()
        colonne_stringa = ", ".join(colonne)
        
        # Crea i placeholder (?, ?, ...) in base al numero di colonne
        placeholders = ", ".join(['?'] * len(colonne))
        
        query = f"INSERT INTO {nome_tabella} ({colonne_stringa}) VALUES ({placeholders})"
        
        # Prepara i dati come una lista di tuple
        dati_tuple = [tuple(riga.values()) for riga in dati_da_inserire]
        
        try:
            # Usa executemany per inserire tutte le righe in modo efficiente
            cursor.executemany(query, dati_tuple)
            conn.commit()
            st.success(f"{cursor.rowcount} record inseriti con successo nella tabella '{nome_tabella}'.")
        except sq.Error as e:
            st.error(f"Errore durante l'inserimento dei dati: {e}")
    
    code_insert = '''
def insert_data_dinamicamente(conn, nome_tabella, dati_da_inserire):
    """
    Inserisce una lista di righe in una tabella in modo dinamico.

    Args:
        conn: L'oggetto di connessione al database.
        nome_tabella (str): Il nome della tabella in cui inserire i dati.
        dati_da_inserire (list of dict): Una lista di dizionari, dove ogni
                                         dizionario rappresenta una riga.
                                         Esempio: [{'nome': 'Mario', 'email': 'mario@test.it'}]
    """
    if not conn or not dati_da_inserire:
        st.warning("Connessione non valida o nessun dato da inserire.")
        return

    cursor = conn.cursor()
    
    # Prendi i nomi delle colonne dal primo dizionario
    colonne = dati_da_inserire[0].keys()
    colonne_stringa = ", ".join(colonne)
    
    # Crea i placeholder (?, ?, ...) in base al numero di colonne
    placeholders = ", ".join(['?'] * len(colonne))
    
    query = f"INSERT INTO {nome_tabella} ({colonne_stringa}) VALUES ({placeholders})"
    
    # Prepara i dati come una lista di tuple
    dati_tuple = [tuple(riga.values()) for riga in dati_da_inserire]
    
    try:
        # Usa executemany per inserire tutte le righe in modo efficiente
        cursor.executemany(query, dati_tuple)
        conn.commit()
        st.success(f"{cursor.rowcount} record inseriti con successo nella tabella '{nome_tabella}'.")
    except sq.Error as e:
        st.error(f"Errore durante l'inserimento dei dati: {e}")
    '''
    st.code(code_insert, language='python')

    st.write("#### 2. Esempio di utilizzo")
    code_insert_example = '''
# --- Esempio di utilizzo ---
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        # Dati per la tabella AnagraficaClienti
        nuovi_clienti = [
            {'id_utente': 1, 'nome_utente': 'Mario Rossi', 'email': 'mario.rossi@example.com'},
            {'id_utente': 2, 'nome_utente': 'Laura Bianchi', 'email': 'laura.bianchi@example.com'},
            {'id_utente': 3, 'nome_utente': 'Giuseppe Verdi', 'email': 'giuseppe.verdi@example.com'}
        ]
        
        insert_data_dinamicamente(conn, "AnagraficaClienti", nuovi_clienti)
        
        conn.close()
    '''
    st.code(code_insert_example, language='python')
#************************************************************************************************************************************************************************************

with st.expander("**:pencil2: Aggiornamento di Dati (UPDATE)**"):
    st.write(
        """
        I dati raramente sono statici. Spesso è necessario modificare record già esistenti.
        La funzione `update_records_dinamicamente` permette di aggiornare una o più righe
        che corrispondono a una condizione specifica.
        """
    )
    
    st.write("#### 1. Funzione per l'aggiornamento dinamico")

    def update_records_dinamicamente(conn, nome_tabella, dati_da_impostare, condizione):
        if not conn or not dati_da_impostare or not condizione:
            st.warning("Parametri non validi per l'aggiornamento.")
            return

        cursor = conn.cursor()
        
        # Costruisci la parte SET della query
        set_clause = ", ".join([f"{col} = ?" for col in dati_da_impostare.keys()])
        
        # Costruisci la parte WHERE della query
        where_clause = " AND ".join([f"{col} = ?" for col in condizione.keys()])
        
        query = f"UPDATE {nome_tabella} SET {set_clause} WHERE {where_clause}"
        
        # Combina i valori per SET e WHERE nell'ordine corretto
        valori = list(dati_da_impostare.values()) + list(condizione.values())
        
        try:
            cursor.execute(query, valori)
            conn.commit()
            st.success(f"{cursor.rowcount} record aggiornati con successo in '{nome_tabella}'.")
        except sq.Error as e:
            st.error(f"Errore durante l'aggiornamento dei record: {e}")

    
    code_update = '''
def update_records_dinamicamente(conn, nome_tabella, dati_da_impostare, condizione):
    """
    Aggiorna i record in una tabella in base a una condizione.

    Args:
        conn: L'oggetto di connessione al database.
        nome_tabella (str): Il nome della tabella da aggiornare.
        dati_da_impostare (dict): Dizionario con le colonne da aggiornare e i nuovi valori.
                                 Esempio: {'email': 'nuova.email@example.com'}
        condizione (dict): Dizionario che rappresenta la clausola WHERE.
                           Esempio: {'id_utente': 1}
    """
    if not conn or not dati_da_impostare or not condizione:
        st.warning("Parametri non validi per l'aggiornamento.")
        return

    cursor = conn.cursor()
    
    # Costruisci la parte SET della query
    set_clause = ", ".join([f"{col} = ?" for col in dati_da_impostare.keys()])
    
    # Costruisci la parte WHERE della query
    where_clause = " AND ".join([f"{col} = ?" for col in condizione.keys()])
    
    query = f"UPDATE {nome_tabella} SET {set_clause} WHERE {where_clause}"
    
    # Combina i valori per SET e WHERE nell'ordine corretto
    valori = list(dati_da_impostare.values()) + list(condizione.values())
    
    try:
        cursor.execute(query, valori)
        conn.commit()
        st.success(f"{cursor.rowcount} record aggiornati con successo in '{nome_tabella}'.")
    except sq.Error as e:
        st.error(f"Errore durante l'aggiornamento dei record: {e}")
    '''
    st.code(code_update, language='python')

    st.write("#### 2. Esempio di utilizzo")
    code_update_example = '''
# --- Esempio di utilizzo ---
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        # Aggiorniamo l'email del cliente con id_utente = 1
        dati_nuovi = {'email': 'm.rossi.new@example.com'}
        condizione_where = {'id_utente': 1}
        
        update_records_dinamicamente(conn, "AnagraficaClienti", dati_nuovi, condizione_where)
        
        conn.close()
    '''
    st.code(code_update_example, language='python')

#************************************************************************************************************************************************************************************
with st.expander("**:wastebasket: Eliminazione Record (DROP & DELETE)**"):
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

    #************************************************************************************************************************************************************************************
with st.expander("**:mag: Esecuzione di Query Complesse**"):
    st.write(
        """
        Oltre a caricare intere tabelle, la vera potenza di SQL risiede nell'eseguire
        query complesse per filtrare, ordinare e aggregare i dati. Pandas può
        eseguire qualsiasi query SQL e restituire il risultato direttamente in un DataFrame.
        """
    )

    def query_to_dataframe(conn, query, params=None):
        try:
            df = pd.read_sql_query(query, conn, params=params)
            return df
        except Exception as e:
            st.error(f"Errore nell'esecuzione della query: {e}")
            return pd.DataFrame() # Ritorna un df vuoto in caso di errore

    st.write("#### 1. Funzione per query personalizzate")
    code_query = '''
def query_to_dataframe(conn, query, params=None):
    """
    Esegue una query SQL personalizzata e restituisce un DataFrame.

    Args:
        conn: L'oggetto di connessione al database.
        query (str): La stringa SQL da eseguire.
        params (tuple, optional): Un tuple di parametri per la query (per sicurezza).
    
    Returns:
        pd.DataFrame: Un DataFrame con i risultati della query.
    """
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Errore nell'esecuzione della query: {e}")
        return pd.DataFrame() # Ritorna un df vuoto in caso di errore
    '''
    st.code(code_query, language='python')
    
    st.write("#### 2. Esempio di utilizzo")
    st.write("Cerchiamo tutti i clienti il cui nome contiene 'Mario' e ordiniamoli per email.")
    code_query_example = '''
# --- Esempio di utilizzo ---
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        # Query con un filtro WHERE, un operatore LIKE e un ORDER BY
        sql = "SELECT * FROM AnagraficaClienti WHERE nome_utente LIKE ? ORDER BY email DESC"
        
        # Il parametro viene passato in modo sicuro
        parametri = ('%Mario%',) 
        
        df_risultato = query_to_dataframe(conn, sql, parametri)
        
        st.write("Risultato della query complessa:")
        st.dataframe(df_risultato)
        
        conn.close()
    '''
    st.code(code_query_example, language='python')
    #************************************************************************************************************************************************************************************
with st.expander("**:link: Migliorare la Gestione della Connessione (Best Practice)**"):
    st.write(
        """
        Una best practice in Python per gestire risorse come le connessioni a un database
        è usare un "context manager" (l'istruzione `with`). Questo garantisce che la
        connessione venga chiusa correttamente anche se si verificano errori nel codice.
        """
    )
    
    st.write("#### 1. Funzione di connessione migliorata")
    st.info("Questa versione della funzione usa `yield` per trasformarsi in un 'generatore' che può essere usato in un blocco `with`.")

    from contextlib import contextmanager

    @contextmanager
    def get_db_connection_safe():
        """
        Una versione più sicura per ottenere la connessione al database
        che può essere usata con un'istruzione 'with'.
        """
        path_db = "database.db"
        conn = None
        try:
            conn = sq.connect(path_db)
            yield conn
        except sq.Error as e:
            st.error(f"Errore di connessione al database: {e}")
        finally:
            if conn:
                conn.close()

    code_conn_with = '''
from contextlib import contextmanager

@contextmanager
def get_db_connection_safe():
    """
    Una versione più sicura per ottenere la connessione al database
    che può essere usata con un'istruzione 'with'.
    """
    path_db = "percorso/al/tuo/database.db"
    conn = None
    try:
        conn = sq.connect(path_db)
        yield conn
    except sq.Error as e:
        st.error(f"Errore di connessione al database: {e}")
    finally:
        if conn:
            conn.close()
    '''
    st.code(code_conn_with, language='python')
    
    st.write("#### 2. Esempio di utilizzo")
    st.write("Nota come non sia più necessario chiamare `conn.close()` esplicitamente.")
    code_with_example = '''
# --- Esempio di utilizzo ---
if __name__ == "__main__":
    # La connessione viene aperta all'inizio del blocco 'with'
    # e chiusa automaticamente alla fine.
    with get_db_connection_safe() as conn:
        if conn:
            # Eseguiamo tutte le nostre operazioni qui dentro
            sql = "SELECT * FROM AnagraficaClienti WHERE id_utente = ?"
            df_utente = query_to_dataframe(conn, sql, params=(1,))
            st.write("Dati ottenuti con connessione sicura:")
            st.dataframe(df_utente)

    # A questo punto, la connessione è già stata chiusa.
    '''
    st.code(code_with_example, language='python')
    #************************************************************************************************************************************************************************************
with st.expander("**:point_right: Esempi Interattivi con Form (INSERT e UPDATE)**", expanded=True):
    st.write(
        """
        La teoria è utile, ma la pratica è ancora meglio! In questa sezione, puoi
        interagire direttamente con il database "AnagraficaClienti" usando dei form
        per inserire e aggiornare i dati in tempo reale.
        """
    )
    st.info("Nota: per questi esempi, assicurati di aver creato la tabella `AnagraficaClienti` come mostrato in precedenza.")

    # --- Mostra i dati attuali ---
    st.write("#### Dati Attuali nella Tabella `AnagraficaClienti`")
    
    # Usiamo la connessione sicura per visualizzare i dati
    try:
        with get_db_connection_safe() as conn:
            if conn:
                df_attuale = query_to_dataframe(conn, "SELECT * FROM AnagraficaClienti ORDER BY id_utente")
                st.dataframe(df_attuale, use_container_width=True)
    except Exception as e:
        st.error(f"Impossibile caricare i dati. Assicurati che la tabella esista. Errore: {e}")
        df_attuale = pd.DataFrame() # Definisci un dataframe vuoto per evitare errori successivi

    # --- Form per l'inserimento ---
    st.write("---")
    st.write("#### Inserisci un Nuovo Cliente")
    
    with st.form("insert_form"):
        st.write("Compila i campi per aggiungere un nuovo record.")
        
        # Usiamo il dataframe caricato per suggerire il prossimo ID disponibile
        next_id = (df_attuale['id_utente'].max() + 1) if not df_attuale.empty else 1
        
        new_id = st.number_input("ID Utente", min_value=1, value=int(next_id))
        new_name = st.text_input("Nome Utente")
        new_email = st.text_input("Email")
        
        submitted_insert = st.form_submit_button("Aggiungi Cliente")

        if submitted_insert:
            if new_name and new_email:
                nuovo_cliente = [{
                    'id_utente': new_id,
                    'nome_utente': new_name,
                    'email': new_email
                }]
                
                with get_db_connection_safe() as conn:
                    if conn:
                        insert_data_dinamicamente(conn, "AnagraficaClienti", nuovo_cliente)
                        # Rerun per aggiornare la tabella visualizzata
                        st.rerun() 
            else:
                st.warning("Per favore, compila tutti i campi.")

    # --- Form per l'aggiornamento ---
    st.write("---")
    st.write("#### Aggiorna un Cliente Esistente")
     
    with st.form("update_form"):
        st.write("Specifica l'ID del cliente da modificare e inserisci il nuovo indirizzo email.")
        
        # L'utente seleziona l'ID da una lista di ID esistenti
        if not df_attuale.empty:
            id_to_update = st.selectbox(
                "ID Utente da aggiornare", 
                options=df_attuale['id_utente'].tolist()
            )
            updated_email = st.text_input("Nuova Email")
        
        submitted_update = st.form_submit_button("Aggiorna Email")  # <--- Spostato QUI
        
        if submitted_update:
            if not df_attuale.empty:  # <--- Aggiungi una condizione per evitare l'errore se la tabella è vuota
                if updated_email:
                    dati_da_impostare = {'email': updated_email}
                    condizione = {'id_utente': id_to_update}
                    
                    with get_db_connection_safe() as conn:
                        if conn:
                            update_records_dinamicamente(conn, "AnagraficaClienti", dati_da_impostare, condizione)
                            st.rerun()
                else:
                    st.warning("Per favore, inserisci la nuova email.")
            else:
                st.warning("Non ci sono clienti da aggiornare.") # Avviso nel caso in cui non ci siano dati.
        
        if df_attuale.empty: # Condizione per mostrare un messaggio informativo
            st.info("Nessun dato presente nella tabella da aggiornare.")
