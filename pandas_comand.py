import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time


today = date.today()
month_today = today.month
anno_corrente = datetime.now().year

st.subheader("🐼 Operazioni comuni sui DataFrame con PANDAS", divider ='blue')

with st.expander("**:package: Importazione librerie**"):
    st.write('#### Librerie necessarie per la produzione dello script')
    code = ''' import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta, datetime, time
    '''
    st.code(code, language="python")

#************************************************************************************************************************************************************************************
with st.expander("**:inbox_tray: Creazione e visualizzazione di un dataframe**"):
    st.write('#### 1. DataFrame Clienti')
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

    st.write('#### 2. DataFrame Ordini')
    code = '''    data_ordini = {
        'ID_ordine': [101, 102, 103, 104, 105, 106, 107, 108],
        'ID_cliente': [1, 3, 2, 1, 5, 6, 10, 4],
        'data_ordine': pd.to_datetime(['2024-01-15', '2024-01-17', '2024-02-01', '2024-02-05', '2024-02-10', '2024-03-01', '2024-03-05', '2024-03-10']),
        'Prodotto': ['Telecaster', 'Stratocaster', 'Les Paul', 'SG', 'Jazzmaster','Es-335','Gretsch White Falcon','Flying V'],
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
        'Prodotto': ['Telecaster', 'Stratocaster', 'Les Paul', 'SG', 'Jazzmaster','Es-335','Gretsch White Falcon','Flying V'],
        'importo': [150.50, 200.00, 75.25, 300.00, 120.00, 80.00, 50.00, 250.00]
    }
    ordini = pd.DataFrame(data_ordini)
    st.dataframe(ordini, use_container_width=True, hide_index = True)

    st.write('#### 3. DataFrame editabile (con streamlit)')
    code = ''' edited_ordini = st.data_editor(ordini, num_rows="dynamic")
    '''
    st.code(code, language="python")
    edited_ordini = st.data_editor(ordini, num_rows="dynamic")

#************************************************************************************************************************************************************************************
with st.expander("**:pencil: Aggiungere/Rinominare/Ordinare & Rimuovere colonne**"):
    df_filtrato = ordini.copy()

    st.write('#### 1. Aggiungi colonna')
    code = '''
    # Aggiunge una colonna 'Anno Corrente' con il valore dell'anno attuale per ogni riga
    df_filtrato['Anno Corrente'] = datetime.now().year
    '''
    st.code(code, language="python")
    df_filtrato['Anno Corrente'] = anno_corrente
    st.dataframe(df_filtrato, use_container_width=True, hide_index = True)

    st.write('#### 2. Rinomina colonna')
    code = '''
    # Rinomina la colonna 'Prodotto' in 'Modello Chitarra'
    df_filtrato = df_filtrato.rename(columns = {'Prodotto': 'Modello Chitarra'})
    '''
    st.code(code, language="python")
    df_filtrato_renamed = df_filtrato.rename(columns = {'Prodotto': 'Modello Chitarra'})
    st.dataframe(df_filtrato_renamed, use_container_width=True, hide_index = True)


    st.write('#### 3. Ordina & Rimuovi colonne')
    st.write("Per riordinare o rimuovere colonne, è sufficiente creare una lista con i nomi delle colonne desiderate nell'ordine prescelto. Le colonne non incluse nella lista verranno escluse.")
    code = '''
    # Seleziona e riordina solo alcune colonne del DataFrame
    df_filtrato_selezionato = df_filtrato[['ID_ordine', 'data_ordine', 'ID_cliente', 'importo']]
    '''
    st.code(code, language="python")
    df_filtrato_selezionato = df_filtrato[['ID_ordine', 'data_ordine', 'ID_cliente', 'importo']]
    st.dataframe(df_filtrato_selezionato, use_container_width=True, hide_index = True)

#************************************************************************************************************************************************************************************
with st.expander("**:mag: Selezionare Dati con .loc e .iloc**"):
    st.write("`.loc` e `.iloc` sono i metodi principali per selezionare dati in un DataFrame.")
    st.write("- **`.loc`** seleziona i dati basandosi sulle **etichette** (nomi di righe e colonne).")
    st.write("- **`.iloc`** seleziona i dati basandosi sulla loro **posizione intera** (indici numerici).")
    
    df_loc_iloc = ordini.copy()
    df_loc_iloc.index = [f"Riga_{i}" for i in range(len(df_loc_iloc))] # Aggiungiamo etichette di indice per l'esempio con .loc

    st.write("DataFrame di esempio con indici personalizzati:")
    st.dataframe(df_loc_iloc)

    st.write("#### 1. Selezionare righe con `.loc` (per etichetta)")
    code = """
# Selezioniamo le righe con etichetta da 'Riga_1' a 'Riga_3'
df_loc_iloc.loc['Riga_1':'Riga_3']
    """
    st.code(code, language='python')
    st.dataframe(df_loc_iloc.loc['Riga_1':'Riga_3'])

    st.write("#### 2. Selezionare righe e colonne con `.loc`")
    code = """
# Selezioniamo le righe 'Riga_0' e 'Riga_4' e le colonne 'Prodotto' e 'importo'
df_loc_iloc.loc[['Riga_0', 'Riga_4'], ['Prodotto', 'importo']]
    """
    st.code(code, language='python')
    st.dataframe(df_loc_iloc.loc[['Riga_0', 'Riga_4'], ['Prodotto', 'importo']])

    st.write("#### 3. Selezionare righe con `.iloc` (per posizione)")
    code = """
# Selezioniamo le prime 3 righe (dalla posizione 0 alla 2)
df_loc_iloc.iloc[0:3]
    """
    st.code(code, language='python')
    st.dataframe(df_loc_iloc.iloc[0:3])

    st.write("#### 4. Selezionare un valore specifico con `.iloc`")
    code = """
# Selezioniamo il valore alla riga in posizione 1 e colonna in posizione 3 ('Stratocaster')
df_loc_iloc.iloc[1, 3]
    """
    st.code(code, language='python')
    st.write(df_loc_iloc.iloc[1, 3])

#************************************************************************************************************************************************************************************
with st.expander("**:arrow_up_down: Ordinare i Dati con .sort_values()**"):
    st.write("La funzione `sort_values()` permette di ordinare un DataFrame in base ai valori di una o più colonne.")
    
    st.write("#### 1. Ordinare per una colonna in ordine crescente")
    code = """
# Ordiniamo il DataFrame degli ordini per importo, dal più piccolo al più grande
ordini.sort_values(by='importo')
    """
    st.code(code, language='python')
    st.dataframe(ordini.sort_values(by='importo'), use_container_width=True, hide_index=True)

    st.write("#### 2. Ordinare per una colonna in ordine decrescente")
    code = """
# Ordiniamo per importo in modo decrescente usando ascending=False
ordini.sort_values(by='importo', ascending=False)
    """
    st.code(code, language='python')
    st.dataframe(ordini.sort_values(by='importo', ascending=False), use_container_width=True, hide_index=True)

    st.write("#### 3. Ordinare per più colonne")
    st.write("Se ci sono valori uguali nella prima colonna, Pandas userà la seconda colonna per spareggiare.")
    df_multi_sort = clienti.copy() # Usiamo il df clienti che ha città duplicate
    code = """
# Ordiniamo prima per 'citta' e poi per 'nome_cliente'
df_multi_sort.sort_values(by=['citta', 'nome_cliente'])
    """
    st.code(code, language='python')
    st.dataframe(df_multi_sort.sort_values(by=['citta', 'nome_cliente']), use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:hole: Gestione dei valori mancanti**"):
    # Aggiungiamo un paio di valori mancanti a titolo dimostrativo
    ordini_missing = ordini.copy()
    ordini_missing.loc[2, 'Prodotto'] = np.nan
    ordini_missing.loc[5, 'importo'] = np.nan

    st.write("DataFrame con valori mancanti simulati:")
    st.dataframe(ordini_missing, use_container_width=True, hide_index=True)

    st.write("#### 1. Contare i valori mancanti")
    st.write("Usiamo `df.isnull().sum()` per vedere quanti valori mancanti ci sono in ogni colonna.")
    code = """
    conteggio_nan = ordini_missing.isnull().sum()
    """
    st.code(code, language="python")
    conteggio_nan = ordini_missing.isnull().sum()
    st.code(conteggio_nan)

    st.write("#### 2. Rimuovere le righe con valori mancanti")
    st.write("Usiamo `df.dropna()` per eliminare le righe che contengono almeno un valore mancante.")
    code = """
    df_pulito_dropna = ordini_missing.dropna()
    """
    st.code(code, language="python")
    df_pulito_dropna = ordini_missing.dropna()
    st.dataframe(df_pulito_dropna, use_container_width=True, hide_index=True)

    st.write("#### 3. Sostituire i valori mancanti")
    st.write("Usiamo `df.fillna()` per sostituire i valori mancanti con un valore a nostra scelta.")
    code = """
    # Sostituiamo i NaN nella colonna 'Prodotto' con 'Non Specificato'
    # e i NaN nella colonna 'importo' con 0.
    df_pulito_fillna = ordini_missing.fillna({'Prodotto': 'Non Specificato', 'importo': 0})
    """
    st.code(code, language="python")
    df_pulito_fillna = ordini_missing.fillna({'Prodotto': 'Non Specificato', 'importo': 0})
    st.dataframe(df_pulito_fillna, use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:page_facing_up: Gestire i Duplicati**"):
    # Creiamo un DataFrame con un duplicato
    clienti_duplicati = pd.concat([clienti, clienti.iloc[[0]]], ignore_index=True)
    
    st.write("Per gestire i dati duplicati, prima si identificano e poi si decide come trattarli. La causa più comune è un errore di inserimento dati.")
    st.write("DataFrame di esempio con una riga duplicata (Mario Rossi):")
    st.dataframe(clienti_duplicati, use_container_width=True, hide_index=True)

    st.write("#### 1. Trovare i duplicati")
    st.write("Usiamo `.duplicated().sum()` per contare quante righe sono duplicati esatti di righe precedenti.")
    code = """
# Conta il numero di righe duplicate
clienti_duplicati.duplicated().sum()
    """
    st.code(code, language='python')
    st.write(f"Numero di righe duplicate: **{clienti_duplicati.duplicated().sum()}**")

    st.write("#### 2. Rimuovere i duplicati")
    st.write("Usiamo `.drop_duplicates()` per creare un nuovo DataFrame senza le righe duplicate. Di default, mantiene la prima occorrenza.")
    code = """
# Rimuove le righe duplicate, mantenendo la prima occorrenza
clienti_senza_duplicati = clienti_duplicati.drop_duplicates()
    """
    st.code(code, language='python')
    clienti_senza_duplicati = clienti_duplicati.drop_duplicates()
    st.dataframe(clienti_senza_duplicati, use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:abc: Operazioni sulle stringhe**"):
    st.write("Le colonne di tipo stringa hanno metodi speciali accessibili tramite l'attributo `.str`, che permettono di manipolare il testo in modo efficiente su intere colonne.")
    clienti_str = clienti.copy()

    st.write("#### 1. Filtrare righe con `str.contains`")
    st.write("Filtra le righe che contengono una specifica sottostringa. Simile a `LIKE` in SQL.")
    code = """
# Filtriamo i clienti che vivono a 'Roma' (case=False ignora maiuscole/minuscole)
clienti_roma = clienti_str[clienti_str['citta'].str.contains('Roma', case=False, na=False)]
    """
    st.code(code, language="python")
    clienti_roma = clienti_str[clienti_str['citta'].str.contains('Roma', case=False, na=False)]
    st.dataframe(clienti_roma, use_container_width=True, hide_index=True)

    st.write("#### 2. Cambiare Maiuscole/Minuscole con `str.lower()` e `str.upper()`")
    code = """
clienti_str['nome_minuscolo'] = clienti_str['nome_cliente'].str.lower()
clienti_str['citta_maiuscolo'] = clienti_str['citta'].str.upper()
    """
    st.code(code, language="python")
    clienti_str_case = clienti.copy()
    clienti_str_case['nome_minuscolo'] = clienti_str_case['nome_cliente'].str.lower()
    clienti_str_case['citta_maiuscolo'] = clienti_str_case['citta'].str.upper()
    st.dataframe(clienti_str_case[['nome_cliente', 'nome_minuscolo', 'citta', 'citta_maiuscolo']], use_container_width=True, hide_index=True)

    st.write("#### 3. Rimuovere spazi bianchi con `str.strip()`")
    clienti_spazi = clienti.copy()
    clienti_spazi.loc[0, 'nome_cliente'] = '  Mario Rossi  '
    st.write("DataFrame con spazi aggiunti per l'esempio:")
    st.dataframe(clienti_spazi.head(1), use_container_width=True, hide_index=True)
    code = """
clienti_spazi['nome_pulito'] = clienti_spazi['nome_cliente'].str.strip()
    """
    st.code(code, language="python")
    clienti_spazi['nome_pulito'] = clienti_spazi['nome_cliente'].str.strip()
    st.write("Stessa riga dopo la pulizia con `strip()`:")
    st.dataframe(clienti_spazi[['nome_cliente', 'nome_pulito']].head(1), use_container_width=True, hide_index=True)

    st.write("#### 4. Sostituire testo con `str.replace()`")
    code = """
clienti_sostituzione = clienti.copy()
clienti_sostituzione['nome_modificato'] = clienti_sostituzione['nome_cliente'].str.replace('Rossi', 'Gialli')
    """
    st.code(code, language="python")
    clienti_sostituzione = clienti.copy()
    clienti_sostituzione['nome_modificato'] = clienti_sostituzione['nome_cliente'].str.replace('Rossi', 'Gialli')
    st.dataframe(clienti_sostituzione, use_container_width=True, hide_index=True)

    st.write("#### 5. Dividere una colonna con `str.split()`")
    code = """
# Dividiamo 'nome_cliente' in 'Nome' e 'Cognome' usando lo spazio come separatore
clienti_split = clienti.copy()
clienti_split[['Nome', 'Cognome']] = clienti_split['nome_cliente'].str.split(' ', expand=True)
    """
    st.code(code, language="python")
    clienti_split = clienti.copy()
    clienti_split[['Nome', 'Cognome']] = clienti_split['nome_cliente'].str.split(' ', expand=True)
    st.dataframe(clienti_split, use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:sparkles: Applicare Funzioni Personalizzate con .apply()**"):
    st.write("La funzione `.apply()` è estremamente potente: permette di applicare una funzione personalizzata a ogni riga o colonna di un DataFrame.")
    apply_df = ordini.copy()
    
    st.write("#### 1. Applicare una funzione a una colonna")
    st.write("Creiamo una funzione che etichetta un ordine come 'Grande' o 'Piccolo' in base al suo importo e la applichiamo per creare una nuova colonna.")
    code = """
# 1. Definiamo una funzione
def categorizza_importo(importo):
    if importo > 150:
        return 'Grande'
    else:
        return 'Piccolo'

# 2. Applichiamo la funzione alla colonna 'importo'
apply_df['Categoria Importo'] = apply_df['importo'].apply(categorizza_importo)
    """
    st.code(code, language='python')
    
    def categorizza_importo(importo):
        if importo > 150:
            return 'Grande'
        else:
            return 'Piccolo'
            
    apply_df['Categoria Importo'] = apply_df['importo'].apply(categorizza_importo)
    st.dataframe(apply_df[['Prodotto', 'importo', 'Categoria Importo']], use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:link: Funzione merge (Join)**"):
    st.write("`pd.merge()` è l'equivalente dei `JOIN` di SQL. Permette di combinare due DataFrame basandosi su una o più colonne comuni.")
    
    st.write('#### 1. Inner Merge')
    st.write("Restituisce solo le righe dove la chiave di join (`ID_cliente`) è presente in **entrambi** i DataFrame.")
    code= ''' 
    # Uniamo clienti e ordini: vedremo solo i clienti che hanno fatto ordini.
    df_merge_inner = pd.merge(clienti, ordini, on='ID_cliente', how='inner')
    '''
    st.code(code, language="python")
    df_merge_inner = pd.merge(clienti, ordini, on='ID_cliente', how='inner')
    st.dataframe(df_merge_inner, use_container_width=True, hide_index=True)

    st.write('#### 2. Left Merge')
    st.write("Restituisce **tutte** le righe del DataFrame di sinistra (`clienti`) e le righe corrispondenti del DataFrame di destra. Se non c'è corrispondenza, i valori del df di destra saranno `NaN`.")
    code= ''' 
    df_merge_left = pd.merge(clienti, ordini, on='ID_cliente', how='left')
    '''
    st.code(code, language="python")
    df_merge_left = pd.merge(clienti, ordini, on='ID_cliente', how='left')
    st.dataframe(df_merge_left, use_container_width=True, hide_index=True)

    st.write('#### 3. Right Merge')
    st.write("Restituisce **tutte** le righe del DataFrame di destra (`ordini`) e le righe corrispondenti di sinistra. In questo caso, vedremo se ci sono ordini senza un cliente corrispondente nell'anagrafica.")
    code= ''' 
    df_merge_right = pd.merge(clienti, ordini, on='ID_cliente', how='right')
    '''
    st.code(code, language="python")
    df_merge_right = pd.merge(clienti, ordini, on='ID_cliente', how='right')
    st.dataframe(df_merge_right, use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:busts_in_silhouette: Funzione groupby (Raggruppamento)**"):
    st.write("La funzione `groupby` divide un DataFrame in gruppi basandosi su una o più colonne, applica una funzione di aggregazione (somma, media, conteggio, etc.) a ogni gruppo e combina i risultati.")

    st.write("#### 1. Somma per gruppo")
    st.write("Calcoliamo il totale speso da ogni cliente.")
    code = '''
    # Raggruppiamo per 'ID_cliente' e calcoliamo la somma di 'importo' per ciascun gruppo.
    totale_per_cliente = ordini.groupby('ID_cliente')['importo'].sum().reset_index()
    '''
    st.code(code, language="python")
    totale_per_cliente = ordini.groupby('ID_cliente')['importo'].sum().reset_index()
    st.dataframe(totale_per_cliente)

    st.write("#### 2. Conteggio per gruppo")
    st.write("Contiamo quanti ordini ha effettuato ogni cliente.")
    code = '''
    conteggio_ordini = ordini.groupby('ID_cliente')['ID_ordine'].count().reset_index()
    '''
    st.code(code, language="python")
    conteggio_ordini = ordini.groupby('ID_cliente')['ID_ordine'].count().reset_index()
    st.dataframe(conteggio_ordini.rename(columns={'ID_ordine': 'Numero di Ordini'}))

    st.write("#### 3. Usare `.agg()` per più aggregazioni")
    st.write("Calcoliamo più statistiche in una sola volta (es. somma e media) usando la funzione `agg`.")
    code = '''
    # Raggruppiamo per Prodotto e calcoliamo somma e media dell'importo.
    statistiche_prodotto = ordini.groupby('Prodotto')['importo'].agg(['sum', 'mean']).reset_index()
    '''
    st.code(code, language="python")
    statistiche_prodotto = ordini.groupby('Prodotto')['importo'].agg(['sum', 'mean']).reset_index()
    statistiche_prodotto['mean'] = statistiche_prodotto['mean'].round(2)
    st.dataframe(statistiche_prodotto)

#************************************************************************************************************************************************************************************
with st.expander("**:bar_chart: Creare Tabelle Pivot con pivot_table()**"):
    st.write("Una tabella pivot è un potente strumento per riorganizzare e riassumere i dati, trasformando i valori di una colonna in nuove colonne.")
    st.write("Per questo esempio, prima uniamo i due DataFrame per avere a disposizione anche la città del cliente.")
    
    df_pivot = pd.merge(clienti, ordini, on='ID_cliente', how='inner')

    st.write("#### Esempio: Calcolare il totale venduto per ogni prodotto in ogni città")
    code = """
# Usiamo pivot_table per avere le città come indice (righe), 
# i prodotti come colonne e la somma degli importi come valori.
# fill_value=0 sostituisce i NaN dove non ci sono vendite.
vendite_pivot = df_pivot.pivot_table(
    index='citta', 
    columns='Prodotto', 
    values='importo', 
    aggfunc='sum', 
    fill_value=0
)
    """
    st.code(code, language='python')
    vendite_pivot = df_pivot.pivot_table(index='citta', columns='Prodotto', values='importo', aggfunc='sum', fill_value=0)
    st.dataframe(vendite_pivot)
    
#************************************************************************************************************************************************************************************
with st.expander("**:inbox_tray: Filtrare con isin (Controllo Appartenenza)**"):
    st.write("La funzione `isin()` filtra un DataFrame basandosi su una lista di valori. È come chiedere: 'mostrami solo le righe dove il valore di questa colonna è presente in questa lista'. È un modo molto efficiente per eseguire un'operazione simile a un `INNER JOIN` ma restituendo solo le righe del DataFrame originale.")
    
    st.write("#### 1. Selezionare i clienti che hanno effettuato almeno un ordine")
    st.write("In questo caso, la 'lista' di ID con cui confrontarsi è la colonna `ID_cliente` del DataFrame `ordini`.")
    code = '''
# Crea una lista di ID cliente unici dal df ordini
ids_clienti_con_ordini = ordini['ID_cliente'].unique()

# Filtra il df clienti per mostrare solo quelli il cui ID è nella lista
clienti_attivi = clienti[clienti['ID_cliente'].isin(ids_clienti_con_ordini)]
    '''
    st.code(code, language="python")
    clienti_attivi = clienti[clienti['ID_cliente'].isin(ordini['ID_cliente'])]
    st.dataframe(clienti_attivi, use_container_width=True, hide_index=True)
    
    st.write("#### 2. Selezionare gli ordini che corrispondono a clienti presenti nell'anagrafica")
    st.write("Qui facciamo il contrario: filtriamo gli ordini per assicurarci che l'`ID_cliente` corrisponda a un cliente valido nell'anagrafica `clienti`.")
    code = '''
# Filtra il df ordini per mostrare solo gli ordini il cui ID_cliente
# è presente anche nel df clienti.
ordini_validi = ordini[ordini['ID_cliente'].isin(clienti['ID_cliente'])]
    '''
    st.code(code, language="python")
    ordini_validi = ordini[ordini['ID_cliente'].isin(clienti['ID_cliente'])]
    st.dataframe(ordini_validi, use_container_width=True, hide_index=True)

#************************************************************************************************************************************************************************************
with st.expander("**:mag_right: Esempio di filtri interattivi**"):
    code= ''' 
    col1, col2 = st.columns(2)
    filtro_cliente = col1.text_input('Filtra per Nome Cliente')
    filtro_citta = col2.text_input('Filtra per Città')
    
    # Crea una copia per non modificare il DataFrame originale tra i rerun
    clienti_filtrati = clienti.copy()

    if filtro_cliente:
        clienti_filtrati = clienti_filtrati[clienti_filtrati['nome_cliente'].str.contains(filtro_cliente, case=False, na=False)]
    
    if filtro_citta:
        clienti_filtrati = clienti_filtrati[clienti_filtrati['citta'].str.contains(filtro_citta, case=False, na=False)]

    st.dataframe(clienti_filtrati)
    '''
    st.code(code, language="python")
    
    col1, col2 = st.columns(2)
    filtro_cliente = col1.text_input('Filtra per Nome Cliente')
    filtro_citta = col2.text_input('Filtra per Città')

    # Ricrea una copia del df originale ad ogni esecuzione per resettare i filtri
    clienti_originale = pd.DataFrame(data_clienti)
    
    if filtro_cliente:
        clienti_originale = clienti_originale[clienti_originale['nome_cliente'].astype(str).str.contains(filtro_cliente, case=False, na=False)]
    
    if filtro_citta:
        clienti_originale = clienti_originale[clienti_originale['citta'].astype(str).str.contains(filtro_citta, case=False, na=False)]

    st.dataframe(clienti_originale, use_container_width=True, hide_index = True)
