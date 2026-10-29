import pytest

from onelease.domain.models import RentalListing


@pytest.mark.parametrize(
    "title, company, price",
    [
        ("   ", "Company 1", 100),
        ("house", "", 100),
        ("house", "Company 1", -5),
        ("house", "Company 1", 0),
    ],
)
def test_invalid_rental_listing_rejected(title: str, company: str, price: int) -> None:
    with pytest.raises(ValueError):
        RentalListing(title, company, price, "Київ")


def test_frozen_model_is_hashable() -> None:
    a = RentalListing("house", "Company 1", 100, "Київ")
    b = RentalListing("house", "Company 1", 100, "Київ")
    assert len({a, b}) == 1
