import argparse
from collections.abc import Callable
from pathlib import Path

from .services.pipeline import Pipeline
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonlSource

FACTORIES: dict[str, Callable[[Path], Source]] = {
    ".jsonl": JsonlSource,
    ".csv": CsvSource,
}


def build_source(path: Path) -> Source:
    try:
        factory = FACTORIES[path.suffix]
    except KeyError:
        raise SystemExit(f"unsupported file type: {path.suffix}") from None

    return factory(path)


def main() -> None:
    parser = argparse.ArgumentParser(prog="onelease")
    parser.add_argument("paths", nargs="+", type=Path, help="файл із даними")
    args = parser.parse_args()

    sources = [build_source(p) for p in args.paths]
    stats = Pipeline(sources).run()

    print(f"Прочитано записів:  {stats.read}")
    print(f"Відхилено:          {stats.invalid}")
    print(f"Дублікатів:         {stats.duplicates}")
    print(f"Залишилось:         {stats.kept}")
    for name, count in stats.by_source.items():
        print(f"   з {name}: {count}")


if __name__ == "__main__":
    main()
