from onelease.services.pipeline import PipelineStats, batched, parse_all


def test_invalid_rows_are_counted() -> None:
    rows = [
        {"title": "Dev", "company": "A", "price": "100", "city": "Київ"},
        {"title": "", "company": "B", "price": "200", "city": "Львів"},
    ]
    stats = PipelineStats()
    result = list(parse_all(rows, stats))  # матеріалізуємо один раз
    assert len(result) == 1
    assert stats.read == 2
    assert stats.invalid == 1


def test_batched_splits_tail() -> None:
    rows = [{"title": f"{i}", "company": f"A{i}", "price": "100", "city": "Київ"} for i in range(7)]
    stats = PipelineStats()
    result = list(parse_all(rows, stats))  # матеріалізуємо один раз
    assert [len(b) for b in batched(result, 3)] == [3, 3, 1]
