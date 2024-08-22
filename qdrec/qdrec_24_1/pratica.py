import os
import re

import pypdf

INPUT_PATH = "samples"
EXTRACTION_PATH = "extracted"


def find_act(word: str, full_text: str):
    act_indexes = [m.start() for m in re.finditer(word, full_text.lower())]

    for start_index in act_indexes:
        print("\n----")

        # Find text from the word to the next full stop
        end_index = full_text.find(".", start_index)
        act = full_text[start_index : end_index + 1]
        act = act.replace("\n", " ").replace("  ", " ")
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

        # Remove any - surrounded by any number of spaces in each side
        # TODO: implement
        # re.sub("[\s-\s]")

        print("\nAffected name:\n" + name)

        print("----\n")


def remove_header(last_word: str, full_text: str):
    # Remove text from the start of full_text up to the first occurence of last_word

    # TODO: implement method
    return full_text


def find_acts_in_file(file_path: str):
    print(f"Reading document {file_path}")

    all_text = ""
    with open(file_path, "rb") as f:
        pdf = pypdf.PdfReader(f)

        city_name = os.path.basename(file_path).split(" - ")[0]
        print(city_name)

        for page_number, page in enumerate(pdf.pages):
            extracted_text = page.extract_text()
            print(f"Reading page {page_number+1}, length: {len(extracted_text)}")

            extracted_text = remove_header(city_name, extracted_text)

            find_act("nomear", extracted_text)
            find_act("exonerar", extracted_text)

            all_text = all_text + "\n\n" + extracted_text

    # Write extracted text to a .txt file with the same name as the document
    extract_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.txt"
    extract_path = os.path.join(EXTRACTION_PATH, extract_filename)
    with open(extract_path, "w", encoding="utf-8") as f:
        f.write(all_text)


def main():

    if not os.path.exists(EXTRACTION_PATH):
        os.mkdir(EXTRACTION_PATH)

    for file in os.listdir(INPUT_PATH):
        file_path = os.path.join(INPUT_PATH, file)
        find_acts_in_file(file_path)


if __name__ == "__main__":
    main()

print("Finished!")
