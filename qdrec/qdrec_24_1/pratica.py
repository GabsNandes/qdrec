import os
import re

import pypdf

script_path = os.path.dirname(os.path.realpath(__file__))

# file_path = os.path.join(script_path, "nosso.pdf")

file_path = os.path.join("samples", "DiarioOficial_NovaIguaçu_0518-24.pdf")


def find_act(word: str, full_text: str):
    act_indexes = [m.start() for m in re.finditer(word, full_text.lower())]

    for start_index in act_indexes:
        print("\n----")

        # Find text from the word to the next full stop
        end_index = extracted_text.find(".", start_index)
        act = extracted_text[start_index : end_index + 1]
        print("Full act text:")
        print(act)

        # Find the first ocurrence of an uppercase letter after the word, up to the next comma
        # This is the name of the person affected by the act
        rest = act[act.lower().find(word) + len(word) :].strip()

        name_start_index = re.search("[A-Z]", rest)
        if name_start_index is None:
            continue

        name_start_index = name_start_index.start()
        name_end_index = rest.find(",", name_start_index)
        name = rest[name_start_index:name_end_index]
        name = name.strip().replace("\n", "").replace(" -", "")
        print("\nAffected name:\n" + name)

        print("----\n")


all_text = ""

with open(file_path, "rb") as file:
    pdf = pypdf.PdfReader(file)

    for page_number, page in enumerate(pdf.pages):
        extracted_text = page.extract_text()
        print(f"Reading page {page_number+1}, length: {len(extracted_text)}")

        find_act("nomear", extracted_text)
        find_act("exonerar", extracted_text)

        all_text = all_text + extracted_text


with open("all_text.txt", "w", encoding="utf-8") as file:
    file.write(all_text)


print("Finished!")
