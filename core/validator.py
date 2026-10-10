import pandas as pd


class DataValidator:

    def __init__(self, dataframe):
        self.df = dataframe

    def report(self):

        print("\n========== RAPPORT ==========\n")

        print(f"Nombre de lignes : {len(self.df)}")

        print(f"Nombre de colonnes : {len(self.df.columns)}")

        print("\nColonnes :")

        for col in self.df.columns:
            print(f" - {col}")

        print("\nValeurs manquantes :")

        print(self.df.isnull().sum())

        print("\nDoublons :")

        print(self.df.duplicated().sum())