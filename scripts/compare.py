import time
import tracemalloc
from pathlib import Path

from onelease.services.pipeline import (
    PipelineStats,
    collect,
    deduplicate,
    parse_all,
    to_rental_listing,
)
from onelease.sources.json_file import read_rows_jsonl

path = Path("data/large.jsonl")


def lazy():
    stats = PipelineStats()
    collect(deduplicate(parse_all(read_rows_jsonl(path), stats), stats), stats)
    return stats.kept


def greedy():
    rows = list(read_rows_jsonl(path))  # усе в памʼяті
    parsed = [to_rental_listing(r) for r in rows]
    valid = [v for v in parsed if v is not None]
    seen, unique = set(), []
    for v in valid:
        if v.key not in seen:
            seen.add(v.key)
            unique.append(v)
    return len(unique)


for name, fn in (("генераторний конвеєр", lazy), ("проміжні списки", greedy)):
    tracemalloc.start()
    t0 = time.perf_counter()
    n = fn()
    elapsed = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024
    tracemalloc.stop()
    print(f"{name:22} {n} записів {elapsed:.2f} с пік {peak:.1f} МБ")
