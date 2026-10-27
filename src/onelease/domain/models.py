from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RentalListing:
    title: str
    company: str
    price: int | None
    city: str

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.company
