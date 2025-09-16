import pandas as pd
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader


def create_html_df(df: pd.DataFrame, firma: str, template_name: str) -> str:
    """
    Genera una stringa HTML da un DataFrame Pandas usando un template Jinja2.

    Args:
        df (pd.DataFrame): Il DataFrame da convertire in tabella HTML.
        firma (str): Una stringa per la firma da inserire nel report.
        template_name (str): Il nome del file del template (es. 'template.html').

    Returns:
        str: La stringa HTML completa generata dal template.
    """
    # Imposta l'ambiente di Jinja2 per caricare i file dalla stessa cartella dello script
    env = Environment(loader=FileSystemLoader('.'))
    
    # Carica il template specificato
    template = env.get_template(template_name)

    # Estrae gli header dal DataFrame
    header_row = df.columns.to_list()

    # Esegue il "rendering" del template, passando le variabili
    html_output = template.render(
        df=df,
        header_row=header_row,
        firma=firma
    )

    return html_output