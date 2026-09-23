import re


def parse_price(text: str) -> tuple[float | None, str | None]:
    """
    Витягує суму та валюту з тексту оголошення.
    Повертає (сума, валюта) або (None, None), якщо не знайдено.

    >>> parse_price("15000 грн/міс")
    (15000.0, 'UAH')
    >>> parse_price("$450 в місяць")
    (450.0, 'USD')
    >>> parse_price("Ціна: 12 500 грн")
    (12500.0, 'UAH')
    """
    currency_map = {
        "€": "EUR",
        "eur": "EUR",
        "$": "USD",
        "usd": "USD",
        "грн": "UAH",
        "uah": "UAH",
        "₴": "UAH",
    }

    text_lower = text.lower()

    # шукаємо число (з пробілами як роздільниками тисяч)
    match = re.search(r"(\d[\d\s]*(?:[.,]\d+)?)", text)
    if not match:
        return None, None

    number_str = match.group(1).replace(" ", "").replace(",", ".")
    try:
        amount = float(number_str)
    except ValueError:
        return None, None

    currency = None
    for symbol, code in currency_map.items():
        if symbol in text_lower:
            currency = code
            break

    return amount, currency
