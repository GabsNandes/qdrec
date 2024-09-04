import csv
import json
import os
import re
from dataclasses import dataclass

import pypdf

INPUT_PATH = "samples"
EXTRACTION_PATH = "extracted"


@dataclass
class Act:
    full_text: str
    name: str
    page: int = 0

    def to_dict(self):
        return {"full_text": self.full_text, "name": self.name, "page": self.page}


def find_acts_in_text(word: str, full_text: str, page_number: int) -> list[Act]:
    act_indexes = [m.start() for m in re.finditer(word, full_text.lower())]

    acts: list[Act] = []

    for start_index in act_indexes:
        print("\n----")

        # Find text from the word to the next full stop followed by a newline
        end_index = full_text.find(".\n", start_index)
        act = full_text[start_index : end_index + 1]
        act = act.replace("\n", " ").replace("  ", " ").strip()

        if not act:
            continue

        # Remove any - surrounded by at least one space in each side
        act = re.sub(r"\s+-\s+", "", act)

        print("Full act text:")
        print(act)

        # Find the first ocurrence of an uppercase letter after the word, up to
        # the next comma OR the next word that starts with a lowercase letter,
        # ignoring connecting words like "da", "de", "do", "das", "dos", "e".
        # This is the name of the person affected by the act!
        rest = act[act.lower().find(word) + len(word) :].strip()

        pattern = r"[A-Z\u00C0-\u00DC].*?(?=,|\s(?!(da|de|do|das|dos|e)(\s[A-Z\u00C0-\u00DC]))[a-z])"

        name = re.search(pattern, rest)
        if name:
            name = name.group(0)
            name = name.replace(",", "")
            name = name.strip()
        else:
            name = "?"

        print("\nAffected name:\n", name)

        print("----\n")

        acts.append(Act(act, name, page_number))

    return acts


def remove_header(last_word: str, full_text: str):
    # Remove text from the start of full_text up to the first occurence of last_word
    start_index = full_text.lower().find(last_word.lower()) + len(last_word)
    full_text = full_text[start_index:]

    return full_text


def find_acts_in_file(file_path: str, debug: bool = False) -> list[Act]:
    print(f"Reading document {file_path}")

    all_acts: list[Act] = []

    all_text = ""
    with open(file_path, "rb") as f:
        pdf = pypdf.PdfReader(f)

        city_name = os.path.basename(file_path).split(" - ")[0]

        pages_text = []

        for page_number, page in enumerate(pdf.pages):
            extracted_text = page.extract_text()
            print(f"Reading page {page_number+1}, length: {len(extracted_text)}")

            extracted_text = remove_header(city_name, extracted_text)

            pages_text.append(extracted_text)

            nomination_acts = find_acts_in_text(
                "nomear", extracted_text, page_number + 1
            )
            all_acts.extend(nomination_acts)

            dismissal_acts = find_acts_in_text(
                "exonerar", extracted_text, page_number + 1
            )
            all_acts.extend(dismissal_acts)

            all_text = all_text + "\n\n" + extracted_text

    # Write extracted text to a .txt file with the same name as the document
    if debug:
        extract_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.txt"
        extract_path = os.path.join(EXTRACTION_PATH, extract_filename)
        with open(extract_path, "w", encoding="utf-8") as f:
            f.write(all_text)

    return all_acts


def process_samples(input_path: str, output_path: str, debug: bool = False):
    output_data: dict[str, list[Act]] = {}

    # Check if input refers to a directory or a file
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            acts = find_acts_in_file(file_path, debug)
            output_data[filename] = acts
    else:
        filename = os.path.basename(input_path)
        acts = find_acts_in_file(input_path, debug)
        output_data[filename] = acts

    output_type = os.path.splitext(output_path)[1]

    # JSON file
    if output_type == ".json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                output_data,
                f,
                ensure_ascii=False,
                indent=2,
                default=lambda o: o.to_dict(),
            )

    # CSV file
    elif output_type == ".csv":
        with open(output_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "full_text", "name", "page"])
            for filename, acts in output_data.items():
                for act in acts:
                    writer.writerow([filename, act.full_text, act.name, act.page])

    # Plain text file
    else:
        lines = []
        for filename, acts in output_data.items():
            lines.append("*" * 80 + "\n")
            lines.append(f"File: {filename}\n")
            lines.append("*" * 80 + "\n")
            for act in acts:
                lines.append(f"Page {act.page}\n\n")
                lines.append(act.full_text + "\n\n")
                lines.append(f"Affected name: {act.name}\n")
                lines.append("-" * 80 + "\n")
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)


if __name__ == "__main__":
    if not os.path.exists(EXTRACTION_PATH):
        os.mkdir(EXTRACTION_PATH)
    process_samples(INPUT_PATH, EXTRACTION_PATH, debug=True)
