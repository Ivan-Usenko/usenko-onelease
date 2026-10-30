import csv
import pathlib
import random

random.seed(7)
titles = ["Однокімнатна квартира", "Маєток", "Дім", "Гараж"]
cities = ["Київ", "Львів", "Одеса", "Харків", "Дніпро"]
path = pathlib.Path("data/large.csv")

prev = None
with path.open("w", encoding="utf-8") as f:
    writer = csv.DictWriter(f, ["title", "company", "price", "location"], delimiter=";")
    writer.writeheader()
    for i in range(5_000):
        if i % 10 == 3 and prev is not None:
            row = dict(prev)  # дублікат оголошення
        else:
            row = {
                "title": f"{random.choice(titles)} {i}",
                "company": f"Company {i % 4000}",
                "price": str(random.randint(5000, 35000)) if i % 7 else "за домовленістю",
                "location": random.choice(cities),
            }

        if i % 1000 == 0:
            row = dict(row, title="")  # некоректний запис
        writer.writerow(row)
        prev = row
