import openai
import streamlit as st
import traceback
import os
from src.extract_pdf import all_extraction, extract_field
from src.pdf_reader import read_pdf
from src.script import generate_docx
import docx
from src.constants import JOB_ONE_LEVEL, JOB_TWO_LEVEL, JOB, LEVEL_MAPPING
st.image("assests/logo.jpg", width=300)
st.title("Générateur de CV ")


# def upload_cv():
#     uploaded_file = st.file_uploader(
#         "Choisir un fichier", type=["pdf"]
#     )

#     curr = os.getcwd()
#     nom_repertoire = os.path.join(curr, "uploaded")
#     os.makedirs(nom_repertoire, exist_ok=True)
#     if uploaded_file is not None:
#         file_extension = uploaded_file.name.split(".")[-1]
#         if file_extension == "pdf":
#             text = read_pdf(uploaded_file)
#         output_txt = uploaded_file.name.replace(".pdf", ".txt")
#         output_path = os.path.join(nom_repertoire, output_txt)
#         with open(output_path, "w", encoding="utf-8") as output_file:
#             output_file.write(text)
#         st.success("CV uploadé correctement")
#         return curr, output_txt
#     return None, None


# def type_cv():
#     """Choisir le type de poste et le niveau associé

#     Returns:
#         str: type de poste et le niveau associé
#     """

#     type_job = st.radio("Sélectionnez le type de CV", JOB, horizontal = True)
#     cv_type = level(type_job)
#     return cv_type

# def level(type_job):
#     """Choisir le niveau d'ancienneté du poste

#     Args:
#         type_job (_type_): _description_
#         options (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     level_chosen = "Senior"
#     if type_job in JOB_TWO_LEVEL:
#         options_level = [type_job + " Junior", type_job + " Senior"]
#         level_chosen = st.radio("Sélectionnez le niveau ", options_level)
#         cv_type = LEVEL_MAPPING[level_chosen]
#     if type_job in JOB_ONE_LEVEL:
#         cv_type = LEVEL_MAPPING[type_job]
#     return cv_type

# curr, file_name = upload_cv()
# if curr:
#     cv_type = type_cv()
#     conversion = st.button("Convertir le CV")
#     if conversion:
#             nom_repertoire = os.path.join(curr, "uploaded")
#             try:
#                 with st.spinner(
#                     "Veuillez patienter pendant l'extraction des informations du CV"
#                 ):
#                     json_path = all_extraction(nom_repertoire, file_name, cv_type)
#             except openai.RateLimitError:
#                 traceback.print_exc()
#                 st.error("Limite d'utilisation de l'API atteinte, Le générateur n'a pas pu générer de CV, Veuillez contacter le staff technique !")   
#                 st.stop()
#             try:
#                 docx_name = generate_docx(json_path, cv_type)
#                 repertoire_output = os.path.join(curr, "output")
#                 docx_data = docx.Document(os.path.join(repertoire_output, docx_name))
#                 with open(os.path.join(repertoire_output, docx_name), 'rb') as f:
#                     st.download_button('Télécharger le CV au format NewCo Partners', f, file_name=docx_name)
#             except Exception:
#                 traceback.print_exc()
#                 st.error("Le générateur n'a pas pu générer de CV, Veuillez réessayer ou contacter le staff technique !")

         
       
