import pandas as pd


class ContentBuilder:

    def build(self, dataframe):

        contents = []

        grouped = dataframe.groupby("id_contenu")

        print(f"🔄 Regroupement des contenus : {len(grouped)}")


        for content_id, group in grouped:

            row = group.iloc[0]

            contenu = {
                "id": content_id,
                "type": row["type_contenu"],
                "title": row["title"],
                "date_creation": row["date_creation"],
                "date_modification": row["date_modification"],
                "source": row["source"],
                "body_html": row["body_html"],
                "attachments": []
            }


            for _, item in group.iterrows():

                if pd.notna(item["filename"]):

                    contenu["attachments"].append({
                        "name": item["filename"],
                        "url": item["file_url"]
                    })


            contents.append(contenu)


        print(f"✅ Contenus uniques : {len(contents)}")

        return contents