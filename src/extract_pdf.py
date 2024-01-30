# # from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# # from pdfminer.converter import TextConverter
# # from pdfminer.layout import LAParams
# # from pdfminer.pdfpage import PDFPage
# # from io import StringIO

# # def extract_text_from_pdf(pdf_path):
# #     resource_manager = PDFResourceManager()
# #     return_string = StringIO()
# #     codec = 'utf-8'
# #     laparams = LAParams()
# #     device = TextConverter(resource_manager, return_string, codec=codec, laparams=laparams)
# #     interpreter = PDFPageInterpreter(resource_manager, device)

# #     with open(pdf_path, 'rb') as file:
# #         for page in PDFPage.get_pages(file, check_extractable=True):
# #             interpreter.process_page(page)

# #         text = return_string.getvalue()

# #     device.close()
# #     return_string.close()

# #     return text

# # pdf_path = r'C:\Users\TABARANIYassine(NewC\Documents\code\cv-generator\Cv data\CV 10.pdf'
# # extracted_text = extract_text_from_pdf(pdf_path)
# # print(extracted_text)


from time import sleep
from tqdm import tqdm
import os
from openai import OpenAI
import json
import ast

# clé API Murielle
# key = "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"
# clé API Yassine
# key = "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"
# clé API Kamel
key = "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"

client = OpenAI(api_key=key)

prompt_profil = """Extrait le nom du candidat en l'écrivant toutes ses lettres en majuscule et le prénom du candidat en écrivant uniquement la première lettre du prénom en majuscule et les autres lettres
                    en minuscule. N'écrit pas de phrase au début ou à la fin, je veux que ta sortie soit strictement dans ce format. Toutes les clés doivent être présentes dans le json. 
                    {
                        "Profil": {
                            "nom": "",
                            "prenom": ""
                        }
                    }"""
prompt_formations = """Extrait les formations académiques, diplomes du cv suivant, ne prends pas en compte les certifications
                        et met le sous le format json suivant, N'écrit pas de phrase de présentation au début, ni à la fin je veux que ta sortie soit strictement dans ce format. Toutes les clés doivent être présentes dans le json.
                        {
                            "Formations" : [
                                {"titre":"", 
                                "date":"", 
                                "établissement":"", 
                                "description":""
                                }
                            ]
                        }"""
prompt_expériences = """Extrait les expériences professionnelles du cv en récupérant toutes les infomations des expériences les missions, les tâches réalisées, le contexte , les réalisations.
                        Prend tout le texte inclus entre le titre de l'experience et un autre titre d'une autre expérience et met le dans la valeur de la clé description, pour les environnements tu dois les relever de la description s'il ne sont pas présent,
                        sinon récupère les, et met le sous format json suivant. N'écrit pas de phrase de présentation au début, ni à la fin je veux que ta sortie soit strictement dans ce format. Toutes les clés doivent être présentes dans le json.
                        "{
                            Expériences professionnelles":[
                                {
                                    "nom de l'entreprise": "", 
                                    "nom du poste occupé": "", 
                                    "date": "", 
                                    "description":"", 
                                    "environnement technique": ""
                                }
                            ]
                        }
                        """

prompt_projet = """Extrait les projets académiques du cv suivant et me le sous le format json suivant. Dans la clé description, je veux que
que tu extrait toute le texte entre le début d'une expérience jusqu'à la fin de cette dernière. N'écrit pas de phrase de présentation au début, 
ni à la fin je veux que ta sortie soit strictement dans ce format. Toutes les clés doivent être présentes dans le json.
    {
    "Projets" : 
        [
            {
                "titre": "", 
                "date":"", 
                "description":""
            }
        ]
    }
"""
prompt_competences = """

Extrait les compétences techniques et fonctionnelles, complète avec les compétences dans les environnements techniques des expériences professionnelles du cv suivant
met le sous le format json suivant. N'écrit pas de phrase de présentation au début, ni à la fin je veux que ta sortie soit strictement dans ce format. Toutes les clés doivent être présentes dans le json.
"{
    Compétences techniques" :  {
        "Langages de programmation": "", 
        "Framework": "", 
        "Base de données": "", 
        "Logiciels": "", 
        "Librairie": "",
        "Bibliothèque": "", 
        "Système d'exploitation": "",
        "Serveur d'application": "", 
        "Outils dataviz": "", 
        "Méthodologie": "", 
        "API Design": "", 
        "Cloud Computing": "", 
        "Devops": "", 
        "Autres outils": "",
        "Conduite de projet": "",
    },
    "Compétences fonctionnelles": { 
        "Processus métiers bancaires": "",
        "Interlocuteurs privilégiés": "",
        "Périmètre fonctionnel": ""
    }
}
"""

prompt_certif_langues = """   Extrait les certifications du cv (pas les formations) et met le sous le format json suivant,N'écrit pas de phrase de présentation au début, ni à la fin je veux que ta sortie soit strictement dans ce format 
Ne prends pas plus de 3 certifications et prends les plus pertinentes. N'écrit pas de phrase ni au début ni à la fin, je veux que ta sortie soit strictement à ce format. Toutes les clés doivent être présentes dans le json.
{
    "Certifications" : [
        {
            "nom": "", 
            "date": ""
        }
    ],
    "Langues" : [
        {   
            "nom": "", 
            "niveau": ""
        }
    ]
}
"""

prompt_domaine_intervention = """
Extrait les domaines d'interventions du cv et met le sous le format json suivant. N'écrit pas de phrase de présentation ni au début, ni à la fin je veux que ta sortie soit strictement dans ce format. Toutes les clés doivent être présentes dans le json.
    "Domaines d'intervention": 
    {
        "Outils de planning - Méthodologies Projet" : "" 
    }
}"""

prompt_caption = """
    Veuillez me faire juste en 3 phrases et pas plus une caption en langue française  qui contient les données de cv d'un candidat, commence la caption par le nom de candidat suivi par le verbe etre au présent comme: Alex est un/une en se basant sur le contenu de cv suivant:
    et retourne moi un json. N'écrit pas de phrase ni au début ni à la fin, je veux que ta sortie soit strictement à ce format.
    {
        "caption": ""
    }
"""

def extract_field(nom_repertoire: str, file_name: str, prompt: str):
    """
    Extraire un champ spécifique (Expériences professionnelles, Formations, Compétences, Projets, Langues) du texte extrait d'un CV

    Args:
        nom_repertoire (str): Répertoire Courant
        file_name (str): Nom du fichier CV
        prompt (str): _description_

    Returns:
        str: Information d'un champ spécifique
    """
    cv = ""
    with open(os.path.join(nom_repertoire, file_name), "r", encoding="utf-8") as f:
        cv += f.read()
    fprompt = prompt + cv
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.1,
        messages=[{"role" : "system", "content": """Tu es une api de formattage en json et un expert en RH qui peut extraire les informations de n'importe quel CV. Quand je vais te demander d'extraire des informations, 
                   je veux que tu respectes le formatage json, les indentations et l'encodage utf-8. En sortie, je dois avoir un json string valide sans json decode error et renvoie uniquement les résultats sous la forme json, n'ajoute pas ```json au début ni à la fin
                   """},
                   {"role": "user", "content": fprompt}],
    )
    extracted_information = chat_completion.choices[0].message.content
    return extracted_information


def json_format(extracted_information):
    data = json.loads(extracted_information, strict=False)
    return data

def correct_json_format(error, json_output):
    """_summary_

    Args:
        error (_type_): _description_
        json_output (_type_): _description_

    Returns:
        _type_: _description_
    """
    msg = f"""Tu es une API de correction de format json , j'essaie de charger mes données json en Python json.loads(json_txt) I receive this error message: {error.msg}.
        \nMet le moi sous un format json valide JSON \n\nJSON:{json_output}"""
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.1,
        messages=[{"role": "user", "content": msg}],
    )
    print("-----correction----")
    return json_format(chat_completion.choices[0].message.content)
  
def merge_dictionnaries(dictionnary):
    fusion = {}
    for dictionnaire in dictionnary:
        fusion.update(dictionnaire)
    return fusion

def all_extraction(nom_rep: str, cv_name: str, cv_type):
    """Assemblage des différentes informations extraites du CV et mise sous la forme json

    Args:
        nom_rep (str): Nom du répertoire courant
        cv_name (str): Nom du fichier

    Returns:
        str: Chemin du fichier json créé
    """
    # Extraction des différents champs
    merged_data = list()

    profil = extract_field(nom_rep, cv_name, prompt_profil)
    print(profil)
    data_profil = json_format(profil)
    merged_data.append(data_profil)

    formations = extract_field(nom_rep, cv_name, prompt_formations)
    print(formations)
    data_formations = json_format(formations)
    merged_data.append(data_formations)

    experiences = extract_field(nom_rep, cv_name, prompt_expériences)
    print(experiences)
    sleep(10)
    data_experiences = json_format(experiences)
    merged_data.append(data_experiences)

    competences = extract_field(nom_rep, cv_name, prompt_competences)
    print(competences)
    sleep(20)
    data_competences = json_format(competences)
    merged_data.append(data_competences)

    certif_langues = extract_field(nom_rep, cv_name, prompt_certif_langues)
    print(certif_langues)
    data_certif_langues = json_format(certif_langues)
    merged_data.append(data_certif_langues)

    caption = extract_field(nom_rep, cv_name, prompt_caption)
    print(caption)
    data_caption = json_format(caption)
    merged_data.append(data_caption)

    if cv_type == "-dev-junior" or cv_type == "-data-junior":
        projets = extract_field(nom_rep, cv_name, prompt_projet)
        print(projets)
        sleep(20)
        data_projets = json_format(projets)
        merged_data.append(data_projets)
    
    if cv_type == "-moa":
        domaines_intervention = extract_field(nom_rep, cv_name, prompt_domaine_intervention)
        print(domaines_intervention)
        data_domaine_intervention = json_format(domaines_intervention)
        merged_data.append(data_domaine_intervention)
    


    merged_dictionnaries = merge_dictionnaries(merged_data)
    output_json = cv_name.replace(".txt", ".json")
    with open(os.path.join(nom_rep, output_json), "w", encoding="utf-8") as file:
        json.dump(merged_dictionnaries, file, ensure_ascii=False)
    return os.path.join(nom_rep, output_json)

