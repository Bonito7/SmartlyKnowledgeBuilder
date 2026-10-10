import re


class AIMetadata:

    def clean_text(self, text):
        """Nettoie un texte et normalise les espaces."""

        if text is None:
            return ""

        text = str(text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def clean_title(self, title):
        """Nettoie le titre / motif."""

        title = self.clean_text(title)

        title = title.replace("_", " ")

        return title

    # =========================================================
    # BASE YELEN
    # =========================================================

    def generate_intention(self, title):
        """
        Génère une intention générique pour les contenus Yelen.
        """

        title = self.clean_title(title)

        return (
            f"L'utilisateur recherche des informations "
            f"concernant : {title.lower()}."
        )

    def generate_question(self, title):
        """
        Génère une question utilisateur probable
        pour les contenus Yelen.
        """

        title = self.clean_title(title)

        title_lower = title.lower()

        if any(word in title_lower for word in [
            "comment",
            "procédure",
            "activer",
            "configurer",
            "installer"
        ]):
            return f"{title} ?"

        return f"Comment obtenir des informations sur {title} ?"

    # =========================================================
    # BASE MODOP
    # =========================================================

    def generate_modop_intention(
        self,
        motif,
        pourquoi="",
        que_faire=""
    ):
        """
        Génère une intention de recherche à partir
        du motif et du contenu réel du MODOP.
        """

        motif = self.clean_text(motif)
        pourquoi = self.clean_text(pourquoi)
        que_faire = self.clean_text(que_faire)

        if pourquoi:
            return (
                f"Le client souhaite obtenir une assistance "
                f"concernant « {motif} ». "
                f"Il cherche notamment à comprendre ou résoudre "
                f"la situation décrite : {pourquoi}"
            )

        return (
            f"Le client souhaite obtenir une assistance "
            f"concernant « {motif} »."
        )

    def generate_modop_questions(
        self,
        motif,
        pourquoi="",
        que_faire=""
    ):
        """
        Génère plusieurs formulations naturelles
        qu'un utilisateur pourrait utiliser pour rechercher
        ce mode opératoire.
        """

        motif = self.clean_title(motif)
        pourquoi = self.clean_text(pourquoi)

        questions = []

        # Question principale
        questions.append(
            f"Que faire concernant {motif} ?"
        )

        # Formulation avec "client"
        questions.append(
            f"Un client rencontre le problème suivant : {motif}. "
            f"Quelle est la procédure ?"
        )

        # Formulation assistance
        questions.append(
            f"Comment prendre en charge un client pour {motif} ?"
        )

        # Formulation avec pourquoi
        if pourquoi:
            questions.append(
                f"Pourquoi le client rencontre-t-il cette situation "
                f"({motif}) ?"
            )

        # Formulation naturelle
        questions.append(
            f"Comment résoudre le cas « {motif} » ?"
        )

        return questions

    def generate_modop_metadata(
        self,
        motif,
        pourquoi="",
        que_faire=""
    ):
        """
        Retourne toutes les métadonnées IA d'un élément MODOP.
        """

        return {
            "intention": self.generate_modop_intention(
                motif,
                pourquoi,
                que_faire
            ),

            "questions": self.generate_modop_questions(
                motif,
                pourquoi,
                que_faire
            )
        }