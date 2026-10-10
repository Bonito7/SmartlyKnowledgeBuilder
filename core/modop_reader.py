import pandas as pd
import os


class ModopReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        """
        Lit la feuille 'Modop Prise en charge'
        et retourne uniquement les lignes contenant
        un véritable motif de contact.
        """

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"Fichier MODOP introuvable : {self.file_path}"
            )

        # Lecture sans supposer que la première ligne est l'en-tête
        df = pd.read_excel(
            self.file_path,
            sheet_name="Modop Prise en charge",
            header=None
        )

        # Recherche automatique de la ligne contenant les colonnes
        header_row = None

        for index, row in df.iterrows():
            values = [
                str(value).strip().lower()
                for value in row.tolist()
                if pd.notna(value)
            ]

            if "motif" in values and "pourquoi?" in values:
                header_row = index
                break

        if header_row is None:
            raise ValueError(
                "Impossible de trouver les colonnes du MODOP."
            )

        # Relecture avec le bon header
        df = pd.read_excel(
            self.file_path,
            sheet_name="Modop Prise en charge",
            header=header_row
        )

        # Nettoyage des noms de colonnes
        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        # Renommage standard
        column_mapping = {
            "Motif": "motif",
            "Pourquoi?": "pourquoi",
            "Pourquoi ?": "pourquoi",
            "Que faire?": "que_faire",
            "Que faire ?": "que_faire",
            "Commentaire de codification": "codification",
            "Statut": "statut"
        }

        df = df.rename(columns=column_mapping)

        # Colonnes attendues
        expected_columns = [
            "motif",
            "pourquoi",
            "que_faire",
            "codification",
            "statut"
        ]

        for column in expected_columns:
            if column not in df.columns:
                df[column] = ""

        # Nettoyage des cellules
        for column in expected_columns:
            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

        # Suppression des lignes sans motif
        df = df[
            df["motif"].str.strip() != ""
        ]

        # Suppression des lignes contenant uniquement des espaces
        df = df.reset_index(drop=True)

        return df