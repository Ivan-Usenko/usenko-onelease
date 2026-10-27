from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path

from ..domain.models import RentalListing
from ..domain.parse import to_rental_listing
from ..sources.json_file import read_rows


def deduplicate(items: Iterable[RentalListing]) -> Iterator[RentalListing]:
    seen: set[tuple[str, str]] = set()

    for vacancy in items:
        if vacancy.key not in seen:
            seen.add(vacancy.key)

            yield vacancy


def count_by_city(items: Iterable[RentalListing]) -> Counter[str]:
    return Counter(vacancy.city for vacancy in items)


def load_rental_listings(path: Path) -> list[RentalListing]:
    rows = read_rows(path)
    parsed = (to_rental_listing(row) for row in rows)
    valid = (v for v in parsed if v is not None)
    return list(deduplicate(valid))
