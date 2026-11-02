import pandas as pd


def repair_text(value):
    """
    Répare l'encodage cassé rencontré dans les exports Excel.

    Certains champs ont été encodés en UTF-8 puis relus en latin-1,
    ce qui produit des caractères corrompus :
        "PubliÃ©"  -> "Publié"
        "n\\x9cuds" -> "nœuds"
    """

    if not isinstance(value, str):
        return value

    if not value:
        return value

    # UTF-8 lu en latin-1
    try:
        return value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # Cas restants : octets latin-1 valides en CP1252 (ex: 0x9C = "œ")
    try:
        return value.encode("latin-1").decode("cp1252")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value


def is_blank(value):
    """Vrai si la valeur est nulle, vide ou uniquement des espaces."""

    if value is None:
        return True

    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass

    return str(value).strip() == ""


def format_date(value):
    """Formate une date Excel en texte lisible, gère le vide."""

    if is_blank(value):
        return ""

    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return str(value)


def format_id(value):
    """Formate un identifiant flottant (12543.0 -> '12543')."""

    if is_blank(value):
        return ""

    try:
        number = float(value)

        if number.is_integer():
            return str(int(number))

    except (TypeError, ValueError):
        pass

    return str(value)
