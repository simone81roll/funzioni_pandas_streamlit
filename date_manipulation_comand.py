import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time
import sqlite3 as sq
from dateutil.easter import easter


data_clienti = {
    'ID_cliente': [1, 2, 3, 4, 5, 6, 7],
    'nome_cliente': ['Mario Rossi', 'Laura Bianchi', 'Giuseppe Verdi', 'Anna Neri', 'Paolo Forti', 'Silvia Gallo', 'Marco Bini'],
    'citta': ['Roma', 'Milano', 'Napoli', 'Torino', 'Bologna', 'Milano', 'Roma']
}
clienti = pd.DataFrame(data_clienti)

data_ordini = {
    'ID_ordine': [101, 102, 103, 104, 105, 106, 107, 108],
    'ID_cliente': [1, 3, 2, 1, 5, 6, 10, 4],
    'data_ordine': pd.to_datetime(['2024-01-15', '2024-01-17', '2024-02-01', '2024-02-05', '2024-02-10', '2024-03-01', '2024-03-05', '2024-03-10']),
    'Prodotto': ['Telecaster', 'Stratocaster', 'Les Paul', 'SG', 'Jazzmaster','Es-335','Gretsch White Falcon','Flying V'],
    'importo': [150.50, 200.00, 75.25, 300.00, 120.00, 80.00, 50.00, 250.00]
}
ordini = pd.DataFrame(data_ordini)

def week_number_in_month(date):
    first_day_of_month = date.replace(day=1)
    first_weekday = first_day_of_month.weekday()
    delta_days = (date - first_day_of_month).days
    if first_weekday == 6:
        if delta_days < 1:
            return 1
        else:
            week_number = (delta_days + first_weekday) // 7
    else:
        week_number = (delta_days + first_weekday) // 7 + 1
    return week_number


st.subheader("🗓️ Manipolazione delle date", divider='blue')

#************************************************************************************************************************************************************************************
with st.expander("**:calendar: Operazioni sulle Date e Funzioni Personalizzate**"):
    st.write(
        """
        Lavorare con le date è fondamentale. Pandas offre strumenti potentissimi per
        gestire colonne di tipo data/ora, accessibili tramite l'attributo `.dt`.
        """
    )
    
    date_df = ordini.copy()

    st.write("#### 1. Estrarre componenti da una data")
    st.write("Con `.dt` possiamo facilmente estrarre anno, mese, giorno, giorno della settimana, ecc.")
    code_dt = '''
# Assicuriamoci che la colonna sia di tipo datetime
date_df['data_ordine'] = pd.to_datetime(date_df['data_ordine'])

date_df['Anno'] = date_df['data_ordine'].dt.year
date_df['Mese'] = date_df['data_ordine'].dt.month
date_df['Giorno'] = date_df['data_ordine'].dt.day
date_df['Giorno_Settimana'] = date_df['data_ordine'].dt.day_name(locale='it_IT.utf8')

st.dataframe(date_df)
    '''
    st.code(code_dt, language='python')
    date_df['data_ordine'] = pd.to_datetime(date_df['data_ordine'])
    date_df['Anno'] = date_df['data_ordine'].dt.year
    date_df['Mese'] = date_df['data_ordine'].dt.month
    date_df['Giorno'] = date_df['data_ordine'].dt.day
    date_df['Giorno_Settimana'] = date_df['data_ordine'].dt.day_name(locale='it_IT.utf8')
    st.dataframe(date_df)


    st.write("#### 2. Applicare una funzione personalizzata con `.apply()`")
    st.write("Quando le funzioni base non bastano, possiamo scrivere la nostra logica e applicarla a ogni riga della colonna usando `.apply()`.")
    st.write("Usiamo la tua funzione `week_number_in_month` per calcolare la settimana del mese per ogni ordine.")
    
    # Prima mostriamo il codice della funzione
    st.write("Codice della funzione personalizzata:")
    code_func = '''
def week_number_in_month(date):
    first_day_of_month = date.replace(day=1)
    first_weekday = first_day_of_month.weekday()
    delta_days = (date - first_day_of_month).days
    if first_weekday == 6:
        if delta_days < 1:
            return 1
        else:
            week_number = (delta_days + first_weekday) // 7
    else:
        week_number = (delta_days + first_weekday) // 7 + 1
    return week_number
    '''
    st.code(code_func, language='python')

    # Poi mostriamo come applicarla
    st.write("Applicazione della funzione al DataFrame:")
    code_apply = '''
date_df['Settimana_nel_mese'] = date_df['data_ordine'].apply(week_number_in_month)
st.dataframe(date_df[['data_ordine', 'Settimana_nel_mese']])
    '''
    st.code(code_apply, language='python')
    
    date_df['Settimana_nel_mese'] = date_df['data_ordine'].apply(week_number_in_month)
    st.dataframe(date_df[['data_ordine', 'Settimana_nel_mese']])

# --- SEZIONE 1: CONFIGURAZIONE E FUNZIONI DI BASE ---

with st.expander("**:gear: Configurazione e Import Librerie**"):
    st.write(
        """
        Per questo modulo, abbiamo bisogno di diverse librerie:
        - **Streamlit**: per creare l'interfaccia web.
        - **Pandas**: per gestire i dati in formato tabellare.
        - **sqlite3**: per interagire con il database SQLite.
        - **datetime** e **dateutil**: per calcolare le date delle festività (in particolare la Pasqua).
        """
    )
    code_imports = '''
import pandas as pd
import streamlit as st
from datetime import date, timedelta, datetime
import sqlite3 as sq
from dateutil.easter import easter
    '''
    st.code(code_imports, language='python')
    
    st.write("#### Impostazione del Percorso del Database")
    st.write("Questa funzione definisce il percorso del file del database. È importante per rendere lo script portabile.")
    code_path = '''
# In un progetto reale, il percorso del database andrebbe qui.
# Per questa guida, creiamo il database nella stessa cartella.
path_calendar = "calendar.db"

def get_db_connection():
    """Crea e restituisce una connessione al database SQLite."""
    conn = sq.connect(path_calendar)
    return conn
    '''
    st.code(code_path, language='python')
    
    # Definiamo le funzioni qui in modo che siano disponibili per l'app
    path_calendar = "calendar.db"
    def get_db_connection():
        conn = sq.connect(path_calendar)
        return conn

with st.expander("**:floppy_disk: Funzioni di Interazione con il Database**"):
    st.write(
        """
        Queste sono le funzioni "CRUD" (Create, Read, Update, Delete) che ci permettono
        di comunicare con il nostro database `calendar.db`.
        """
    )

    st.write("#### 1. Creare la Tabella (`create_db`)")
    st.write("Questa funzione crea la tabella delle chiusure per un anno specifico, se non esiste già. Il nome della tabella è dinamico (es. `calendar_chiusure_2024`).")
    code_create = f'''

anno_selezionato = st.number_input("Seleziona l'anno per le operazioni:", value=datetime.now().year, key="anno_globale")

def create_db(anno):
    """Crea la tabella per l'anno specificato se non esiste."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS calendar_chiusure_{{anno_selezionato}} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_chiusura TEXT NOT NULL,
        nota_chiusura TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    '''
    st.code(code_create, language='python')

    st.write("#### 2. Aggiungere un Record (`agg_bd_calendar`)")
    st.write("Inserisce una nuova data di chiusura e una nota nella tabella dell'anno corrispondente.")
    code_add = f'''
def agg_bd_calendar(anno, data_chiusura, nota_chiusura):
    """Aggiunge un record alla tabella dell'anno specificato."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO calendar_chiusure_{{anno}} (data_chiusura, nota_chiusura)
    VALUES (?, ?)
    """, (data_chiusura, nota_chiusura))
    conn.commit()
    conn.close()
    '''
    st.code(code_add, language='python')

    st.write("#### 3. Leggere i Dati (`load_data`)")
    st.write("Recupera tutti i record dalla tabella di un anno e li restituisce come DataFrame Pandas.")
    code_load = f'''
def load_data(anno):
    """Carica tutti i dati dall'anno specificato in un DataFrame."""
    conn = get_db_connection()
    query = f"SELECT * FROM calendar_chiusure_{{anno}}"
    df_database = pd.read_sql(query, conn)
    conn.close()
    return df_database
    '''
    st.code(code_load, language='python')

    st.write("#### 4. Eliminare Record (`delete_records`)")
    st.write("Elimina una o più righe dalla tabella in base a una lista di ID. Usa i placeholder `?` per un'operazione sicura.")
    code_delete = f'''
def delete_records(anno, record_ids):
    """Elimina i record corrispondenti a una lista di ID."""
    if not record_ids: return 0
    conn = get_db_connection()
    cursor = conn.cursor()
    placeholders = ','.join(['?'] * len(record_ids))
    query = f"DELETE FROM calendar_chiusure_{{anno}} WHERE id IN ({{placeholders}})"
    
    cursor.execute(query, tuple(record_ids))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected
    '''
    st.code(code_delete, language='python')
    
    # Rendiamo le funzioni disponibili nello script
    def create_db(anno):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS calendar_chiusure_{anno} (id INTEGER PRIMARY KEY AUTOINCREMENT, data_chiusura TEXT NOT NULL, nota_chiusura TEXT NOT NULL)")
        conn.commit()
        conn.close()

    def agg_bd_calendar(anno, data_chiusura, nota_chiusura):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO calendar_chiusure_{anno} (data_chiusura, nota_chiusura) VALUES (?, ?)", (data_chiusura, nota_chiusura))
        conn.commit()
        conn.close()

    def load_data(anno):
        try:
            conn = get_db_connection()
            query = f"SELECT * FROM calendar_chiusure_{anno}"
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except pd.io.sql.DatabaseError: # Errore se la tabella non esiste
            return pd.DataFrame() # Ritorna un df vuoto

    def delete_records(anno, record_ids):
        if not record_ids: return 0
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['?'] * len(record_ids))
        query = f"DELETE FROM calendar_chiusure_{anno} WHERE id IN ({placeholders})"
        cursor.execute(query, tuple(int(id_val) for id_val in record_ids))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected

# --- SEZIONE 2: APPLICAZIONE INTERATTIVA ---

with st.expander(f"**🚀 Applicazione Interattiva**", expanded=True):
    
    anno_selezionato = st.number_input("Seleziona l'anno per le operazioni:", value=datetime.now().year, key="anno_globale")

    st.write(fr"### 1. Calcolo Automatico Festività Italiane per l'Anno {anno_selezionato}")
    st.write("Questa sezione calcola le festività nazionali per l'anno selezionato e offre un pulsante per salvarle nel database.")

    # Calcolo festività
    pasqua = pd.to_datetime(easter(anno_selezionato))
    df_chiusure_sede = pd.DataFrame({
        'Data': [pd.to_datetime(date(anno_selezionato, 1, 1)), pd.to_datetime(date(anno_selezionato, 1, 6)), pasqua, pasqua + timedelta(days=1),
                 pd.to_datetime(date(anno_selezionato, 4, 25)), pd.to_datetime(date(anno_selezionato, 5, 1)), pd.to_datetime(date(anno_selezionato, 6, 2)),
                 pd.to_datetime(date(anno_selezionato, 8, 15)), pd.to_datetime(date(anno_selezionato, 11, 1)), pd.to_datetime(date(anno_selezionato, 12, 8)),
                 pd.to_datetime(date(anno_selezionato, 12, 25)), pd.to_datetime(date(anno_selezionato, 12, 26))],
        'Nota': ['Chiusura (Festività)'] * 12
    })
    df_chiusure_sede['Data'] = df_chiusure_sede['Data'].dt.strftime("%d/%m/%Y")
    st.dataframe(df_chiusure_sede, use_container_width=True, hide_index=True)

    if st.button('Salva Festività nel DB'):
        create_db(anno_selezionato)
        for _, row in df_chiusure_sede.iterrows():
            agg_bd_calendar(anno_selezionato, row['Data'], row['Nota'])
        st.success('Festività salvate con successo nel database!')
        st.rerun()

    st.write("---")
    st.write("### 2. Aggiunta Manuale di Chiusure")
    st.write("Usa questo form per aggiungere chiusure specifiche (es. ponti, ferie aziendali) al database.")
    
    with st.form(key='date_chiusure'):
        col1, col2 = st.columns(2)
        data_chiusura = col1.date_input('Data:', value=None, format="DD/MM/YYYY")
        nota_chiusura = col2.selectbox('Seleziona una opzione:', ('Chiusura', 'Parziale', 'Ponte'))
        
        if st.form_submit_button(label='Aggiungi Chiusura'):
            if data_chiusura:
                create_db(anno_selezionato)
                agg_bd_calendar(anno_selezionato, data_chiusura.strftime("%d/%m/%Y"), nota_chiusura)
                st.success('Chiusura aggiunta con successo!')
                st.rerun()
            else:
                st.warning("Per favore, seleziona una data.")

    st.write("---")
    st.write("### 3. Visualizzazione e Gestione Chiusure Salvare")
    st.write("Qui puoi vedere tutte le chiusure salvate nel database per l'anno selezionato. Seleziona una o più righe e clicca 'Elimina' per rimuoverle.")
    
    db_chiusura_sede = load_data(anno_selezionato)
    if not db_chiusura_sede.empty:
        record_selected = st.dataframe(
            db_chiusura_sede,
            on_select="rerun",
            selection_mode=["multi-row"],
            hide_index=True
        )
        
        selected_ids = [db_chiusura_sede.iloc[i]['id'] for i in record_selected.selection.rows]
        
        if selected_ids:
            st.write(f"**ID selezionati per l'eliminazione:** {', '.join(map(str, selected_ids))}")
            if st.button("Elimina Record Selezionati", type="primary"):
                rows_deleted = delete_records(anno_selezionato, selected_ids)
                if rows_deleted > 0:
                    st.success(f"{rows_deleted} record eliminati con successo.")
                    st.rerun()
                else:
                    st.warning("Nessun record è stato eliminato.")
    else:
        st.info(f"Nessuna chiusura salvata nel database per l'anno {anno_selezionato}.")
        # Bottone per creare la tabella se non esiste
        if st.button(f"Crea Tabella per l'anno {anno_selezionato}"):
            create_db(anno_selezionato)
            st.rerun()
