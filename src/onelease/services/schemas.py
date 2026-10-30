from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..domain.models import RentalListing


class RentalListingIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=200)
    company: str = Field(min_length=1)
    price: int | None = Field(default=None, gt=0)
    city: str = Field(default="", alias="location")

    @field_validator("price", mode="before")
    @classmethod
    def unknown_price(cls, value: object) -> object:
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return None  # «за домовленістю» – ціна невідома

        return value

    @field_validator("title", "company")
    @classmethod
    def strip_spaces(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("title")
    @classmethod
    def lowercase(cls, value: str) -> str:
        return value.lower()

    def to_domain(self) -> RentalListing:
        return RentalListing(
            title=self.title,
            company=self.company,
            price=self.price,
            city=self.city,
        )
