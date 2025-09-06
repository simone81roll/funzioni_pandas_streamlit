import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time


today = date.today()
month_today = today.month
anno_corrente = datetime.now().year

with st.expander("**:black_square_button: Importazione librerie**"):
    code = ''' import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time
    '''
    st.code(code, language="python")

#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Creazione e visualizzazione di un dataframe**"):
    st.write('DataFrame Clienti')
    code = '''    data_clienti = {
        'ID_cliente': [1, 2, 3, 4, 5, 6, 7],
        'nome_cliente': ['Mario Rossi', 'Laura Bianchi', 'Giuseppe Verdi', 'Anna Neri', 'Paolo Forti', 'Silvia Gallo', 'Marco Bini'],
        'citta': ['Roma', 'Milano', 'Napoli', 'Torino', 'Bologna', 'Milano', 'Roma']
    }
    clienti = pd.DataFrame(data_clienti)
    st.dataframe(clienti, use_container_width=True, hide_index = True)'''
    st.code(code, language="python")    
    
    data_clienti = {
        'ID_cliente': [1, 2, 3, 4, 5, 6, 7],
        'nome_cliente': ['Mario Rossi', 'Laura Bianchi', 'Giuseppe Verdi', 'Anna Neri', 'Paolo Forti', 'Silvia Gallo', 'Marco Bini'],
        'citta': ['Roma', 'Milano', 'Napoli', 'Torino', 'Bologna', 'Milano', 'Roma']
    }
    clienti = pd.DataFrame(data_clienti)
    st.dataframe(clienti, use_container_width=True, hide_index = True)

    st.write('DataFrame Ordini')
    code = '''    data_ordini = {
        'ID_ordine': [101, 102, 103, 104, 105, 106, 107, 108],
        'ID_cliente': [1, 3, 2, 1, 5, 6, 10, 4],
        'data_ordine': pd.to_datetime(['2024-01-15', '2024-01-17', '2024-02-01', '2024-02-05', '2024-02-10', '2024-03-01', '2024-03-05', '2024-03-10']),
        'importo': [150.50, 200.00, 75.25, 300.00, 120.00, 80.00, 50.00, 250.00]
    }
    ordini = pd.DataFrame(data_ordini)
    st.dataframe(ordini, use_container_width=True, hide_index = True)
    ''' 
    st.code(code, language="python")     
    
    data_ordini = {
        'ID_ordine': [101, 102, 103, 104, 105, 106, 107, 108],
        'ID_cliente': [1, 3, 2, 1, 5, 6, 10, 4],
        'data_ordine': pd.to_datetime(['2024-01-15', '2024-01-17', '2024-02-01', '2024-02-05', '2024-02-10', '2024-03-01', '2024-03-05', '2024-03-10']),
        'importo': [150.50, 200.00, 75.25, 300.00, 120.00, 80.00, 50.00, 250.00]
    }
    ordini = pd.DataFrame(data_ordini)
    st.dataframe(ordini, use_container_width=True, hide_index = True)
    
    st.write('DataFrame editabile (con streamlit)')
    code = ''' edited_ordini = st.data_editor(ordini, num_rows="dynamic")
    '''
    st.code(code, language="python") 
    edited_ordini = st.data_editor(ordini, num_rows="dynamic")

#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Aggiungere/Rinominare/Ordinare & Rimuovere colonne del dataframe**"):
    code = '''    
    #Creazione di variabili con le date
    today = date.today()
    month_today = today.month
    anno_corrente = datetime.now().year
    '''
    st.code(code, language="python")

    df_filtrato = ordini.copy()

    st.write('Aggiungi colonna')
    code = '''
    ordini['Nuova Colonna'] = anno_corrente
    st.dataframe(ordini, use_container_width=True, hide_index = True)
    '''
    st.code(code, language="python")
    df_filtrato['Nuova Colonna'] = anno_corrente
    st.dataframe(df_filtrato, use_container_width=True, hide_index = True)

    st.write('Rinomina colonna')
    code = '''
    ordini = ordini.rename(columns = {'Nuova Colonna': 'Anno Corrente'})
    '''
    st.code(code, language="python")
    df_filtrato = df_filtrato.rename(columns = {'Nuova Colonna': 'Anno Corrente'})
    st.dataframe(df_filtrato, use_container_width=True, hide_index = True)


    st.write('Ordina & Rimuovi colonna')
    code = '''
    ordini = ordini[['ID_ordine', 'data_ordine', 'ID_cliente']]
    #omettendo una colonna dalla lista non verrà visualizzata
    '''
    st.code(code, language="python")
    df_filtrato = df_filtrato[['ID_ordine', 'data_ordine', 'ID_cliente']]
    df_filtrato


#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Funzione merge**"):
    st.write('Merge inner')
    code= ''' 
    df_merge = pd.merge(
        clienti, 
        ordini, 
        left_on='ID_cliente', 
        right_on='ID_cliente', 
        how='inner'
    )
    '''
    st.code(code, language="python")
    df_merge = pd.merge(clienti, ordini, left_on='ID_cliente', right_on='ID_cliente', how='inner')
    df_merge

    st.write('Merge left')
    code= ''' 
    df_merge = pd.merge(
        clienti, 
        ordini, 
        left_on='ID_cliente', 
        right_on='ID_cliente', 
        how='left'
    )
    '''
    st.code(code, language="python")
    df_merge = pd.merge(clienti, ordini, left_on='ID_cliente', right_on='ID_cliente', how='left')
    df_merge 

    st.write('Merge right')
    code= ''' 
    df_merge = pd.merge(
        clienti, 
        ordini, 
        left_on='ID_cliente', 
        right_on='ID_cliente', 
        how='right'
    )
    '''
    st.code(code, language="python")
    df_merge = pd.merge(clienti, ordini, left_on='ID_cliente', right_on='ID_cliente', how='right')
    df_merge

    code= ''' 
        #Se (come negli esempi sopra) le due colonne con le quali andrà fatto 
    #il merge hanno lo stesso nome non è necessario inserire:
    left_on='ID_cliente', 
    right_on='ID_cliente', 

    #Possiamo semplificarla in questo modo:
    df_merge = pd.merge(
        clienti, 
        ordini, 
        on='ID_cliente', 
        how='right'
    )   
    '''
    st.code(code, language="python")

#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Funzione groupby**"):
    st.write('Funzione groupby')
    #df_pezzi_netti = df_utops_cross_lordo.groupby(['Consulente','Team Consulente']).agg(PezziNetti = ('ID', 'size')).reset_index()
#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Gestione filtri**"):

    code= ''' 
    col1, col2 = st.columns(2)
    filtro_cliente = col1.text_input('Filtra per Cliente')
    filtro_citta = col2.text_input('Filtra per Città')
    
    if filtro_cliente:
        clienti = clienti[clienti['nome_cliente'].astype(str).str.contains(filtro_cliente, case=False, na=False)]
    
    if filtro_citta:
        clienti = clienti[clienti['citta'].astype(str).str.contains(filtro_citta, case=False, na=False)]

    # Visualizzazione e selezione del DataFrame
    event = st.dataframe(
        clienti,
        selection_mode="single-row",
        on_select="rerun"
    )
    selected_rows = event.selection.rows 
    '''
    st.code(code, language="python")
    
    col1, col2 = st.columns(2)
    filtro_cliente = col1.text_input('Filtra per Cliente')
    filtro_citta = col2.text_input('Filtra per Città')
    
    if filtro_cliente:
        clienti = clienti[clienti['nome_cliente'].astype(str).str.contains(filtro_cliente, case=False, na=False)]
    
    if filtro_citta:
        clienti = clienti[clienti['citta'].astype(str).str.contains(filtro_citta, case=False, na=False)]

    # Visualizzazione e selezione del DataFrame
    event = st.dataframe(
        clienti,
        selection_mode="single-row",
        on_select="rerun"
    )
    selected_rows = event.selection.rows
#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Funzione isin**"):
    #st.header('Funzione isin')
    st.info("L'istruzione seleziona solo le righe del dataframe 'clienti' in cui il valore della colonna 'ID_cliente' è presente anche nella colonna 'ID_cliente' del dataframe ordini e viceversa.  \n"
    "In pratica, sta effettuando un'operazione di filtraggio basato su un insieme di valori, che è un modo molto efficiente per eseguire un'operazione simile a un inner join in SQL, \n"
    "ma che restituisce solo le righe del DataFrame originale.")

    df_clienti = clienti[clienti['ID_cliente'].isin(ordini['ID_cliente'])]
    df_ordini = ordini[ordini['ID_cliente'].isin(clienti['ID_cliente'])]
    st.write('Filtro sul dataframe Clienti')
    code = '''df_clienti = clienti[clienti['ID_cliente'].isin(ordini['ID_cliente'])]'''
    st.code(code, language="python")
    df_clienti
    st.write('Filtro sul dataframe Ordini')
    code = '''df_ordini = ordini[ordini['ID_cliente'].isin(clienti['ID_cliente'])]'''
    st.code(code, language="python")
    df_ordini
#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Leggere un file .csv e .xlsx**"):
    st.write("Lettura file csv")
    code = '''
    file_csv = pd.read_csv(percorso_del_file_csv, sep = ';')
    dataframe = pd.DataFrame(file_csv)'''
    st.code(code, language="python")
    st.write("Lettura file excel")
    code = '''
    file_excel = pd.read_excel(percorso_del_file_excel, sheet_name= 'FoglioXXX', usecols=['Pippo', 'Pluto', 'Team', 'Ingresso']) 
    dataframe = pd.DataFrame(file_excel)'''
    st.code(code, language="python")
    st.info("usecols è opzionale e puoi decidere quali colonne importare, se non viene inserito verrà importato tutto il file")



#**********funzioni per un database SQLite3****************
def get_db_connection(): #connsessione al database
    path_db = fr"percorso/xxxxxx.db"
    conn = sq.connect(path_db)
    return conn

def load_data(): #lettura del database
    conn = get_db_connection()
    query = f"SELECT * FROM {tab_name}"
    df_database = pd.read_sql(query, conn)
    conn.close()
    return df_database


#*************funzioni varie******************
def week_number_in_month(date):
    first_day_of_month = date.replace(day=1) #crea un nuovo oggetto date che rappresenta il primo giorno del mese della data fornita
    first_weekday = first_day_of_month.weekday() #si ottiene il giorno della settimana del primo giorno del mese. Il metodo weekday() restituisce un numero intero da 0 (lunedì) a 6 (domenica).
    delta_days = (date - first_day_of_month).days
    if first_weekday == 6:
        if delta_days < 1:
            return 1
        else:
            week_number = (delta_days + first_weekday) // 7
    # Calcola il numero della settimana relativa al mese
    else:
        week_number = (delta_days + first_weekday) // 7 + 1
    return week_number