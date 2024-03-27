import pandas as pd
from typing import List
import os
import glob
from pathlib import Path
import json
import matplotlib.pyplot as plt

col_date: str = "date_heure"
col_donnees: str = "consommation"
cols: List[str] = [col_date, col_donnees]
fic_export_data: str = "data/interim/data.csv"


def load_data():
    list_fic: list[str] = [Path(e) for e in glob.glob("data/raw/*json")]
    list_df: list[pd.DataFrame] = []
    for p in list_fic:
        # list_df.append(pd.read_json(p))
        with open(p, "r") as f:
            dict_data: dict = json.load(f)
            df: pd.DataFrame = pd.DataFrame.from_dict(dict_data.get("results"))
            list_df.append(df)

    df: pd.DataFrame = pd.concat(list_df, ignore_index=True)
    return df


def format_data(df: pd.DataFrame):
    # typage
    df[col_date] = pd.to_datetime(df[col_date])
    # ordre
    df = df.sort_values(col_date)
    # filtrage colonnes
    df = df[cols]
    # dédoublonnage
    df = df.drop_duplicates()
    return df


def export_data(df: pd.DataFrame):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv(fic_export_data, index=False)


def plot_weekly_consumption(df: pd.DataFrame):
    df['Semaine'] = df[col_date].dt.week
    consommation_par_semaine = df.groupby('Semaine')[col_donnees].sum()

    plt.figure(figsize=(10, 6))
    consommation_par_semaine.plot(kind='bar', color='blue')
    plt.title('Consommation par semaine')
    plt.xlabel('Semaine de l\'année')
    plt.ylabel('Consommation totale')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def main_process():
    df: pd.DataFrame = load_data()
    df = format_data(df)
    export_data(df)
    plot_weekly_consumption(df)


if __name__ == "__main__":

    # data_file: str = "data/raw/eco2mix-regional-tr.csv"
    main_process()
