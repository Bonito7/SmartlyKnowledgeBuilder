from bs4 import BeautifulSoup
import re


class HTMLCleaner:

    @staticmethod
    def clean(html):

        if html is None:
            return ""

        html = str(html)

        soup = BeautifulSoup(html, "lxml")

        # Supprime les éléments inutiles
        for tag in soup(["script", "style", "iframe"]):
            tag.decompose()

        # Convertit le HTML en texte
        text = soup.get_text(separator="\n")

        # Nettoyage des lignes vides
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        # Nettoyage des espaces
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()