import pdfplumber
import re,os

def read_pdf(file):
    with pdfplumber.open(file) as f:
        text = ""
        for page_num in range(len(f.pages)):
            page = f.pages[page_num]
            t =  str(page.extract_text())
            text = text + t.replace('"', "'")
            # Filtrer les caractères non imprimables
        #text = re.sub(r'[^\w\s\-\nàâ\u2013äéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ.,;:!?+#/•"\'()]', '', text)
            #text = re.sub(r'[^a-zA-ZÀ-ÖÙ-öù-ÿ\s]', '', text)
    return text


# import fitz  # PyMuPDF

# def read_pdf(file):
#     text = ""
#     current_directory = os.getcwd()
#     file = os.path.join(current_directory, file.name)
#     with fitz.open(file) as pdf_document:
#         print("tel")
#         num_pages = pdf_document.page_count
 
#         for page_num in range(num_pages):
#             page = pdf_document[page_num]
#             text += page.get_text()
 
#     return text
# print(read_pdf("HASSAN_KIBOU_CV_JANVIER_24.pdf"))