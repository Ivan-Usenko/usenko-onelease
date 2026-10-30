from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field

from pydantic import ValidationError

from ..domain.models import RentalListing
from .ports import Source
from .schemas import RentalListingIn


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_source: Counter[str] = field(default_factory=Counter)
    by_city: Counter[str] = field(default_factory=Counter)


class Pipeline:
    def __init__(self, sources: list[Source]) -> None:
        self._sources = sources

    def run(self) -> PipelineStats:
        stats = PipelineStats()
        seen: set[tuple[str, str]] = set()
        for source in self._sources:
            for listing in self._parse(source, stats):
                if listing.key in seen:
                    stats.duplicates += 1
                    continue
                seen.add(listing.key)
                stats.kept += 1
                stats.by_source[source.name] += 1
                stats.by_city[listing.city] += 1
        return stats

    @staticmethod
    def _parse(source: Source, stats: PipelineStats) -> Iterator[RentalListing]:
        for row in source.read():
            stats.read += 1
            try:
                yield RentalListingIn.model_validate(row).to_domain()
            except ValidationError:
                stats.invalid += 1
