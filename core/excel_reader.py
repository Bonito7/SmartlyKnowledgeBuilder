import pandas as pd
import os
import glob


class ExcelReader:

    def __init__(self, folder_path="data/input"):
        self.folder_path = folder_path
        self.file_path = None
        self.data = None


    def find_excel_file(self):
        """
        Recherche automatiquement un fichier Excel dans le dossier input
        """

        files = glob.glob(
            os.path.join(self.folder_path, "*.xlsx")
        )

        if not files:
            raise FileNotFoundError(
                "Aucun fichier Excel trouvé dans le dossier data/input"
            )

        # Prend le premier fichier trouvé
        self.file_path = files[0]

        print(f"📄 Fichier détecté : {self.file_path}")

        return self.file_path


    def load(self):
        """
        Charge automatiquement le fichier Excel trouvé
        """

        self.find_excel_file()

        print("📂 Chargement du fichier Excel...")

        self.data = pd.read_excel(
            self.file_path,
            engine="openpyxl"
        )

        print("✅ Fichier chargé avec succès")
        print(f"📊 Nombre de contenus : {len(self.data)}")

        return self.data


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