import pandas as pd
import streamlit as st
from datetime import datetime

st.subheader("📊📋 Creazione dei TASK aggiornabili", divider ='blue')

with st.expander("**:package: Importazione librerie**"):
    st.write('#### Librerie necessarie per la produzione dello script')
    code = ''' import pandas as pd
import streamlit as st
from datetime import datetime
    '''
    st.code(code, language="python")

with st.expander("**:arrow_forward: Funzioni preliminari**"):

    code = ''' # --- Percorso del file Excel ---
path_task = fr"Task_report.xlsx"

# --- Funzione per salvare tutte le modifiche su Excel ---
def save_all_sheets(writer, all_sheets_data):
    """Salva tutti i fogli di lavoro nel file Excel."""
    for sheet_name, df in all_sheets_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# --- Caricamento dei dati ---
try:
    all_sheets = pd.read_excel(path_task, sheet_name=None)
except FileNotFoundError:
    st.error("File non trovato. Verifica il percorso del file.")
    st.stop() # Interrompe l'esecuzione se il file non esiste

# --- Gestione del foglio di metadati per il reset automatico ---
metadata_sheet = '_metadata'
if metadata_sheet in all_sheets:
    df_metadata = all_sheets[metadata_sheet]
    # Assicura che la colonna sia di tipo datetime
    df_metadata['last_reset'] = pd.to_datetime(df_metadata['last_reset'])
else:
    # Se il foglio non esiste, lo crea
    df_metadata = pd.DataFrame(columns=['sheet_name', 'last_reset'])

    '''
    st.code(code, language="python")

with st.expander("**:package: Task automatico**"):
    col1, col2 = st.columns([0.4, 0.6],vertical_alignment="center")
    col1.write("Aggiornamento di un task in modo automatico a seguito dell'invio di una e-mail")
    code_0 = col2.checkbox("Visualizza Codice", key='code_0')
    
    if code_0:
        code = '''def get_task_text(sede, ricerca, sheet):    
df_task = pd.read_excel(path_task, sheet_name=sheet)

# Costruisci la stringa di ricerca
if sede:
    typologia_search = f"{ricerca} {sede}"
else:
    typologia_search = f"{ricerca}"
#st.write(typologia_search)

# Trova la riga corrispondente
match_row = df_task[df_task['TIPOLOGIA'].str.contains(typologia_search, case=False, na=False)]
if not match_row.empty:
    # Prendi il primo match
    task_value = match_row.iloc[0]['TASK']
    return task_value
else:
    return None


def aggiorna_task_status(path, sheet_name, task_text):
    """
    Apre il file Excel, modifica lo stato di una task specifico e salva il file.

    Parameters:
        path (str): Percorso del file Excel.
        sheet_name (str): Nome del foglio su cui operare.
        task_text (str): Testo della task da aggiornare.
    """
    # Legge tutte le schede del file Excel
    all_sheets = pd.read_excel(path, sheet_name=None)
    
    # Ottieni il DataFrame della scheda specificata
    df = all_sheets.get(sheet_name)
    if df is None:
        raise ValueError(f"La scheda '{sheet_name}' non esiste nel file '{path}'.")

    # Assicura che la colonna 'STATUS' sia di tipo booleano
    df['STATUS'] = df['STATUS'].astype(bool)

    # Crea una maschera per la task specifica
    mask = df['TASK'] == task_text

    # Aggiorna lo stato della task
    df.loc[mask, 'STATUS'] = True

    # Aggiorna il dizionario delle schede
    all_sheets[sheet_name] = df

    # Riscrive il file Excel con le modifiche
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for s_name, df_sheet in all_sheets.items():
            df_sheet.to_excel(writer, sheet_name=s_name, index=False)

#--------------------------------------------------------------------------------------------------------------------------


#Prima parte dedicata alla tipologia di mail da inviare
send_option = st.radio("Seleziona la tipologia di invio della mail 👇",["Giornaliero", "Settimanale", "Mensile"], horizontal = True, index=0)
ricerca = 'Data Analysis & Reporting' #si riferisce alla colonna `Tipologia` del file excel
if send_option == "Giornaliero":
    sheet = 'Task_giornaliero'
    task_text = get_task_text(sede, ricerca, sheet)
    if task_text:
        subject = st.text_input("Oggetto mail", f"{task_text}")
elif send_option == "Settimanele":                    
    sheet = 'Task_settimanale'
    task_text = get_task_text(sede, ricerca, sheet)
    if task_text:
        subject = st.text_input("Oggetto mail", f"{task_text}")                  
elif send_option == "Mensile":                    
    sheet = 'Task_mese'
    task_text = get_task_text(sede, ricerca, sheet)
    if task_text:
        subject = st.text_input("Oggetto mail", f"{task_text}")

#--------------------------------------------------------------------------------------------------------------------------

#Seconda parte dedicata all'invio'
success = False
html_output_saved = False
with col1:
    email_data = get_email_addresses()
    tipi_email = list(set([data['tipo'] for data in email_data]))
    tipo_selezionato = "TEST" #fa riferimento alla tabella presente nel database SQLite3 creato per le DL
    email_details = [data for data in email_data if data['tipo'] == tipo_selezionato][0]


    if st.button('Invia',key = 'and', icon=":material/alternate_email:", use_container_width=True):
        user_login, user_password = get_login_credentials()
        if user_login == []:
            st.error('Attenzione login non effettuato', icon="🚨")
        else:
            from_email = email_details['mittente']
            to_email = email_details['destinatari']
            cc = email_details['cc'] if email_details['cc'] else ""
            subject = subject
            success = send_email (html_output, to_email, subject, from_email, user_login, user_password, cc) 
    
html_output = create_html_df(
    df=ordini, #il dataframe che vogliamo inserire nel testo della mail 
    firma=firma_utente, 
    template_name='template.html'
        )

    '''
        st.code(code, language="python")
    st.divider()


    st.write("Simulazione invio mail")
    
    def get_task_text(ricerca, sheet):    
        df_task = pd.read_excel(path_task, sheet_name=sheet)
        
        typologia_search = f"{ricerca}"
        #st.write(typologia_search)
        
        # Trova la riga corrispondente
        match_row = df_task[df_task['TIPOLOGIA'].str.contains(typologia_search, case=False, na=False)]
        if not match_row.empty:
            # Prendi il primo match
            task_value = match_row.iloc[0]['TASK']
            return task_value
        else:
            return None

    def aggiorna_task_status(path, sheet_name, task_text):
        """
        Apre il file Excel, modifica lo stato di una task specifico e salva il file.

        Parameters:
            path (str): Percorso del file Excel.
            sheet_name (str): Nome del foglio su cui operare.
            task_text (str): Testo della task da aggiornare.
        """
        # Legge tutte le schede del file Excel
        all_sheets = pd.read_excel(path, sheet_name=None)
        
        # Ottieni il DataFrame della scheda specificata
        df = all_sheets.get(sheet_name)
        if df is None:
            raise ValueError(f"La scheda '{sheet_name}' non esiste nel file '{path}'.")

        # Assicura che la colonna 'STATUS' sia di tipo booleano
        df['STATUS'] = df['STATUS'].astype(bool)

        # Crea una maschera per la task specifica
        mask = df['TASK'] == task_text

        # Aggiorna lo stato della task
        df.loc[mask, 'STATUS'] = True

        # Aggiorna il dizionario delle schede
        all_sheets[sheet_name] = df

        # Riscrive il file Excel con le modifiche
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            for s_name, df_sheet in all_sheets.items():
                df_sheet.to_excel(writer, sheet_name=s_name, index=False)



    path_task = fr"Task_report.xlsx"
    # --- Caricamento dei dati ---
    try:
        all_sheets = pd.read_excel(path_task, sheet_name=None)
    except FileNotFoundError:
        st.error("File non trovato. Verifica il percorso del file.")
        st.stop() # Interrompe l'esecuzione se il file non esiste

    sheet = 'Task_giornaliero'

    col1, col2 = st.columns(2)
    send_option = col1.radio("Seleziona la tipologia di invio della mail 👇",["Giornaliero", "Settimanale", "Mensile"], horizontal = True, index=0)

    df_task_write = all_sheets.get(sheet, pd.DataFrame(columns=['TASK', 'STATUS']))    
    select_task = col1.selectbox("**Seleziona il TASK**",df_task_write['TASK'].tolist(), index =0)

    ricerca = 'Data Analysis & Reporting' #si riferisce alla colonna `Tipologia` del file excel
    
    if send_option == "Giornaliero":
        sheet = 'Task_giornaliero'
        task_text = get_task_text(select_task, sheet)
        if task_text:
            subject = col1.text_input("Oggetto mail", f"{task_text} - giornaliero")
    elif send_option == "Settimanale":    
        sheet = 'Task_settimanale'
        task_text = get_task_text(select_task, sheet)
        if task_text:
            subject = col1.text_input("Oggetto mail", f"{task_text} - settimanale")                  
    elif send_option == "Mensile":                    
        sheet = 'Task_mese'
        task_text = get_task_text(select_task, sheet)
        if task_text:
            subject = col1.text_input("Oggetto mail", f"{task_text} - mensile")   
               
    if col1.button('Invia',key = 'and', icon=":material/alternate_email:", use_container_width=True):
        sheets_da_aggiornare = [sheet]  
        for sheet in sheets_da_aggiornare:
            aggiorna_task_status(path_task, sheet, task_text)





# --- Percorso del file Excel ---
path_task = fr"Task_report.xlsx"

# --- Funzione per salvare tutte le modifiche su Excel ---
def save_all_sheets(writer, all_sheets_data):
    """Salva tutti i fogli di lavoro nel file Excel."""
    for sheet_name, df in all_sheets_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# --- Caricamento dei dati ---
try:
    all_sheets = pd.read_excel(path_task, sheet_name=None)
except FileNotFoundError:
    st.error("File non trovato. Verifica il percorso del file.")
    st.stop() # Interrompe l'esecuzione se il file non esiste

# --- Gestione del foglio di metadati per il reset automatico ---
metadata_sheet = '_metadata'
if metadata_sheet in all_sheets:
    df_metadata = all_sheets[metadata_sheet]
    # Assicura che la colonna sia di tipo datetime
    df_metadata['last_reset'] = pd.to_datetime(df_metadata['last_reset'])
else:
    # Se il foglio non esiste, lo crea
    df_metadata = pd.DataFrame(columns=['sheet_name', 'last_reset'])

with st.container(border=True):
    st.markdown("#### TASK ")
    
    with st.container(border=True):
        col1, col2 = st.columns([0.3, 0.7],vertical_alignment="center")
        opzioni = ["Giornaliero", "Settimanale", "Mensile"]
        selezione = col1.segmented_control(
            ''':orange-background[**Opzioni di invio e-mail**]''', opzioni, key='send', label_visibility="collapsed", default="Giornaliero"
        )

        if selezione == "Giornaliero":
            sheet = 'Task_giornaliero'
        elif selezione == "Settimanale":
            sheet = 'Task_settimanale'
        else: # Mensile
            sheet = 'Task_mese'

        # Carica il DataFrame corretto
        df_task_write = all_sheets.get(sheet, pd.DataFrame(columns=['TASK', 'STATUS']))

        code_1 = col2.checkbox("Visualizza Codice", key='code_1')

        if code_1:
            code = '''col1.markdown("#### TASK ")
            
opzioni = ["Giornaliero", "Settimanale", "Mensile"]
selezione = col1.segmented_control(
    '''':orange-background[**Opzioni di invio e-mail**]'''', opzioni, key='send', label_visibility="collapsed", default="Giornaliero"
)

if selezione == "Giornaliero":
    sheet = 'Task_giornaliero'
elif selezione == "Settimanale":
    sheet = 'Task_settimanale'
else: # Mensile
    sheet = 'Task_mese'

# Carica il DataFrame corretto
df_task_write = all_sheets.get(sheet, pd.DataFrame(columns=['TASK', 'STATUS']))

# --- Logica per il Reset Automatico ---
now = datetime.now()
needs_reset = False

# Recupera l'ultimo reset per il foglio corrente
last_reset_entry = df_metadata[df_metadata['sheet_name'] == sheet]

if last_reset_entry.empty:
    # Se non c'è mai stato un reset, lo forza per inizializzare
    needs_reset = True
else:
    last_reset_date = last_reset_entry['last_reset'].iloc[0]
    # Controllo basato sulla selezione
    if selezione == "Giornaliero" and last_reset_date.date() < now.date():
        needs_reset = True
    elif selezione == "Settimanale" and last_reset_date.isocalendar().week != now.isocalendar().week:
        needs_reset = True
    elif selezione == "Mensile" and (last_reset_date.month != now.month or last_reset_date.year != now.year):
        needs_reset = True

# Esegue il reset se necessario
if needs_reset:
    df_task_write['STATUS'] = False
    all_sheets[sheet] = df_task_write
    
    # Aggiorna o aggiunge la data di reset nei metadati
    if not last_reset_entry.empty:
        df_metadata.loc[df_metadata['sheet_name'] == sheet, 'last_reset'] = now
    else:
        new_entry = pd.DataFrame([{'sheet_name': sheet, 'last_reset': now}])
        df_metadata = pd.concat([df_metadata, new_entry], ignore_index=True)
    
    all_sheets[metadata_sheet] = df_metadata
    
    # Salva le modifiche
    with pd.ExcelWriter(path_task, engine='openpyxl') as writer:
        save_all_sheets(writer, all_sheets)
    
    st.toast(f'Task "{selezione}" resettati automaticamente! 🚀', icon='✅')

# Converte la colonna 'STATUS' in booleano per l'editor
df_task_write['STATUS'] = df_task_write['STATUS'].astype(bool)
            '''
            st.code(code, language="python")

    # --- Logica per il Reset Automatico ---
    now = datetime.now()
    needs_reset = False
    
    # Recupera l'ultimo reset per il foglio corrente
    last_reset_entry = df_metadata[df_metadata['sheet_name'] == sheet]
    
    if last_reset_entry.empty:
        # Se non c'è mai stato un reset, lo forza per inizializzare
        needs_reset = True
    else:
        last_reset_date = last_reset_entry['last_reset'].iloc[0]
        # Controllo basato sulla selezione
        if selezione == "Giornaliero" and last_reset_date.date() < now.date():
            needs_reset = True
        elif selezione == "Settimanale" and last_reset_date.isocalendar().week != now.isocalendar().week:
            needs_reset = True
        elif selezione == "Mensile" and (last_reset_date.month != now.month or last_reset_date.year != now.year):
            needs_reset = True

    # Esegue il reset se necessario
    if needs_reset:
        df_task_write['STATUS'] = False
        all_sheets[sheet] = df_task_write
        
        # Aggiorna o aggiunge la data di reset nei metadati
        if not last_reset_entry.empty:
            df_metadata.loc[df_metadata['sheet_name'] == sheet, 'last_reset'] = now
        else:
            new_entry = pd.DataFrame([{'sheet_name': sheet, 'last_reset': now}])
            df_metadata = pd.concat([df_metadata, new_entry], ignore_index=True)
        
        all_sheets[metadata_sheet] = df_metadata
        
        # Salva le modifiche
        with pd.ExcelWriter(path_task, engine='openpyxl') as writer:
            save_all_sheets(writer, all_sheets)
        
        st.toast(f'Task "{selezione}" resettati automaticamente! 🚀', icon='✅')


    # --- Interfaccia Utente ---

    # Converte la colonna 'STATUS' in booleano per l'editor
    df_task_write['STATUS'] = df_task_write['STATUS'].astype(bool)


    with st.container(border=True):
        col1, col2 = st.columns([0.3, 0.7],vertical_alignment="center")
    # Bottone di Reset Manuale
        if col1.button('Reset Manuale', icon=":material/playlist_remove:"):
            df_task_write['STATUS'] = False
            all_sheets[sheet] = df_task_write
            
            # Aggiorna anche il reset manuale nei metadati
            if not df_metadata[df_metadata['sheet_name'] == sheet].empty:
                df_metadata.loc[df_metadata['sheet_name'] == sheet, 'last_reset'] = now
            else:
                new_entry = pd.DataFrame([{'sheet_name': sheet, 'last_reset': now}])
                df_metadata = pd.concat([df_metadata, new_entry], ignore_index=True)
                
            all_sheets[metadata_sheet] = df_metadata

            with pd.ExcelWriter(path_task, engine='openpyxl') as writer:
                save_all_sheets(writer, all_sheets)
            st.success("Task resettati manualmente!")

        # Editor dei dati
        edited_df = st.data_editor(df_task_write, hide_index=True, column_order=('TASK', 'STATUS'))

        code_2 = col2.checkbox("Visualizza Codice", key='code_2')

        if code_2:
            code = '''# Bottone di Reset Manuale
if col1.button('Reset Manuale', icon=":material/playlist_remove:"):
    df_task_write['STATUS'] = False
    all_sheets[sheet] = df_task_write
    
    # Aggiorna anche il reset manuale nei metadati
    if not df_metadata[df_metadata['sheet_name'] == sheet].empty:
        df_metadata.loc[df_metadata['sheet_name'] == sheet, 'last_reset'] = now
    else:
        new_entry = pd.DataFrame([{'sheet_name': sheet, 'last_reset': now}])
        df_metadata = pd.concat([df_metadata, new_entry], ignore_index=True)
        
    all_sheets[metadata_sheet] = df_metadata

    with pd.ExcelWriter(path_task, engine='openpyxl') as writer:
        save_all_sheets(writer, all_sheets)
    st.success("Task resettati manualmente!")

# Editor dei dati
edited_df = st.data_editor(df_task_write, hide_index=True, column_order=('TASK', 'STATUS'))
            '''
            st.code(code, language="python")



    with st.container(border=True):
        # Progress bar
        completati = edited_df['STATUS'].sum()
        totale = len(edited_df)
        percentuale = completati / totale if totale > 0 else 0
        st.progress(
            percentuale,
            text=f"Task completati :material/chevron_forward: {completati} di {totale} ({percentuale:.0%})"
        )

        col1, col2 = st.columns([0.15, 0.85],vertical_alignment="center")
        # Pulsante per salvare le modifiche
        if col1.button("Salva modifiche"):
            all_sheets[sheet] = edited_df
            # Non salviamo i metadati qui, solo le modifiche ai task
            with pd.ExcelWriter(path_task, engine='openpyxl') as writer:
                save_all_sheets(writer, all_sheets)
            st.success("Task aggiornati!")

        code_3 = col2.checkbox("Visualizza Codice", key='code_3')

        if code_3:
            code = '''# Progress bar
completati = edited_df['STATUS'].sum()
totale = len(edited_df)
percentuale = completati / totale if totale > 0 else 0
st.progress(
    percentuale,
    text=f"Task completati :material/chevron_forward: {completati} di {totale} ({percentuale:.0%})"
)

# Pulsante per salvare le modifiche
if st.button("Salva modifiche"):
    all_sheets[sheet] = edited_df
    # Non salviamo i metadati qui, solo le modifiche ai task
    with pd.ExcelWriter(path_task, engine='openpyxl') as writer:
        save_all_sheets(writer, all_sheets)
    st.success("Task aggiornati!")
            '''
            st.code(code, language="python")            