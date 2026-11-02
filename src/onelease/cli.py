import argparse
import logging
from collections.abc import Callable
from pathlib import Path

from .config import Settings
from .errors import OneleaseError, SourceError
from .logging_setup import setup
from .services.pipeline import Pipeline
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonlSource

logger = logging.getLogger(__name__)

FACTORIES: dict[str, Callable[[Path], Source]] = {
    ".jsonl": JsonlSource,
    ".csv": CsvSource,
}


def build_source(path: Path) -> Source:
    try:
        factory = FACTORIES[path.suffix]
    except KeyError:
        raise SourceError(f"unsupported file type: {path.suffix}") from None

    return factory(path)


def main() -> None:
    parser = argparse.ArgumentParser(prog="onelease")
    parser.add_argument("paths", nargs="+", type=Path, help="файл із даними")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="перекриває значення з .env і змінних середовища",
    )
    args = parser.parse_args()

    settings = Settings()
    setup(args.log_level or settings.log_level)

    try:
        sources = [build_source(p) for p in args.paths]
        stats = Pipeline(sources).run()
    except OneleaseError as exc:
        logger.error("%s", exc)
        raise SystemExit(1) from exc

    print(f"Прочитано записів:  {stats.read}")
    print(f"Відхилено:          {stats.invalid}")
    print(f"Дублікатів:         {stats.duplicates}")
    print(f"Залишилось:         {stats.kept}")
    for name, count in stats.by_source.items():
        print(f"   з {name}: {count}")


if __name__ == "__main__":
    main()
