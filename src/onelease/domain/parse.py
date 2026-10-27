from typing import Any

from .models import RentalListing


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_price(raw: Any) -> int | None:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def to_rental_listing(row: dict) -> RentalListing | None:
    title = row.get("title") or ""

    if not title.strip():
        return None

    return RentalListing(
        title=normalize_title(title),
        company=row.get("company", ""),
        price=parse_price(row.get("price")),
        city=row.get("city", ""),
    )
