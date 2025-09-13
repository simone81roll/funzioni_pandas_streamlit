import streamlit as st
import numpy as np
import pandas as pd

st.subheader("Operazioni comuni con NumPy... applicate ai DataFrame di Pandas!", divider='blue')

# --- 1. CREIAMO UN DATAFRAME DI ESEMPIO ---
# Questo DataFrame sarà la base per tutti i nostri esempi.
# È molto più realistico di un semplice array.
dati = {
    'Nome': ['Anna', 'Marco', 'Sofia', 'Luca', 'Elena', 'Giovanni'],
    'Dipartimento': ['Vendite', 'IT', 'Marketing', 'Vendite', 'IT', 'Marketing'],
    'Età': [28, 45, 31, 29, 38, 52],
    'Stipendio': [2500.0, 4100.0, 2800.0, 2600.0, np.nan, 3900.0] # Aggiungiamo un valore mancante!
}
df = pd.DataFrame(dati)

st.write("In questa guida, useremo il seguente DataFrame di Pandas come esempio:")
st.dataframe(df)
st.info("Nota: La colonna 'Stipendio' contiene un valore mancante (`NaN`) che impareremo a gestire.")

#************************************************************************************************************************************************************************************
with st.expander("**:gear: Creazione di Array... da un DataFrame!**"):
    st.write("Nel lavoro di tutti i giorni, raramente creiamo array da zero. Più spesso, li estraiamo da dati già esistenti, come un DataFrame.")

    st.write("#### Come ottenere un array NumPy da una colonna del DataFrame")
    st.write("Ogni colonna di un DataFrame (`Series`) può essere facilmente convertita in un array NumPy usando l'attributo `.to_numpy()`.")
    code = """
# Selezioniamo la colonna 'Stipendio' e la convertiamo in un array NumPy
stipendi_array = df['Stipendio'].to_numpy()
    """
    st.code(code, language="python")
    st.write("Risultato (un puro array NumPy):")
    stipendi_array = df['Stipendio'].to_numpy()
    st.code(str(stipendi_array))
    st.write("Ora possiamo usare tutte le funzioni NumPy su questo array!")

#************************************************************************************************************************************************************************************
with st.expander("**:chart_with_upwards_trend: Operazioni Matematiche e Statistiche**"):
    st.write("Questo è il cuore di NumPy: calcolare metriche e aggregare dati. Vediamo come farlo sulle colonne del nostro DataFrame.")
    
    st.write("Useremo le colonne 'Età' e 'Stipendio' per gli esempi:")
    st.code(str(df[['Età', 'Stipendio']]))

    st.write("#### 1. Funzioni di aggregazione su una colonna")
    st.write("Possiamo applicare le funzioni NumPy direttamente a una Series di Pandas.")
    code = """
# Calcoliamo la media delle età
media_eta = np.mean(df['Età'])

# Calcoliamo lo stipendio massimo (ignorando i valori mancanti)
stipendio_max = np.nanmax(df['Stipendio']) # Usiamo nanmax per ignorare i NaN

# Calcoliamo la deviazione standard degli stipendi
dev_std_stipendi = np.nanstd(df['Stipendio'])
    """
    st.code(code, language="python")
    st.write(f"**Media delle età:** {np.mean(df['Età']):.2f} anni")
    st.write(f"**Stipendio massimo:** {np.nanmax(df['Stipendio']):.2f} €")
    st.write(f"**Deviazione Standard degli Stipendi:** {np.nanstd(df['Stipendio']):.2f} €")
    
    st.write("#### 2. Operazioni per asse (`axis`) su dati numerici")
    st.write("Per usare `axis`, prima selezioniamo solo le colonne numeriche e le convertiamo in un array NumPy.")
    dati_numerici = df[['Età', 'Stipendio']].to_numpy()
    code = """
# Selezioniamo solo le colonne numeriche
dati_numerici = df[['Età', 'Stipendio']].to_numpy()

# Media per ogni colonna (Età, Stipendio)
media_colonne = np.nanmean(dati_numerici, axis=0)
    """
    st.code(code, language="python")
    st.write("Risultato `np.nanmean(..., axis=0)` (media di Età e Stipendio):")
    st.code(str(np.nanmean(dati_numerici, axis=0)))

#************************************************************************************************************************************************************************************
with st.expander("**:mag: Selezione, Indicizzazione e Filtro**"):
    st.write("Estrarre dati che soddisfano certe condizioni è fondamentale.")

    st.write("#### 1. Filtro Booleano (la funzione più importante!)")
    st.write("Permette di selezionare intere righe del DataFrame che soddisfano una condizione.")
    code = """
# 1. Creiamo la condizione sulla colonna 'Età'
condizione = df['Età'] > 35

# 2. Usiamo la condizione per filtrare l'intero DataFrame
dipendenti_senior = df[condizione]
    """
    st.code(code, language="python")
    st.write("Risultato del filtro `df[df['Età'] > 35]` (tutti i dipendenti con più di 35 anni):")
    st.dataframe(df[df['Età'] > 35])

    st.write("#### 2. `np.where()` - Il 'if-else' per creare nuove colonne")
    st.write("È perfetto per creare una nuova colonna basata su una condizione di un'altra.")
    code = """
# Creiamo una nuova colonna 'Seniority'
# Se l'età è > 40, il valore è 'Senior', altrimenti 'Junior'
df['Seniority'] = np.where(df['Età'] > 40, 'Senior', 'Junior')
    """
    st.code(code, language="python")
    df['Seniority'] = np.where(df['Età'] > 40, 'Senior', 'Junior')
    st.write("Risultato (DataFrame con la nuova colonna):")
    st.dataframe(df)
    
    st.write("#### 3. `np.argmax()` - Trovare la posizione del valore massimo")
    st.write("Ci dice l'**indice** (la posizione) del valore massimo in una colonna. Utile per trovare la riga corrispondente.")
    code = """
# Troviamo l'indice dello stipendio più alto.
# Usiamo .to_numpy() per essere sicuri, ma spesso funziona anche senza.
# Nota: np.argmax non gestisce i NaN, quindi prima dobbiamo riempirli.
stipendi_senza_nan = df['Stipendio'].fillna(0) # Sostituiamo temporaneamente i NaN con 0
pos_stipendio_max = np.argmax(stipendi_senza_nan.to_numpy())
    """
    st.code(code, language="python")
    stipendi_senza_nan = df['Stipendio'].fillna(0)
    pos_stipendio_max = np.argmax(stipendi_senza_nan.to_numpy())
    st.write(f"**Lo stipendio più alto si trova in posizione (indice): {pos_stipendio_max}**")
    st.write("Possiamo usare questo indice per vedere chi è il dipendente:")
    st.dataframe(df.iloc[[pos_stipendio_max]])


#************************************************************************************************************************************************************************************
with st.expander("**:wrench: Manipolazione e Pulizia Dati**"):

    st.write("#### 1. `np.unique()` - Trovare valori unici in una colonna")
    st.write("Perfetto per le colonne categoriche, come 'Dipartimento'.")
    code = """
dipartimenti_unici = np.unique(df['Dipartimento'])
    """
    st.code(code, language="python")
    st.write("Risultato:")
    st.code(str(np.unique(df['Dipartimento'])))

    st.write("#### 2. Gestire Valori Mancanti (`np.nan`) con NumPy")
    st.write("Il nostro DataFrame ha un `NaN` nella colonna 'Stipendio'. Vediamo come trovarlo e sostituirlo.")
    
    code_nan = """
# Contare quanti valori mancanti ci sono nella colonna 'Stipendio'
# np.isnan() crea un array booleano (True dove è NaN)
# np.sum() somma i True (che valgono 1)
quanti_mancanti = np.sum(np.isnan(df['Stipendio']))

# Calcolare la media degli stipendi ignorando i NaN
media_stipendi = np.nanmean(df['Stipendio'])

# Creare una nuova colonna 'Stipendio_Pulito' dove i NaN
# sono sostituiti dalla media, usando np.where()
df['Stipendio_Pulito'] = np.where(
    np.isnan(df['Stipendio']),    # Condizione: se lo stipendio è NaN...
    media_stipendi,               # ...metti la media...
    df['Stipendio']               # ...altrimenti, lascia lo stipendio originale.
)
    """
    st.code(code_nan, language="python")

    quanti_mancanti = np.sum(np.isnan(df['Stipendio']))
    st.write(f"**Numero di valori mancanti in 'Stipendio':** {quanti_mancanti}")

    media_stipendi = np.nanmean(df['Stipendio'])
    df['Stipendio_Pulito'] = np.where(np.isnan(df['Stipendio']), media_stipendi, df['Stipendio'])
    st.write(f"**Media calcolata (ignorando i NaN):** {media_stipendi:.2f} €")
    st.write("**DataFrame con la colonna 'Stipendio_Pulito':**")
    st.dataframe(df[['Nome', 'Stipendio', 'Stipendio_Pulito']])