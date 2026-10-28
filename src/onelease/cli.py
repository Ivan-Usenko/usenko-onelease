import argparse
from itertools import islice
from pathlib import Path

from .services.pipeline import PipelineStats, deduplicate, parse_all
from .sources.json_file import read_rows_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(prog="onelease")
    parser.add_argument("path", type=Path, help="файл із даними")
    parser.add_argument("preview", type=int, help="кількість об'єктів для попереднього перегляду")
    args = parser.parse_args()

    stats = PipelineStats()
    pipeline = deduplicate(parse_all(read_rows_jsonl(args.path), stats), stats)

    if args.preview:
        for vacancy in islice(pipeline, args.preview):
            print(vacancy)

        print(f"{stats.read=}")
        return


if __name__ == "__main__":
    main()
