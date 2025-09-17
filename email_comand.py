import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
import io

st.subheader("✉️ Inviare Email con Python", divider='blue')

# Funzione per ottenere la lista degli account disponibili
def get_available_accounts():
    accounts = []
    passwords = []
    if "email" in st.secrets:
        if "account1" in st.secrets["email"]:
            username = st.secrets["email"]["account1"]["username"]
            password = st.secrets["email"]["account1"]["password"]
            accounts.append(username)
            passwords.append(password)
        if "account2" in st.secrets["email"]:
            username = st.secrets["email"]["account2"]["username"]
            password = st.secrets["email"]["account2"]["password"]            
            accounts.append(username)
            passwords.append(password)    
    return accounts, passwords

def send_email(html_content, to_email, subject, from_email, login, password, cc_email):

    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]

    # Crea l'oggetto del messaggio
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    if cc_email:
        msg['Cc'] = cc_email

    # Aggiungi il contenuto HTML
    msg.attach(MIMEText(html_content, 'html'))

    all_recipients = [email.strip() for email in to_email.split(',')]
    if cc_email:
        all_recipients += [email.strip() for email in cc_email.split(',')]
    
    # Invia l'email
    try:    
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Inizializza la connessione TLS
            server.login(login, password)  # Effettua il login
            server.send_message(msg)  # Invia il messaggio
            return True
            
    except Exception as e:
        st.error(f"Errore nell'invio dell'email: {e}")
        return False

# --- INIZIO SEZIONE EMAIL ---

with st.expander("**:key: Preparazione all'Invio di Email con Gmail e Streamlit**"):
    st.write(
        """
        Questa guida ti mostra come inviare email in modo sicuro da un'app Streamlit usando un account Gmail.
        Per ragioni di sicurezza, non useremo la tua password principale, ma una speciale "Password per le app".
        """
    )
    
    # --- PASSO 1: PASSWORD GMAIL ---
    st.subheader("Passo 1: Creare una 'Password per le app' in Gmail")
    st.write(
        """
        Dato che la **Verifica in 2 passaggi** è attiva sulla maggior parte degli account Google, non puoi usare la tua password standard per accedere da app di terze parti come il nostro script Python. Devi generare una password specifica per questa app.
        """
    )
    st.markdown(
        """
        1.  Vai al tuo **Account Google** cliccando sull'icona del tuo profilo in alto a destra in qualsiasi pagina Google e selezionando "Gestisci il tuo Account Google".
        2.  Nel menu a sinistra, vai alla sezione **Sicurezza**.
        3.  Scorri verso il basso fino al riquadro "Come accedi a Google" e assicurati che la **Verifica in 2 passaggi** sia **Attiva**. Se non lo è, attivala.
        4.  Sempre in quel riquadro, clicca su **Password per le app**.
        5.  Potrebbe venirti chiesto di inserire nuovamente la password del tuo account.
        6.  Nella pagina "Password per le app", clicca su "Seleziona app" e scegli **Posta**.
        7.  Clicca su "Seleziona dispositivo" e scegli **Computer Windows** (o un'altra opzione a tua scelta).
        8.  Clicca su **Genera**.
        """
    )
    st.warning("**Importante**: Google ti mostrerà una password di 16 caratteri. Copiala e salvala immediatamente. Una volta chiusa la finestra, non potrai più visualizzarla.")
    
    # --- PASSO 2: FILE SECRETS.TOML ---
    st.subheader("Passo 2: Configurare il file `secrets.toml`")
    st.write(
        """
        Per non scrivere le tue credenziali direttamente nel codice (una pratica molto insicura), useremo il sistema di gestione dei segreti di Streamlit.
        
        1.  Nella cartella principale del tuo progetto, crea una nuova cartella chiamata `.streamlit`.
        2.  All'interno di questa cartella, crea un file chiamato `secrets.toml`.
        3.  Incolla e compila il seguente contenuto nel file, usando la **password per le app di 16 caratteri** che hai appena generato.
        """
    )
    code_secrets = '''
# .streamlit/secrets.toml

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587

[email.account1]
username = "tua_prima_email@gmail.com"
password = "TUA_PASSWORD_PER_LE_APP_DI_16_CARATTERI"

# Puoi aggiungere un secondo account se necessario
[email.account2]
username = "tua_seconda_email@gmail.com"
password = "ALTRA_PASSWORD_PER_LE_APP"
'''
    st.code(code_secrets, language='toml')

with st.expander("**:package: Importazione librerie**"):
    st.write('#### Librerie necessarie per la produzione dello script')
    code = ''' import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
import io
    '''
    st.code(code, language="python")

with st.expander("**:key: Script per l'invio**"):    
    st.write('#### Integrare il codice in Streamlit')
    st.write('''Possiamo creare un file chiamato, ad esempio **funzioni_mail.py**, da richiamare all'occorrenza con le seguenti funzioni:
        '''
        )

    code_functions = '''
def get_available_accounts():
    accounts = []
    passwords = []
    if "email" in st.secrets:
        if "account1" in st.secrets["email"]:
            username = st.secrets["email"]["account1"]["username"]
            password = st.secrets["email"]["account1"]["password"]
            accounts.append(username)
            passwords.append(password)
        if "account2" in st.secrets["email"]:
            username = st.secrets["email"]["account2"]["username"]
            password = st.secrets["email"]["account2"]["password"]            
            accounts.append(username)
            passwords.append(password)    
    return accounts, passwords

def send_email(html_content, to_email, subject, from_email, login, password, cc_email):

    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]

    # Crea l'oggetto del messaggio
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    if cc_email:
        msg['Cc'] = cc_email

    # Aggiungi il contenuto HTML
    msg.attach(MIMEText(html_content, 'html'))

    all_recipients = [email.strip() for email in to_email.split(',')]
    if cc_email:
        all_recipients += [email.strip() for email in cc_email.split(',')]
    
    # Invia l'email
    try:    
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Inizializza la connessione TLS
            server.login(login, password)  # Effettua il login
            server.send_message(msg)  # Invia il messaggio
            return True
            
    except Exception as e:
        st.error(f"Errore nell'invio dell'email: {e}")
        return False
'''
    st.code(code_functions, language='python')
    
    st.write("##### Richiamare le funzioni per procedere all'invio:")
    st.write('''In questo esempio pratico abbiamo una funzione che legge una DL salvata in un database **SQLite3**
        PS: possiamo pensare di salvare la seguente funzione sempre nel file **funzioni_mail.py**
        '''
        )    

    code_mail_db = '''
path_mail = percorso/mail_db.db"

def get_email_addresses(tipo=None):

    conn = sq.connect(path_mail)
    cursor = conn.cursor()
    
    if tipo:
        # Recupera solo gli indirizzi di un certo tipo
        cursor.execute("SELECT id, tipo, mittente, destinatari, cc FROM mailing_list WHERE tipo = ?", (tipo,))
    else:
        # Recupera tutti gli indirizzi
        cursor.execute("SELECT id, tipo, mittente, destinatari, cc FROM mailing_list")
    
    results = cursor.fetchall()
    conn.close()
    
    # Converti i risultati in un formato più utilizzabile
    email_data = []
    for row in results:
        email_data.append({
            'id': row[0],
            'tipo': row[1],
            'mittente': row[2],
            'destinatari': row[3],
            'cc': row[4]
        })
    
    return email_data
    '''
    st.code(code_mail_db, language='python')


    st.write('''nel file principale creaiamo lo script per procedere con l'effettivo invio delle mail
        '''
        ) 

    code_invio_mail = '''
# come prima cosa importiamo le funzioni
from  funzioni_mail.py import get_available_accounts, send_email, get_email_addresses, 

#richiamiamo la funzione di jinja2 per la creazione dell'output HTML
html_output = create_html_df(
    df=ordini, #il dataframe che vogliamo inserire nel testo della mail 
    firma=firma_utente, 
    template_name='template.html'
        )

#prepariamo tutte le eventuali variabili


    '''
    st.code(code_invio_mail, language='python')

    # SOSTITUISCI IL TUO EXPANDER ":key: Script per l'invio" CON QUESTO

with st.expander("**:rocket: Esempio Pratico: Inviare un Report via Email**"):
    
    st.write(
        """
        Vediamo ora come mettere tutto insieme. In questo esempio, costruiremo uno script che:
        1.  Crea un report HTML da un DataFrame usando Jinja2.
        2.  Recupera una lista di distribuzione da un database SQLite.
        3.  Invia il report via email usando le funzioni definite in precedenza.
        """
    )

    st.write("#### 1. Funzione per leggere la Lista di Distribuzione (dal DB)")
    st.info("Per questo esempio, ipotizziamo di avere un file database `mail_db.db` con una tabella `mailing_list`.")
    
    code_mail_db = '''
# Funzione da inserire in un file di utility come 'funzioni_mail.py'
import sqlite3 as sq

def get_email_addresses(db_path, tipo=None):
    """
    Recupera indirizzi email da una tabella 'mailing_list' in un database SQLite.
    """
    conn = sq.connect(db_path)
    cursor = conn.cursor()
    
    if tipo:
        cursor.execute("SELECT tipo, mittente, destinatari, cc FROM mailing_list WHERE tipo = ?", (tipo,))
    else:
        cursor.execute("SELECT tipo, mittente, destinatari, cc FROM mailing_list")
    
    results = cursor.fetchall()
    conn.close()
    
    email_data = [{'tipo': r[0], 'mittente': r[1], 'destinatari': r[2], 'cc': r[3]} for r in results]
    return email_data
    '''
    st.code(code_mail_db, language='python')

    st.write("#### 2. Script Principale per la Composizione e l'Invio")
    st.write(
        """
        Nello script principale della nostra app Streamlit, importiamo le funzioni necessarie
        e costruiamo l'interfaccia utente.
        """
    )

    code_invio_mail = '''
# Importiamo le funzioni che abbiamo preparato
# from funzioni_mail import get_available_accounts, send_email, get_email_addresses
# from funzioni_jinja import create_html_df # Funzione per creare l'HTML

accounts, passwords = get_available_accounts()

if not accounts:
    st.error("Nessun account email configurato in secrets.toml!")
else:
    with st.container():    
        data_invio = 'GG/MM/AAAA'
        subject = st.text_input("Oggetto mail", f"Dataframe degli ordini aggiornato al {data_invio}")                   
        
        col1, col2, col3,col4  = st.columns(4)
        success = False
        html_output_saved = False               
        with col1:
            email_data = get_email_addresses()
            tipi_email = list(set([data['tipo'] for data in email_data]))
            tipo_selezionato = "TEST" #fa riferimento alla tabella presente nel database SQLite3 creato per le DL
            email_details = [data for data in email_data if data['tipo'] == tipo_selezionato][0]

            if st.button('Invia mail',key = 'send', icon=":material/alternate_email:", use_container_width=True):
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

    if success:
        st.success("Email inviata con successo!")
    '''
    st.code(code_invio_mail, language='python')

# SOSTITUISCI IL TUO EXPANDER ":package: Altre funzioni di esempiio utilizzate" CON QUESTO

with st.expander("**:paperclip: Funzioni Avanzate: Invio con Allegati e Immagini Integrate**"):
    
    st.write(
        """
        È possibile rendere le email ancora più complete allegando file (es. PDF, Excel) o integrando immagini direttamente nel corpo del messaggio (es. un logo aziendale).
        
        - **Allegato (Attachment):** Il file viene inviato "a parte" e il destinatario può scaricarlo. Si usa `MIMEBase`.
        - **Immagine Integrata (Embedded):** L'immagine viene visualizzata direttamente nel corpo dell'email. Si usa `MIMEImage` con un `Content-ID`.
        """
    )

    code_att_file_img = '''
# Funzione modificata per gestire sia allegati che immagini integrate
def send_email_advanced(html_content, to_email, subject, from_email, login, password, cc_email=None, attachment_path=None, image_path=None):
    
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]

    msg = MIMEMultipart('related') # 'related' è importante per le immagini integrate
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    if cc_email:
        msg['Cc'] = cc_email

    # Crea una parte alternativa per il testo HTML
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_content, 'html'))

    # Immagine integrata (se specificata)
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            # Il Content-ID deve corrispondere al 'cid:' nel tag <img> dell'HTML
            # Esempio: <img src="cid:logo_aziendale">
            img.add_header('Content-ID', '<logo_aziendale>')
            msg.attach(img)

    # Allegato (se specificato)
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)
    
    # Logica di invio (invariata)
    try:    
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(login, password)
            server.send_message(msg)
            return True
    except Exception as e:
        st.error(f"Errore nell'invio dell'email: {e}")
        return False
    '''
    st.code(code_att_file_img, language='python')