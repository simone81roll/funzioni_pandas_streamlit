import streamlit as st
import os
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import pandas as pd

import io
from io import BytesIO
import numpy as np


import datetime
from datetime import date, timedelta, datetime

st.subheader("📋 Elaborare file di testo", divider='blue')

with st.expander("**:inbox_tray: Import**"):
    st.write('''
#### 1. Importazioni Iniziali
- **`streamlit (st)`:** Per creare l'interfaccia utente web interattiva.
- **`os`:** Per interagire con il sistema operativo, come controllare l'esistenza dei file.
- **`imaplib, email, email.header, email.message, bs4 (BeautifulSoup)`:** Per la connessione al server IMAP di Gmail, l'analisi delle email e l'estrazione di contenuto HTML (tabelle).
- **`pandas (pd), io, numpy (np)`:** Per la manipolazione dei dati, in particolare per la creazione e la gestione dei DataFrame e l'output in CSV.
- **`datetime, date, timedelta`:** Per la gestione e la manipolazione di date e orari.
    ''')
    code = '''
import streamlit as st
import os
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import pandas as pd

import io
from io import BytesIO
import numpy as np


import datetime
from datetime import date, timedelta, datetime
    '''
    st.code(code, language="python")
#************************************************************************************************************************************************************************************

with st.expander("**:email: Importazione ed elaborazione da casella e-mail**"):
    
    # Crea le schede
    tab1, tab2, tab3 = st.tabs(["1. Estrazione Email", "2. Elaborazione Dati", "3. Output Finale"])

    # -------------------------------------------------------------------------------------------
    # TAB 1: Configurazione & Estrazione Email
    with tab1:
        st.subheader("Configurazione e Download")

    code = '''  
# Input per il nome della cartella
col1, col2, col3 = st.columns([2, 2, 1], vertical_alignment="bottom")
label_name = col1.text_input('**Inserisci il nome della cartella**')

# Filtro per l'oggetto
filtro_oggetto = col2.selectbox("**Seleziona il filtro per l'oggetto della mail**",["Clienti", "Ordini"], index =0)
#filtro_oggetto = st.text_input("Inserisci il filtro per l'oggetto")
file_name = filtro_oggetto.replace('/', '_') 


# Pulsante per eseguire l'operazione
if col3.button('Estrai'):
    username = 'example@facile.it'
    password = "*****************"

    # Crea una connessione al server di Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    # Effettua il login
    mail.login(username, password)

    # Seleziona la cartella
    mail.select(f'"{label_name}"')

    if filtro_oggetto:
        result, data = mail.search(None, f'(SUBJECT "{filtro_oggetto}")')
    else:
        result, data = mail.search(None, 'ALL')

    # Estrai gli ID delle email trovate
    email_ids = data[0].split()
    # Conta il numero di email trovate
    num_emails = len(email_ids)

    # Apri un file per scrivere le email trovate
    with open(f'{file_name}.txt', 'w', encoding='utf-8') as f:
        for email_id in email_ids:
            # Recupera il messaggio
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Decodifica l'oggetto dell'email
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            # Recupera altre informazioni utili
            from_ = msg.get('From')
            date_ = msg.get('Date')

            # Estrai il corpo del messaggio
            body = ""
            table = None  # Inizializza table come None
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/html':
                        html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        soup = BeautifulSoup(html_body, 'html.parser')
                        table = soup.find('table')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                if msg.get_content_type() == 'text/html':
                    soup = BeautifulSoup(body, 'html.parser')
                    table = soup.find('table')

            # Scrivi le informazioni nel file, inclusa la tabella
            f.write(f'Da: {from_} Oggetto: {subject} {date_}')
            if table:
                for row in table.find_all('tr'):
                    columns = row.find_all(['td', 'th'])
                    values = [col.get_text(strip=True) for col in columns]
                    line = '\\t'.join(values)
                    f.write(line + '\\n')
                f.write("\\n")  # Aggiungi una linea vuota dopo ogni email
            else:
                f.write("Tabella non trovata in questa email.\\n")

    # Chiudi la connessione
    mail.logout()

    with open(f'{file_name}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    '''
    tab1.code(code, language="python")


    # -------------------------------------------------------------------------------------------
    # TAB 2: Pulizia Dati
    with tab2:
        st.subheader("Filtri e Pulizia")
        code_2 = '''
# Variabili per salvare la data e i dati da modificare
data_line = ''
if file_name == 'chiamate':
    exclude_keywords = ['Da:', 'Oggetto:' ,'Outbound ', 'Consulente', 'Totale']
    column_names = ['Consulente',   'Totale',   'Utile OK', 'Utile KO', 'NT',   'Appuntamento', '% NT', '% Eff.', 'Totale_1', 'Utile OK_1', 'Utile KO_1', 'NT_1', 'Appuntamento_1','% NT_1','% Eff._1']
elif file_name == 'emissioni':
    exclude_keywords = ['Da:', 'Oggetto:' ,'Polizze Vendute', 'Consulente', 'Totale', 'Altro']
    column_names = ['Consulente', 'Rinnovi',   'NB',   'Tot. Emissioni', 'Rinnovi_1',   'NB_1',   'Tot. Emissioni_1']
output_lines = []
previous_line = None

for line in lines:
    # Controlla se la riga corrente è vuota o inizia con una delle parole chiave da escludere
    if line.strip() and not any(line.startswith(keyword) for keyword in exclude_keywords):
        output_lines.append(line.strip())
    previous_line = line.strip()  # Aggiorna la linea precedente
if output_lines:  # Controlla che output_lines non sia vuoto
    data = output_lines[0]

exclude_keywords_output = ['+0000','Totale', 'Rinnovi']

filtered_output_lines = [line for line in output_lines if not any(keyword in line for keyword in exclude_keywords_output)]

with open(f'{file_name}.txt', 'w', encoding='utf-8') as file:
    file.write('\\n'.join(filtered_output_lines))

if os.path.exists(f'{file_name}.txt') and os.path.getsize(f'{file_name}.txt') > 0:
    date_object = datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %z')
    # Format the date as GG/MM/AA
    formatted_date = date_object.strftime('%d/%m/%y')

    #formatted_date = "03/03/24"  # Formato gg/mm/aa
    date_object = datetime.strptime(formatted_date, '%d/%m/%y')
    week_num = week_number_in_month(date_object)

    #col1, col2, col3 = st.columns(3)
    col3.write(f"\\nMail scaricate: \\n{num_emails}")
    col2.write(f"Numero Week: {week_num}")
    col1.write(f"Data e-mail: {formatted_date}")


    df = pd.DataFrame([x.split('\\t') for x in filtered_output_lines[0:]])
    df = df.sort_index()  # Ordiniamo nuovamente il DataFrame
    df['Data'] = formatted_date
    df['Mese'] = date_object.month
    df['Week'] = week_num

    df.columns = column_names + ['Data'] + ['Mese'] + ['Week']

    column_order = ['Data', 'Mese', 'Week'] + column_names

    df = df[column_order]
    
    nome_file = f'{file_name}_output.csv'
    # Salva il DataFrame come file CSV
    df.to_csv(nome_file, index=False)
else:
    st.warning(f'Nessuna mail presente in cartella')
    '''
    tab2.code(code_2, language="python")    

    # -------------------------------------------------------------------------------------------
    # TAB 3: Output Finale
    with tab3:
        st.subheader("Risultato e Download CSV")
        code_3 = '''
csv_file_path = f'{file_name}_output.csv'

if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
    df = pd.read_csv(csv_file_path)
    st.dataframe(df, use_container_width=True, hide_index=True)
    # Aggiungi un pulsante di download del file CSV
    st.download_button(
        label="Scarica CSV",
        data=open(csv_file_path, 'rb').read(),
        file_name=csv_file_path,
        mime='text/csv'
else:
    st.warning("Esegui prima l'estrazione e l'elaborazione.")    
    )    
    '''
    tab3.code(code_3, language="python")          



with st.expander("**:page_with_curl: Lettura di un file**"):
    st.write('Esempio di codice utilizzato in un altro report per la lettura e la manipolazione di un file **.txt**')
    code = '''
uploaded_txt_pg = st.file_uploader("Carica il file **Presenze Giornaliere**", type=["txt"])        
    
if uploaded_txt_pg is not None:
    # Leggi il contenuto del file
    stringio = io.StringIO(uploaded_txt_pg.getvalue().decode("utf-8"))
    string_data = stringio.read()
    
    # Dividi il contenuto in righe
    lines = string_data.split('\n')
    filtered_content = '\n'.join(lines)

    df_pg = pd.read_csv(io.StringIO(filtered_content), sep='\t')
    df_pg = df_pg[['Utente', 'Primo login', 'Working time' ]]
    
    df_pg['Primo login'] = pd.to_datetime(df_pg['Primo login'], format='%Y-%m-%d %H:%M:%S')
    df_pg['Primo login'] = df_pg['Primo login'].dt.strftime('%d/%m/%y')
    df_pg['Working time'] = pd.to_datetime(df_pg['Working time'], format='%H:%M:%S')
    df_pg["Working time"] = (df_pg['Working time'].dt.hour * 60 + df_pg['Working time'].dt.minute)/60

    df_pg["Working time"] = np.where((df_pg["Working time"] > 7.5) & (df_pg["Working time"] <= 8), df_pg["Working time"] - 0.5, df_pg["Working time"])
    df_pg["Working time"] = np.where(df_pg["Working time"] > 8, df_pg["Working time"] - 1, df_pg["Working time"])

    df_pg.rename(columns = {"Primo login": 'Data'}, inplace = True)
    df_pg['Mese'] = pd.to_datetime(df_pg['Data'], format='%d/%m/%y').dt.month
    df_pg = df_pg[['Mese','Data','Utente', 'Working time' ]]
    st.dataframe(df_pg, use_container_width=True, hide_index = True)            

    '''
    st.code(code, language="python")