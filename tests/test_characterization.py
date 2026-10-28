from onelease.services.pipeline import PipelineStats, parse_all, batched


def test_invalid_rows_are_counted():
    rows = [
        {"title": "Dev", "company": "A", "salary": "100", "city": "Київ"},
        {"title": "", "company": "B", "salary": "200", "city": "Львів"},
    ]
    stats = PipelineStats()
    result = list(parse_all(rows, stats))  # матеріалізуємо один раз
    assert len(result) == 1
    assert stats.read == 2
    assert stats.invalid == 1


def test_batched_splits_tail():
    assert [len(b) for b in batched(range(7), 3)] == [3, 3, 1]
