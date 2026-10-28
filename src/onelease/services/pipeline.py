from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from itertools import islice

from ..domain.models import RentalListing
from ..domain.parse import to_rental_listing


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_city: Counter = field(default_factory=Counter)
    price_count: int = 0
    price_sum: int = 0
    price_min: int | None = None
    price_max: int | None = None

    @property
    def price_avg(self) -> float | None:
        if not self.price_count:
            return None
        return self.price_sum / self.price_count


def parse_all(rows: Iterable[dict], stats: PipelineStats) -> Iterator[RentalListing]:
    for row in rows:
        stats.read += 1
        listing = to_rental_listing(row)
        if listing is None:
            stats.invalid += 1
            continue
        yield listing


def deduplicate(items: Iterable[RentalListing], stats: PipelineStats) -> Iterator[RentalListing]:
    seen: set[tuple[str, str]] = set()
    for listing in items:
        if listing.key in seen:
            stats.duplicates += 1
            continue
        seen.add(listing.key)
        yield listing


def count_by_city(items: Iterable[RentalListing]) -> Counter[str]:
    return Counter(vacancy.city for vacancy in items)


def collect(items: Iterable[RentalListing], stats: PipelineStats) -> None:
    for listing in items:
        stats.kept += 1
        stats.by_city[listing.city] += 1
        price = listing.price
        if price is None:
            continue
        stats.price_count += 1
        stats.price_sum += price
        if stats.price_min is None or price < stats.price_min:
            stats.price_min = price
        if stats.price_max is None or price > stats.price_max:
            stats.price_max = price


def batched(items: Iterable[RentalListing], size: int) -> Iterator[tuple[RentalListing, ...]]:
    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch
