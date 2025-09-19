import streamlit as st
import pandas as pd
import numpy as np
import json


st.subheader("💹 Creazione di grafici", divider='blue')

st.write("#### DataFrame di Esempio:")
col1, col2 = st.columns(2)
chart_data = pd.DataFrame(
    {
        "Mese": ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu"],
        "Vendite_A": [100, 120, 150, 130, 180, 210],
        "Vendite_B": [80, 90, 110, 115, 140, 160],
    }
).set_index("Mese")
df_chart_data = pd.DataFrame(chart_data)
col1.write("**Vendite**")
col1.dataframe(df_chart_data.head(), use_container_width=True)

# Creiamo un DataFrame più ricco per questi esempi
np.random.seed(0)
data = {
    'Età': np.random.randint(18, 70, size=100),
    'Paese': np.random.choice(['Italia', 'Germania', 'Francia', 'Spagna'], size=100, p=[0.4, 0.2, 0.2, 0.2]),
    'Importo_Acquisto': np.random.lognormal(mean=4, sigma=0.8, size=100).round(2)
}
df_customers = pd.DataFrame(data)

col2.write("**Clienti**")
col2.dataframe(df_customers.head(), use_container_width=True)

with st.expander("📊 **Creazione di Grafici da un DataFrame (px.scatter)**"):
    st.write(
        """
        Per un controllo completo su aspetto, etichette e interattività, la libreria **Plotly Express** è la scelta migliore.
        I grafici creati con Plotly sono completamente interattivi: puoi fare zoom, passare il mouse sui dati per vedere i dettagli e molto altro.  
        Il dataframe utilizzato è `Vendite`.
        """
    )
    
    # Aggiungiamo le importazioni necessarie per Plotly
    st.write("Prima di tutto, importa la libreria:")
    code_import_plotly = "import plotly.express as px"
    st.code(code_import_plotly, language='python')
    import plotly.express as px

    st.write("##### Grafico a Dispersione (Scatter Plot)")
    st.write("Utile per mostrare la relazione tra due variabili numeriche.")

    code_scatter = '''
# Creiamo la figura del grafico con Plotly Express
fig = px.scatter(
    chart_data, 
    x="Vendite_A", 
    y="Vendite_B", 
    title="Relazione tra Vendite Prodotto A e Prodotto B",
    labels={"Vendite_A": "Vendite del Prodotto A (€)", "Vendite_B": "Vendite del Prodotto B (€)"},
    hover_name=chart_data.index # Mostra il mese quando passi il mouse
)

# Mostriamo il grafico in Streamlit
st.plotly_chart(fig, use_container_width=True)
    '''
    st.code(code_scatter, language='python')
    
    fig = px.scatter(
        chart_data, 
        x="Vendite_A", 
        y="Vendite_B", 
        title="Relazione tra Vendite Prodotto A e Prodotto B",
        labels={"Vendite_A": "Vendite del Prodotto A (€)", "Vendite_B": "Vendite del Prodotto B (€)"},
        hover_name=chart_data.index
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("**📈 Grafici Istogramma (px.histogram)**"):
    st.write("Un **istogramma** è perfetto per capire la **distribuzione di una singola variabile numerica**. Mostra quante volte i valori cadono all'interno di determinati intervalli (chiamati *bins*).")
    st.write(
        """
        Il dataframe utilizzato è `Cliente`.
        """
    )
    
    code_hist = '''
fig_hist = px.histogram(
    df_customers, 
    x="Età", 
    nbins=20, # Specifichiamo il numero di "barre"
    title="Distribuzione dell'Età dei Clienti"
)
st.plotly_chart(fig_hist, use_container_width=True)
    '''
    st.code(code_hist, language='python')
    fig_hist = px.histogram(
        df_customers, 
        x="Età", 
        nbins=20,
        title="Distribuzione dell'Età dei Clienti"
    )
    st.plotly_chart(fig_hist, use_container_width=True)


with st.expander("**📉 Grafico a Scatola - Box Plot (px.box)**"):
    st.write("Un **box plot** è un modo potente per visualizzare la distribuzione di dati numerici e confrontarla tra diverse categorie. Mostra la mediana, i quartili e i possibili valori anomali (*outlier*).")

    code_box = '''
fig_box = px.box(
    df_customers, 
    x="Paese", 
    y="Importo_Acquisto",
    color="Paese", # Colora ogni box in modo diverso
    title="Distribuzione degli Acquisti per Paese"
)
st.plotly_chart(fig_box, use_container_width=True)
    '''
    st.code(code_box, language='python')
    fig_box = px.box(
        df_customers, 
        x="Paese", 
        y="Importo_Acquisto",
        color="Paese",
        title="Distribuzione degli Acquisti per Paese"
    )
    st.plotly_chart(fig_box, use_container_width=True)

with st.expander("**◔ Grafico a Torta - Pie Chart (px.pie)**"):    
    st.write("Un **grafico a torta** è utile per mostrare la **proporzione di ogni categoria** rispetto al totale.")

    code_pie = '''
# Calcoliamo prima i totali per paese
vendite_per_paese = df_customers.groupby('Paese')['Importo_Acquisto'].sum().reset_index()

fig_pie = px.pie(
    vendite_per_paese, 
    names="Paese", 
    values="Importo_Acquisto",
    title="Proporzione delle Vendite Totali per Paese"
)
st.plotly_chart(fig_pie, use_container_width=True)
    '''
    st.code(code_pie, language='python')
    vendite_per_paese = df_customers.groupby('Paese')['Importo_Acquisto'].sum().reset_index()
    fig_pie = px.pie(
        vendite_per_paese, 
        names="Paese", 
        values="Importo_Acquisto",
        title="Proporzione delle Vendite Totali per Paese"
    )
    st.plotly_chart(fig_pie, use_container_width=True)