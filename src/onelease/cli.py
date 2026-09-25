from onelease.domain.parse import parse_price


def main() -> None:
    print("OneLease 0.1.0 - середовище налаштовано")
    print(f"Результат парсингу ціни \"1500 грн/міс\": {parse_price("1500 грн/міс")}")


if __name__ == "__main__":
    main()
