import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from ..services.ports import Source


class CsvSource(Source):
    name = "csv"

    def __init__(self, path: Path, delimiter: str = ";") -> None:
        self._path = path
        self._delimiter = delimiter

    def read(self) -> Iterator[dict[str, Any]]:
        with self._path.open(encoding="utf-8", newline="") as f:
            yield from csv.DictReader(f, delimiter=self._delimiter)
