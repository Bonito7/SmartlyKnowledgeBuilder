import pandas as pd

from core.text_utils import repair_text


class ExcelReader:

    def __init__(self, file_path):
        """
        Lit un fichier Excel de la base Yelen.

        Le chemin pointe directement vers le fichier,
        par exemple : data/input/export_yelen_17092026.xlsx
        """

        self.file_path = file_path
        self.data = None


    def find_data_sheet(self):
        """
        Retourne le nom de la première feuille contenant
        réellement des données.

        Certains exports contiennent une première feuille vide
        (Feuil1) et les données dans la suivante (Feuil2).
        """

        sheets = pd.read_excel(
            self.file_path,
            sheet_name=None,
            engine="openpyxl"
        )

        for sheet_name, dataframe in sheets.items():

            if dataframe.empty:
                continue

            return sheet_name, dataframe

        raise ValueError(
            f"Aucune feuille de données dans {self.file_path}"
        )


    def read(self):
        """
        Charge le fichier Excel, détecte la feuille utile
        et répare l'encodage des colonnes texte.
        """

        sheet_name, dataframe = self.find_data_sheet()

        print(f"📄 Feuille détectée : {sheet_name}")

        # Nettoyage des noms de colonnes
        dataframe.columns = [
            str(column).strip()
            for column in dataframe.columns
        ]

        # Réparation de l'encodage des colonnes texte
        for column in dataframe.columns:

            if dataframe[column].dtype == object:
                dataframe[column] = dataframe[column].map(
                    repair_text
                )

        self.data = dataframe

        print(f"✅ {len(dataframe)} lignes chargées")

        return dataframe


    def preview(self, rows=5):

        if self.data is None:
            print("⚠️ Aucun fichier chargé")
            return

        print("\n===== APERÇU DES DONNÉES =====")
        print(self.data.head(rows))


    def columns(self):

        if self.data is None:
            return []

        return list(self.data.columns)
