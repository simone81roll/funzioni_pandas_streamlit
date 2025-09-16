import pandas as pd
import streamlit as st
from datetime import date, timedelta, datetime, time
import numpy as np
from jinja2_function import create_html_df



today = date.today()
today_ggmm = today.strftime("%d/%m")
ora_attuale = datetime.now()
ora_aggiunta = ora_attuale + timedelta(hours=2)
anno_corrente = datetime.now().year
month_today = today.month

data_ordini = {
    'ID_ordine': [101, 102, 103, 104, 105, 106, 107, 108],
    'ID_cliente': [1, 3, 2, 1, 5, 6, 10, 4],
    'data_ordine': pd.to_datetime(['2024-01-15', '2024-01-17', '2024-02-01', '2024-02-05', '2024-02-10', '2024-03-01', '2024-03-05', '2024-03-10']),
    'Prodotto': ['Telecaster', 'Stratocaster', 'Les Paul', 'SG', 'Jazzmaster','Es-335','Gretsch White Falcon','Flying V'],
    'importo': [150.50, 200.00, 75.25, 300.00, 120.00, 80.00, 50.00, 250.00]
}
ordini = pd.DataFrame(data_ordini)

with st.expander("**:inbox_tray: Install e Import**"):
    st.write('#### Librerie necessarie per la produzione dello script')
    code = ''' pip install jinja2

from jinja2 import Environment, FileSystemLoader
    '''
    st.code(code, language="python")

#************************************************************************************************************************************************************************************
with st.expander("**:page_with_curl: Creazione File HTML con Jinja2**"):
    st.write(
        """
        **Jinja2** è un "motore di template" per Python. Ci permette di creare un modello di documento (in questo caso HTML) 
        e di inserire dinamicamente i dati provenienti da uno script Python, come un DataFrame. 
        È perfetto per generare report personalizzati.
        """
    )

    st.write("#### Struttura dei File")
    st.info("Assicurati di avere tre file nella stessa cartella: lo script di Streamlit, `jinja2_function.py` e `template.html`.")
    
    st.write("#### 1. Codice della Funzione (`jinja2_function.py`)")
    code_function = '''
from jinja2 import Environment, FileSystemLoader
import pandas as pd

def create_html_df(df: pd.DataFrame, firma: str, template_name: str) -> str:
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    header_row = df.columns.to_list()
    html_output = template.render(
        df=df,
        header_row=header_row,
        firma=firma
    )
    return html_output
    '''
    st.code(code_function, language='python')

    st.write("#### 2. Codice del Template (`template.html`)")
    code_template = '''
<!DOCTYPE html>
<html>
<head>
<title>Report Ordini</title>
<style>
    /* ... stili CSS ... */
</style>
</head>
<body>
    <h1>Report Ordini Recenti</h1>
    <table>
        <thead>
            <tr>
                {% for col_name in header_row %}
                    <th>{{ col_name }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for index, row in df.iterrows() %}
                <tr>
                    {% for item in row %}
                        <td>{{ item }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <p><i>Report generato da: <b>{{ firma }}</b></i></p>
</body>
</html>
    '''
    st.code(code_template, language='html')
    
    st.write("#### 3. Genera il tuo Report")
    
    # Usiamo il DataFrame 'ordini' già definito all'inizio dello script
    st.write("DataFrame di esempio che verrà usato per il report:")
    st.dataframe(ordini, use_container_width=True, hide_index=True)
    
    # Campo di testo per inserire la firma
    firma_utente = st.text_input("Inserisci il tuo nome per la firma del report", "Mario Rossi")

    # Bottone per avviare la creazione dell'HTML
    if st.button("🚀 Genera Report HTML"):
        # Chiamata alla funzione importata
        html_generato = create_html_df(
            df=ordini, 
            firma=firma_utente, 
            template_name='template.html'
        )
        
        st.success("File HTML generato con successo!")

        # Mostra il codice HTML generato
        st.write("Anteprima del codice HTML creato:")
        st.code(html_generato, language='html')

        # Aggiunge un bottone per il download del file
        st.download_button(
            label="📥 Scarica Report (.html)",
            data=html_generato,
            file_name="report_ordini.html",
            mime="text/html"
        )


with st.expander("**:pencil: Esempi utilizzati in altri report**"):
    st.write(
        """
        **Jinja2** in questo caso avevamo un dataframe e diversi paramentri/variabili  
        sia nello script principale sia all'interno della funzione
        """
    )

    code_jinja = '''

def jinja2_utilities_bp(df_target, prod_adsl, prod_lg, gg_lavorativi, somma_intervallo, firma, sheet_name, image_path):
    
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template/BP_utilities_2025.html')

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    
    target_adsl = int(df_target['target_adsl'])
    target_energia = int(df_target['target_lg'])

    target_adsl_giornaliero = int(round(target_adsl/gg_lavorativi, 0))
    target_energia_giornaliero = int(round(target_energia/gg_lavorativi, 0))

    media_adsl = int(round(prod_adsl/somma_intervallo,0))
    media_energia = int(round(prod_lg/somma_intervallo, 0))
    
    denominatore = gg_lavorativi - somma_intervallo
    if denominatore == 0:
        new_target_adsl = '-'
        new_target_energia = '-'
    else:    
        new_target_adsl = int(round((target_adsl - prod_adsl)/(gg_lavorativi-somma_intervallo),0))
        new_target_energia = int(round((target_energia - prod_lg)/(gg_lavorativi-somma_intervallo),0))

    html_output = template.render(
        target_adsl=target_adsl,
        target_energia=target_energia,
        target_adsl_giornaliero=target_adsl_giornaliero,
        target_energia_giornaliero=target_energia_giornaliero,
        prod_adsl=prod_adsl,
        prod_lg=prod_lg,
        media_adsl=media_adsl,
        media_energia=media_energia,
        new_target_adsl=new_target_adsl,
        new_target_energia=new_target_energia,
        today = today,
        firma=firma,
        sheet_name=sheet_name,
        image_path=image_path
    )

    return html_output
    '''
    st.code(code_jinja, language='python')