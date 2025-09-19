import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.subheader("🧠 Machine Learning", divider='blue')

with st.expander("**:inbox_tray: Import**"):
    code = '''
# Importazioni necessarie    
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
    '''
    st.code(code, language="python")

with st.expander("**🤖 Machine Learning: I Primi Passi**"):
    st.write(
        """
        Il Machine Learning (ML) può sembrare complesso, ma l'idea di base è semplice: invece di scrivere regole a mano, 
        **insegniamo a un computer a trovare dei pattern nei dati**. Il computer "impara" dagli esempi che gli forniamo.
        """
    )
    st.info("Per questo esempio, assicurati di avere installato `scikit-learn`: `pip install scikit-learn`")

    st.write("### Il nostro primo modello: La Regressione Lineare")
    st.write(
        """
        Iniziamo con uno dei modelli più semplici e intuitivi: la **Regressione Lineare**. 
        L'obiettivo è trovare la **linea retta che meglio descrive la relazione tra due variabili**.
        
        **Scenario**: Vogliamo prevedere le vendite (`y`) in base alla spesa pubblicitaria (`X`).
        """
    )
    
    # Importazioni necessarie
    import numpy as np
    from sklearn.linear_model import LinearRegression
    import plotly.graph_objects as go

    st.write("#### Passo 1: Creare i dati di esempio")
    code_data_ml = '''
# Creiamo dati fittizi ma realistici
np.random.seed(42) # Rende i dati casuali ma riproducibili
spesa_pubblicitaria = np.random.rand(50, 1) * 100 # 50 valori di spesa tra 0 e 100
vendite = 2.5 * spesa_pubblicitaria + np.random.randn(50, 1) * 20 + 15 # y = 2.5x + b + rumore

df_ml = pd.DataFrame({'Spesa_Pubblicitaria': spesa_pubblicitaria.flatten(), 'Vendite': vendite.flatten()})
    '''
    st.code(code_data_ml, language='python')
    np.random.seed(42)
    spesa_pubblicitaria = np.random.rand(50, 1) * 100
    vendite = 2.5 * spesa_pubblicitaria + np.random.randn(50, 1) * 20 + 15
    df_ml = pd.DataFrame({'Spesa_Pubblicitaria': spesa_pubblicitaria.flatten(), 'Vendite': vendite.flatten()})

    st.write("#### Passo 2: Visualizzare i dati")
    st.write("Prima di tutto, guardiamo i nostri dati per vedere se c'è una relazione visiva.")
    fig_ml_scatter = px.scatter(df_ml, x='Spesa_Pubblicitaria', y='Vendite', title="Spesa Pubblicitaria vs. Vendite")
    st.plotly_chart(fig_ml_scatter, use_container_width=True)

    st.write("#### Passo 3: Addestrare il modello")
    st.write(
        """
        Ora chiediamo a `scikit-learn` di trovare la linea retta che meglio si adatta a questi punti.
        Questo processo si chiama "addestramento" o "fitting".
        """
    )
    code_train = '''
# Prepariamo i dati
X = df_ml[['Spesa_Pubblicitaria']] # Variabile indipendente (deve essere un DataFrame)
y = df_ml['Vendite']             # Variabile dipendente (la cosa che vogliamo prevedere)

# Creiamo e addestriamo il modello
model = LinearRegression()
model.fit(X, y)

st.success("Modello addestrato con successo!")
    '''
    st.code(code_train, language='python')
    X = df_ml[['Spesa_Pubblicitaria']]
    y = df_ml['Vendite']
    model = LinearRegression()
    model.fit(X, y)
    
    st.write("#### Passo 4: Fare una previsione interattiva")
    st.write("Ora che il modello ha 'imparato', possiamo usarlo per fare previsioni su nuovi dati.")
    
    spesa_utente = st.slider("Seleziona una spesa pubblicitaria (€):", 0, 100, 50)
    
    # Il modello si aspetta un array 2D, quindi usiamo [[...]]
    previsione = model.predict([[spesa_utente]])
    
    st.metric(
        label=f"Previsione di vendita per {spesa_utente}€ di spesa",
        value=f"{previsione[0]:.2f} €"
    )

    st.write("#### Passo 5: Visualizzare il risultato")
    st.write("Aggiungiamo la linea trovata dal nostro modello al grafico originale.")
    
    # Creiamo una nuova figura per mostrare la linea di regressione
    fig_ml_line = go.Figure()
    # Aggiungiamo i punti originali
    fig_ml_line.add_trace(go.Scatter(x=df_ml['Spesa_Pubblicitaria'], y=df_ml['Vendite'], mode='markers', name='Dati Reali'))
    # Aggiungiamo la linea di previsione
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range)
    fig_ml_line.add_trace(go.Scatter(x=x_range.flatten(), y=y_range, mode='lines', name='Linea di Previsione (Modello)', line=dict(color='red', width=3)))
    fig_ml_line.update_layout(title="Risultato del Modello di Regressione Lineare")
    st.plotly_chart(fig_ml_line, use_container_width=True)

with st.expander("**👾 Altri Esempi di Machine Learning: Classificazione con KNN**"):
    st.write(
        """
        Oltre alla regressione (prevedere un valore numerico), un altro compito fondamentale del ML è la **classificazione**: 
        prevedere a quale **categoria** appartiene un dato. Esempi: un'email è "spam" o "non spam"? Un cliente è "a rischio abbandono" o "fedele"?
        """
    )
    st.write("### Algoritmo: K-Nearest Neighbors (KNN)")
    st.write(
        """
        L'idea del KNN è molto semplice: per classificare un nuovo dato, guarda i suoi **'K' vicini più prossimi** nei dati di addestramento. 
        Il nuovo dato verrà assegnato alla categoria più comune tra i suoi vicini. 
        È come dire: "dimmi chi sono i tuoi amici e ti dirò chi sei".
        """
    )
    st.info("Per questo esempio, useremo il famoso dataset **Iris**, che contiene misurazioni di tre diverse specie di fiori.")

    # Importazioni necessarie
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    st.write("#### Passo 1: Caricare e visualizzare il dataset Iris")
    code_load_iris = '''
# Carichiamo il dataset, che è già incluso in scikit-learn
iris = load_iris()
df_iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df_iris['specie'] = [iris.target_names[i] for i in iris.target]

# Visualizziamo le relazioni tra le misure dei petali, colorando per specie
fig_iris = px.scatter(
    df_iris, 
    x="petal length (cm)", 
    y="petal width (cm)", 
    color="specie",
    title="Dataset Iris: Lunghezza vs. Larghezza dei Petali"
)
st.plotly_chart(fig_iris, use_container_width=True)
    '''
    st.code(code_load_iris, language='python')
    iris = load_iris()
    df_iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df_iris['specie'] = [iris.target_names[i] for i in iris.target]
    fig_iris = px.scatter(
        df_iris, 
        x="petal length (cm)", 
        y="petal width (cm)", 
        color="specie",
        title="Dataset Iris: Lunghezza vs. Larghezza dei Petali"
    )
    st.plotly_chart(fig_iris, use_container_width=True)
    st.write("Come puoi vedere, le specie diverse formano dei gruppi (cluster) abbastanza distinti. Questo è un buon segno per il nostro modello!")
    
    st.write("#### Passo 2: Suddividere i dati in Training Set e Test Set")
    st.write(
        """
        Un passo **fondamentale** nel machine learning. Non possiamo usare gli stessi dati sia per addestrare il modello che per valutarlo, 
        altrimenti sarebbe come dare a uno studente le risposte del test prima dell'esame!
        - **Training Set**: I dati che il modello usa per "imparare".
        - **Test Set**: Dati nuovi, mai visti prima, che usiamo per verificare quanto bene il modello ha imparato.
        """
    )
    code_split = '''
X = iris.data # Le 4 colonne con le misurazioni (le nostre "features")
y = iris.target # La colonna con la specie (il nostro "target")

# Suddividiamo i dati: 80% per il training, 20% per il test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    '''
    st.code(code_split, language='python')
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    st.write("#### Passo 3: Addestrare e Valutare il modello KNN")
    code_train_knn = '''
# Creiamo il modello, dicendogli di guardare i 3 vicini più prossimi (K=3)
knn_model = KNeighborsClassifier(n_neighbors=3)

# Addestriamo il modello usando solo il training set
knn_model.fit(X_train, y_train)

# Usiamo il modello addestrato per fare previsioni sul test set
y_pred = knn_model.predict(X_test)

# Calcoliamo l'accuratezza: quante previsioni ha fatto correttamente?
accuracy = accuracy_score(y_test, y_pred)
st.metric("Accuratezza del Modello sul Test Set", f"{accuracy:.2%}")
    '''
    st.code(code_train_knn, language='python')
    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(X_train, y_train)
    y_pred = knn_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.metric("Accuratezza del Modello sul Test Set", f"{accuracy:.2%}")

    st.write("#### Passo 4: Fare una previsione interattiva")
    st.write("Ora usa il modello addestrato per classificare un fiore immaginario!")
    
    col1, col2 = st.columns(2)
    sl = col1.slider("Lunghezza Sepalo (cm)", float(X[:, 0].min()), float(X[:, 0].max()), 5.1)
    sw = col2.slider("Larghezza Sepalo (cm)", float(X[:, 1].min()), float(X[:, 1].max()), 3.5)
    pl = col1.slider("Lunghezza Petalo (cm)", float(X[:, 2].min()), float(X[:, 2].max()), 1.4)
    pw = col2.slider("Larghezza Petalo (cm)", float(X[:, 3].min()), float(X[:, 3].max()), 0.2)
    
    # Prepara i dati dell'utente per la previsione
    user_input = np.array([[sl, sw, pl, pw]])
    
    # Fai la previsione
    prediction_index = knn_model.predict(user_input)[0]
    prediction_name = iris.target_names[prediction_index]
    
    st.success(f"**Il modello prevede che il fiore sia della specie: __{prediction_name.capitalize()}__** 🌸")


with st.expander("**֎🇦🇮 Esempio Avanzato: Prevedere il Volume di Chiamate con un Random Forest**"):
    st.write(
        """
        Questo è un problema pratico: come possiamo prevedere il carico di lavoro futuro basandoci sui dati storici? 
        Useremo un modello più avanzato, il **Random Forest Regressor**, che è eccellente per catturare pattern non lineari e complessi.
        
        **Obiettivo**: Prevedere il numero di chiamate per ogni ora, dal lunedì al venerdì della prossima settimana.
        """
    )
    st.info("Un **Random Forest** è un modello che costruisce un'intera 'foresta' di alberi decisionali e fa la media dei loro risultati. Questo lo rende molto più robusto e preciso di un singolo albero.")

    # Importazioni necessarie
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error
    
    st.write("#### Passo 1: Creare un Dataset di Esempio Realistico")
    st.write("Simuliamo i dati di un call center per gli ultimi 90 giorni.")
    code_gen_data = '''
def crea_dati_chiamate(giorni=90):
    date_rng = pd.to_datetime(pd.date_range(end=pd.Timestamp.now(), periods=giorni, freq='D'))
    df_list = []
    fasce_orarie = [f"{h:02d}:00/{h:02d}:59" for h in range(9, 21)]

    for data in date_rng:
        for fascia in fasce_orarie:
            ora_inizio = int(fascia.split(':')[0])
            giorno_settimana = data.dayofweek # 0=Lunedì, 6=Domenica
            
            # Simuliamo i pattern
            base_chiamate = 50
            pattern_orario = max(0, np.sin((ora_inizio - 9) * np.pi / 12) * 50) # Picco a metà giornata
            pattern_settimanale = [1.2, 1.1, 1.0, 1.05, 0.9, 0.5, 0.4] # Lunedì più impegnativo
            
            chiamate = (base_chiamate + pattern_orario) * pattern_settimanale[giorno_settimana]
            chiamate += np.random.randn() * 10 # Aggiungiamo rumore casuale
            
            df_list.append({'Data': data, 'Fascia_Oraria': fascia, 'NumeroChiamate': max(0, int(chiamate))})
            
    return pd.DataFrame(df_list)

df_chiamate = crea_dati_chiamate()
st.dataframe(df_chiamate.head(), use_container_width=True)
    '''
    st.code(code_gen_data, language='python')

    def crea_dati_chiamate(giorni=90):
        date_rng = pd.to_datetime(pd.date_range(end=pd.Timestamp.now(), periods=giorni, freq='D'))
        df_list = []
        fasce_orarie = [f"{h:02d}:00/{h:02d}:59" for h in range(9, 21)]
        for data in date_rng:
            for fascia in fasce_orarie:
                ora_inizio = int(fascia.split(':')[0])
                giorno_settimana = data.dayofweek
                base_chiamate = 50
                pattern_orario = max(0, np.sin((ora_inizio - 9) * np.pi / 11) * 60)
                pattern_settimanale = [1.3, 1.1, 1.0, 1.05, 0.9, 0.4, 0.3]
                chiamate = (base_chiamate + pattern_orario) * pattern_settimanale[giorno_settimana]
                chiamate += np.random.randn() * 15
                if 12 <= ora_inizio <= 13: chiamate *= 0.6 # Pausa pranzo
                df_list.append({'Data': data, 'Fascia_Oraria': fascia, 'NumeroChiamate': max(0, int(chiamate))})
        return pd.DataFrame(df_list)

    df_chiamate = crea_dati_chiamate()
    st.dataframe(df_chiamate.head(), use_container_width=True)

    st.write("#### Passo 2: Feature Engineering")
    st.write("**Questo è il passo più importante**. I modelli di ML capiscono solo i numeri. Dobbiamo trasformare le date e le fasce orarie in *features numeriche* che il modello possa usare per imparare.")
    code_feature_eng = '''
df_chiamate['OraInizio'] = df_chiamate['Fascia_Oraria'].apply(lambda x: int(x.split(':')[0]))
df_chiamate['GiornoDellaSettimana'] = df_chiamate['Data'].dt.dayofweek # 0=Lunedì, 1=Martedì...
df_chiamate['GiornoDelMese'] = df_chiamate['Data'].dt.day
df_chiamate['Mese'] = df_chiamate['Data'].dt.month

st.write("DataFrame con le nuove features numeriche:")
st.dataframe(df_chiamate[['Data', 'OraInizio', 'GiornoDellaSettimana', 'NumeroChiamate']].head(), use_container_width=True)
    '''
    st.code(code_feature_eng, language='python')
    df_chiamate['OraInizio'] = df_chiamate['Fascia_Oraria'].apply(lambda x: int(x.split(':')[0]))
    df_chiamate['GiornoDellaSettimana'] = df_chiamate['Data'].dt.dayofweek
    df_chiamate['GiornoDelMese'] = df_chiamate['Data'].dt.day
    df_chiamate['Mese'] = df_chiamate['Data'].dt.month
    st.write("DataFrame con le nuove features numeriche:")
    st.dataframe(df_chiamate[['Data', 'OraInizio', 'GiornoDellaSettimana', 'NumeroChiamate']].head(), use_container_width=True)

    st.write("#### Passo 3: Addestrare il Modello")
    code_train_rf = '''
# Selezioniamo solo i giorni lavorativi per l'addestramento
df_lavorativi = df_chiamate[df_chiamate['GiornoDellaSettimana'] < 5]

# Definiamo le features (X) e il target (y)
features = ['OraInizio', 'GiornoDellaSettimana', 'GiornoDelMese', 'Mese']
target = 'NumeroChiamate'

X = df_lavorativi[features]
y = df_lavorativi[target]

# Suddividiamo i dati per training e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creiamo e addestriamo il modello Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_split=5)
rf_model.fit(X_train, y_train)

# Valutiamo il modello sul test set
y_pred = rf_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
st.metric("Errore Medio Assoluto (MAE) sul Test Set", f"{mae:.2f} chiamate")
st.caption("Il MAE ci dice che, in media, le previsioni del modello si discostano dal valore reale di circa tot chiamate.")
    '''
    st.code(code_train_rf, language='python')
    df_lavorativi = df_chiamate[df_chiamate['GiornoDellaSettimana'] < 5]
    features = ['OraInizio', 'GiornoDellaSettimana', 'GiornoDelMese', 'Mese']
    target = 'NumeroChiamate'
    X = df_lavorativi[features]
    y = df_lavorativi[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_split=5)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    st.metric("Errore Medio Assoluto (MAE) sul Test Set", f"{mae:.2f} chiamate")
    st.caption(f"Il MAE ci dice che, in media, le previsioni del modello si discostano dal valore reale di circa {mae:.0f} chiamate.")

    st.write("#### Passo 4: Creare e Visualizzare le Previsioni Future")
    st.write("Ora creiamo un DataFrame per la prossima settimana e usiamo il modello per prevedere il numero di chiamate.")
    code_predict = '''
# Troviamo la data del prossimo lunedì
today = pd.Timestamp.now()
next_monday = today + pd.Timedelta(days=(7 - today.dayofweek))

# Creiamo le date per la prossima settimana lavorativa
date_future_rng = pd.date_range(start=next_monday, periods=5, freq='D')
fasce_orarie = [f"{h:02d}:00/{h:02d}:59" for h in range(9, 21)]

# Creiamo il DataFrame futuro da popolare con le previsioni
df_future = pd.DataFrame([(d, f) for d in date_future_rng for f in fasce_orarie], columns=['Data', 'Fascia_Oraria'])

# Creiamo le stesse features che abbiamo usato per l'addestramento
df_future['OraInizio'] = df_future['Fascia_Oraria'].apply(lambda x: int(x.split(':')[0]))
df_future['GiornoDellaSettimana'] = df_future['Data'].dt.dayofweek
df_future['GiornoDelMese'] = df_future['Data'].dt.day
df_future['Mese'] = df_future['Data'].dt.month

# Facciamo le previsioni
df_future['PrevisioneChiamate'] = rf_model.predict(df_future[features])
df_future['Giorno'] = df_future['Data'].dt.strftime('%A') # Nome del giorno per il grafico

# Visualizziamo i risultati con un grafico
fig = px.line(
    df_future, 
    x='OraInizio', 
    y='PrevisioneChiamate', 
    color='Giorno',
    title='Previsione Volume Chiamate per la Prossima Settimana',
    labels={'OraInizio': 'Ora del Giorno', 'PrevisioneChiamate': 'Numero di Chiamate Previste'},
    markers=True
)
st.plotly_chart(fig, use_container_width=True)
    '''
    st.code(code_predict, language='python')
    today = pd.Timestamp.now()
    next_monday = today + pd.Timedelta(days=(7 - today.dayofweek))
    date_future_rng = pd.date_range(start=next_monday, periods=5, freq='D')
    fasce_orarie = [f"{h:02d}:00/{h:02d}:59" for h in range(9, 21)]
    df_future = pd.DataFrame([(d, f) for d in date_future_rng for f in fasce_orarie], columns=['Data', 'Fascia_Oraria'])
    df_future['OraInizio'] = df_future['Fascia_Oraria'].apply(lambda x: int(x.split(':')[0]))
    df_future['GiornoDellaSettimana'] = df_future['Data'].dt.dayofweek
    df_future['GiornoDelMese'] = df_future['Data'].dt.day
    df_future['Mese'] = df_future['Data'].dt.month
    df_future['PrevisioneChiamate'] = rf_model.predict(df_future[features])
    df_future['Giorno'] = df_future['Data'].dt.day_name()
    fig = px.line(
        df_future, x='OraInizio', y='PrevisioneChiamate', color='Giorno',
        title='Previsione Volume Chiamate per la Prossima Settimana',
        labels={'OraInizio': 'Ora del Giorno', 'PrevisioneChiamate': 'Numero di Chiamate Previste'},
        markers=True,
        category_orders={"Giorno": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
    )
    st.plotly_chart(fig, use_container_width=True)
