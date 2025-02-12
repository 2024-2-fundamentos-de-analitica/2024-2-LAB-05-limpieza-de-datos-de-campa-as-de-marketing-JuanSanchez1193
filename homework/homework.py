"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel



"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortgage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaign_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - cons_price_idx
    - euribor_three_months



"""

import pandas as pd
import zipfile
from pathlib import Path

def clean_campaign_data():
    input_folder = Path("files/input/")
    output_folder = Path("files/output/")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    client_data = []
    campaign_data = []
    economics_data = []
    
    for zip_path in input_folder.glob("*.zip"):
        with zipfile.ZipFile(zip_path, 'r') as archive:
            for csv_name in archive.namelist():
                with archive.open(csv_name) as file:
                    df = pd.read_csv(file)
                    
                    client_df = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
                    client_df['job'] = client_df['job'].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
                    client_df['education'] = client_df['education'].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
                    client_df['credit_default'] = client_df['credit_default'].apply(lambda x: 1 if x == "yes" else 0)
                    client_df['mortgage'] = client_df['mortgage'].apply(lambda x: 1 if x == "yes" else 0)
                    client_data.append(client_df)
                    
                    campaign_df = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()
                    campaign_df['previous_outcome'] = campaign_df['previous_outcome'].apply(lambda x: 1 if x == "success" else 0)
                    campaign_df['campaign_outcome'] = campaign_df['campaign_outcome'].apply(lambda x: 1 if x == "yes" else 0)
                    campaign_df['last_contact_date'] = pd.to_datetime(campaign_df[['day', 'month']].assign(year=2022).astype(str).agg('-'.join, axis=1))
                    campaign_df.drop(columns=['day', 'month'], inplace=True)
                    campaign_data.append(campaign_df)
                    
                    economics_df = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
                    economics_data.append(economics_df)
    
    if client_data:
        pd.concat(client_data).to_csv(output_folder / "client.csv", index=False)
    if campaign_data:
        pd.concat(campaign_data).to_csv(output_folder / "campaign.csv", index=False)
    if economics_data:
        pd.concat(economics_data).to_csv(output_folder / "economics.csv", index=False)

if __name__ == "__main__":
    clean_campaign_data()

