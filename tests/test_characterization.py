from pathlib import Path

from onelease.services.pipeline import load_rental_listings


def test_legacy_output_is_stable():
    rows = load_rental_listings(Path("data/ads.json"))
    assert len(rows) == 8  # дублікати злилися
    assert rows[0].title == "однокімнатна квартира"
    assert rows[0].price == 7000
    assert rows[1].price is None  # нечислова ціна -> None
