import os
import re

import pypdf

script_path = os.path.dirname(os.path.realpath(__file__))

# file_path = os.path.join(script_path, "nosso.pdf")

file_path = os.path.join("samples", "DiarioOficial_NovaIguaçu_0518-24.pdf")


all_text = ""

with open(file_path, "rb") as file:
    pdf = pypdf.PdfReader(file)

    for page_number, page in enumerate(pdf.pages):
        extracted_text = page.extract_text()
        print(page_number, len(extracted_text))
        print("----")

        processed_text = extracted_text.lower()

        # Find position of the word 'nomear' in the text
        # index = processed_text.find("nomear")

        designations = [m.start() for m in re.finditer("nomear", processed_text)]

        for start_index in designations:
            # Find text from the word 'nomear' to the next full stop
            end_index = extracted_text.find(".", start_index)
            designation_act = extracted_text[start_index : end_index + 1]
            print(designation_act)

        dismissals = [m.start() for m in re.finditer("exonerar", processed_text)]

        for start_index in dismissals:
            # Find text from the word 'exonerar' to the next full stop
            end_index = extracted_text.find(".", start_index)
            designation_act = extracted_text[start_index : end_index + 1]
            print(designation_act)

        all_text = all_text + extracted_text


with open("all_text.txt", "w", encoding="utf-8") as file:
    file.write(all_text)


print("fim")
