import argparse
import time
import tracemalloc
from itertools import islice
from pathlib import Path

from .services.pipeline import PipelineStats, collect, deduplicate, parse_all
from .sources.json_file import read_rows_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(prog="onelease")
    parser.add_argument("path", type=Path, help="файл із даними")
    parser.add_argument("--preview", type=int, help="кількість об'єктів для попереднього перегляду")
    parser.add_argument("--stats", action="store_true", help="показати статистику")
    args = parser.parse_args()

    tracemalloc.start()
    t0 = time.perf_counter()

    stats = PipelineStats()
    pipeline = deduplicate(parse_all(read_rows_jsonl(args.path), stats), stats)
    collect(pipeline, stats)

    if args.stats:
        print(f"Прочитано записів:\t{stats.read}")
        print(f"Відхилено:\t\t{stats.invalid}")
        print(f"Дублікатів:\t\t{stats.duplicates}")
        print(f"Залишилось:\t\t{stats.kept}")
        print(f"Ціна: min={stats.price_min} max={stats.price_max} avg={stats.price_avg}")

    if args.preview:
        for listing in islice(pipeline, args.preview):
            print(listing)

        print(f"{stats.read=}")
        return

    for city, count in stats.by_city.items():
        print(f"  {city}: {count}")

    peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024
    tracemalloc.stop()

    print(f"Час: {time.perf_counter() - t0:.2f} с, пік пам'яті {peak:.1f} МБ")


if __name__ == "__main__":
    main()
