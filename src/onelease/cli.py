import argparse
from pathlib import Path

from .services.pipeline import count_by_city, load_rental_listings


def main() -> None:
    parser = argparse.ArgumentParser(prog="onelease")
    parser.add_argument("path", type=Path, help="файл із даними")
    args = parser.parse_args()

    rental_listings = load_rental_listings(args.path)
    print(f"Завантажено записів: {len(rental_listings)}")
    for city, count in count_by_city(rental_listings).most_common():
        print(f" {city}: {count}")


if __name__ == "__main__":
    main()
