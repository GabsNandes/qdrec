"""
import pytesseract
from pdf2image import convert_from_path

print("lendo pdf")
imagem = convert_from_path("nosso.pdf")

print("usando pytesseract")
texto = pytesseract.image_to_string(imagem[0], lang="por")

with open("out.ascii", "wb") as file:
    print("Escrevendo arquivo")
    file.write(texto.encode(encoding="ascii", errors="xmlcharrefreplace"))


print("fim")
"""

# Get path of current script
import os

import pypdf

script_path = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(script_path, "nosso.pdf")

with open(file_path, "rb") as file:
    pdf = pypdf.PdfReader(file)

    for page in pdf.pages:
        print(page.extract_text())
        print("----")

print("fim")
