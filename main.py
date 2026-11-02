import json
import os

from core.excel_reader import ExcelReader
from core.ai_metadata import AIMetadata
from core.word_generator import WordGenerator
from core.modop_reader import ModopReader


# =========================================================
# CONFIGURATION
# =========================================================

CONFIG_FILE = "config.json"

INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"


def load_config():
    """
    Charge config.json et met à jour les dossiers
    d'entrée / de sortie.
    """

    global INPUT_DIR, OUTPUT_DIR

    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️  {CONFIG_FILE} introuvable, "
              f"utilisation des dossiers par défaut.")
        return {}

    try:

        with open(
            CONFIG_FILE,
            encoding="utf-8"
        ) as file:
            config = json.load(file)

    except json.JSONDecodeError as error:

        print(f"⚠️  {CONFIG_FILE} invalide ({error}), "
              f"utilisation des dossiers par défaut.")
        return {}

    INPUT_DIR = config.get("input_folder", INPUT_DIR)
    OUTPUT_DIR = config.get("output_folder", OUTPUT_DIR)

    return config


# =========================================================
# RECHERCHE DES FICHIERS
# =========================================================

def find_excel_files():

    if not os.path.exists(INPUT_DIR):
        raise FileNotFoundError(
            f"Le dossier {INPUT_DIR} n'existe pas."
        )

    files = [
        file
        for file in os.listdir(INPUT_DIR)
        if file.lower().endswith((".xlsx", ".xls"))
    ]

    return files


def find_yelen_file(files):

    """
    Identifie le fichier Yelen.
    On privilégie les fichiers contenant 'export'
    ou 'yelen' dans leur nom.
    """

    candidates = [
        file for file in files
        if "export" in file.lower()
        or "yelen" in file.lower()
    ]

    if not candidates:
        raise FileNotFoundError(
            "Aucun fichier Excel Yelen détecté."
        )

    return candidates[0]


def find_modop_file(files):

    """
    Identifie le fichier MODOP.
    """

    candidates = [
        file for file in files
        if "modop" in file.lower()
        or "mode" in file.lower()
        or "prise" in file.lower()
    ]

    if not candidates:
        raise FileNotFoundError(
            "Aucun fichier Excel MODOP détecté."
        )

    return candidates[0]


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("=" * 70)
    print("       SMARTLY KNOWLEDGE BUILDER")
    print("=" * 70)
    print()

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    load_config()

    print(f"Dossier d'entrée  : {INPUT_DIR}")
    print(f"Dossier de sortie : {OUTPUT_DIR}")
    print()

    # -----------------------------------------------------
    # Préparation
    # -----------------------------------------------------

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = find_excel_files()

    print("Fichiers Excel détectés :")
    for file in files:
        print(f"  - {file}")

    print()

    # -----------------------------------------------------
    # Identification des bases
    # -----------------------------------------------------

    yelen_filename = find_yelen_file(files)
    modop_filename = find_modop_file(files)

    yelen_path = os.path.join(
        INPUT_DIR,
        yelen_filename
    )

    modop_path = os.path.join(
        INPUT_DIR,
        modop_filename
    )

    print("BASE YELEN")
    print(f"  {yelen_filename}")

    print()

    print("BASE MODOP")
    print(f"  {modop_filename}")

    print()

    # -----------------------------------------------------
    # Initialisation
    # -----------------------------------------------------

    ai = AIMetadata()

    generator = WordGenerator(
        output_dir=OUTPUT_DIR
    )

    # =====================================================
    # 1. TRAITEMENT YELEN
    # =====================================================

    print("=" * 70)
    print("TRAITEMENT DE LA BASE YELEN")
    print("=" * 70)
    print()

    try:

        reader = ExcelReader(yelen_path)

        df_yelen = reader.read()

        print(
            f"✓ {len(df_yelen)} lignes Yelen chargées."
        )

        print()

        # -------------------------------------------------
        # Types de contenu
        # -------------------------------------------------

        if "type_contenu" not in df_yelen.columns:

            raise ValueError(
                "La colonne 'type_contenu' est absente "
                "de la base Yelen."
            )

        content_types = (
            df_yelen["type_contenu"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        # Exclusion des valeurs non textuelles
        # (identifiants numériques parasite dans l'export)
        content_types = [
            content_type
            for content_type in sorted(content_types)
            if content_type
            and not content_type.replace(".", "", 1).isdigit()
        ]

        print(
            f"✓ {len(content_types)} types de contenu détectés."
        )

        print()

        # -------------------------------------------------
        # Génération des documents Yelen
        # -------------------------------------------------

        yelen_count = 0

        for content_type in content_types:

            subset = df_yelen[
                df_yelen["type_contenu"]
                .astype(str)
                .str.strip()
                == content_type
            ].copy()

            if subset.empty:
                continue

            print(
                f"  → {content_type} : "
                f"{len(subset)} contenus"
            )

            # -------------------------------------------------
            # IMPORTANT :
            # Ici on utilise ton générateur Yelen existant.
            # -------------------------------------------------

            try:

                output_file = generator.generate_document(
                    subset,
                    content_type,
                    ai
                )

                print(
                    f"     ✓ {os.path.basename(output_file)}"
                )

                yelen_count += 1

            except AttributeError:

                print(
                    "     ⚠ La méthode "
                    "'generate_document' n'existe pas encore "
                    "dans word_generator.py."
                )

                print(
                    "     → Le traitement MODOP continuera."
                )

                break

        print()

        print(
            f"Documents Yelen générés : {yelen_count}"
        )

    except Exception as error:

        print()
        print(
            f"✗ Erreur pendant le traitement Yelen : "
            f"{error}"
        )

    # =====================================================
    # 2. TRAITEMENT MODOP
    # =====================================================

    print()
    print("=" * 70)
    print("TRAITEMENT DE LA BASE MODOP")
    print("=" * 70)
    print()

    try:

        modop_reader = ModopReader(
            modop_path
        )

        df_modop = modop_reader.read()

        print(
            f"✓ {len(df_modop)} motifs MODOP chargés."
        )

        print()

        # -------------------------------------------------
        # Génération du document MODOP
        # -------------------------------------------------

        modop_output = (
            generator.generate_modop_document(
                df_modop,
                ai
            )
        )

        print(
            "✓ Document MODOP généré :"
        )

        print(
            f"  {modop_output}"
        )

    except Exception as error:

        print()
        print(
            f"✗ Erreur pendant le traitement MODOP : "
            f"{error}"
        )

    # =====================================================
    # FIN
    # =====================================================

    print()
    print("=" * 70)
    print("TRAITEMENT TERMINÉ")
    print("=" * 70)
    print()

    print(
        f"Les fichiers sont disponibles dans : "
        f"{OUTPUT_DIR}"
    )

    print()


# =========================================================
# EXECUTION
# =========================================================

if __name__ == "__main__":
    main()