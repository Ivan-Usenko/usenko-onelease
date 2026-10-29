from dataclasses import dataclass

ELITE_REAL_ESTATE_PRICE_THRESHOLD = 30000


@dataclass(frozen=True, slots=True)
class RentalListing:
    title: str
    company: str
    price: int | None
    city: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not self.company.strip():
            raise ValueError("company must not be empty")
        if self.price is not None and self.price <= 0:
            raise ValueError("price must be positive")

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.company

    @property
    def is_elite_real_estate(self) -> bool:
        return self.price is not None and self.price >= ELITE_REAL_ESTATE_PRICE_THRESHOLD
