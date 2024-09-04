import argparse

from qdrec.scripts.append_nominations import process_samples


def main():
    parser = argparse.ArgumentParser(
        description="QDREC: Extract nomination and exoneration acts from PDF files"
    )

    parser.add_argument(
        "input",
        type=str,
        help="Input file or directory",
    )

    parser.add_argument(
        "output",
        type=str,
        help="Output file (txt, csv, or json)",
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if input_path is None:
        parser.error("Please provide an input file or directory")

    if output_path is None:
        parser.error("Please provide an output file or directory")

    process_samples(input_path, output_path)


if __name__ == "__main__":
    main()
