import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time
from io import BytesIO
from openpyxl import load_workbook, Workbook
import os


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

with st.expander("**:black_square_button: Import**"):
	code = '''
	from io import BytesIO
	from openpyxl import load_workbook, Workbook
	import os
	'''
	st.code(code, language="python")
#************************************************************************************************************************************************************************************
with st.expander("**:black_square_button: Leggere un file .csv e .xlsx**"):
    st.write("#### 1. Lettura file csv")
    code = '''
    file_csv = pd.read_csv(percorso_del_file_csv, sep = ';')
    dataframe = pd.DataFrame(file_csv)'''
    st.code(code, language="python")
    st.write("#### 2. Lettura file excel")
    code = '''
    file_excel = pd.read_excel(percorso_del_file_excel, sheet_name= 'FoglioXXX', usecols=['Pippo', 'Pluto', 'Team', 'Ingresso']) 
    dataframe = pd.DataFrame(file_excel)'''
    st.code(code, language="python")
    st.info("usecols è opzionale e puoi decidere quali colonne importare, se non viene inserito verrà importato tutto il file")
#************************************************************************************************************************************************************************************    
with st.expander("**:arrow_down: Esportare un DataFrame in .xlsx**"):
    st.write(
        """
        Una volta che i dati sono stati elaborati, è spesso necessario esportarli in un formato
        come Excel. Streamlit rende questo processo semplice con il `st.download_button`.
        
        Il trucco consiste nel creare il file Excel "in memoria" (usando `BytesIO`) invece che 
        su un file fisico sul disco, per poi passarlo al pulsante di download.
        """
    )

    # Usiamo il DataFrame 'clienti' e 'ordini' come esempio
    st.write("Esempio di esportazione dei DataFrame 'clienti' e 'ordini' in un unico file Excel con due fogli di lavoro.")

    code = '''
from io import BytesIO

output = BytesIO()

# Usiamo pd.ExcelWriter per scrivere più fogli nello stesso file
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    clienti.to_excel(writer, index=False, sheet_name='Clienti')
    ordini.to_excel(writer, index=False, sheet_name='Ordini')

# Recuperiamo i dati binari del file Excel creato in memoria
file_data = output.getvalue()

st.download_button(
    label="📥 Scarica File Excel",
    data=file_data,
    file_name="Export_Clienti_Ordini.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
    '''
    st.code(code, language='python')
    
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        clienti.to_excel(writer, index=False, sheet_name='Clienti')
        ordini.to_excel(writer, index=False, sheet_name='Ordini')

    file_data = output.getvalue()

    st.download_button(
        label="📥 Scarica File Excel",
        data=file_data,
        file_name="Export_Clienti_Ordini.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key='download-excel'
    )