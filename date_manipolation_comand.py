import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time

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