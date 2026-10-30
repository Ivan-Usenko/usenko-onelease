from collections.abc import Iterator
from typing import Any

from onelease.services.pipeline import Pipeline


class FakeSource:
    def __init__(self, rows: list[dict[str, Any]], name: str = "fake") -> None:
        self.name = name
        self._rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self._rows


ROW = {"title": "Listing 1", "company": "Company 1", "price": "6000", "city": "Київ"}


def test_invalid_row_is_skipped_not_raised() -> None:
    stats = Pipeline([FakeSource([ROW, {"title": "", "company": "B"}])]).run()
    assert stats.invalid == 1 and stats.kept == 1


def test_duplicates_across_sources() -> None:
    stats = Pipeline([FakeSource([ROW], "a"), FakeSource([ROW], "b")]).run()
    assert stats.duplicates == 1
    assert stats.by_source == {"a": 1}


def test_unknown_price_is_not_an_error() -> None:
    row = dict(ROW, price="за домовленістю")
    stats = Pipeline([FakeSource([row])]).run()
    assert stats.kept == 1 and stats.invalid == 0


def test_empty_source_is_not_an_error() -> None:
    stats = Pipeline([FakeSource([])]).run()
    assert stats.read == 0


def test_invalid_price_is_not_an_error() -> None:
    stats = Pipeline(
        [FakeSource([{"title": "L1", "company": "C1", "price": "invalid", "city": "Kyiv"}])]
    ).run()
    assert stats.kept == 1
