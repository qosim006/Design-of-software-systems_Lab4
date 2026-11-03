"""
Task 8 — The Java habit that broke the search

Answers:
8.1 Python keeps only the second definition under the name search; it
    replaces the first definition, and filters becomes a required argument.
8.2 One method uses filters=None to support calls with and without filters.
    A mutable default dictionary could be shared and modified across calls.
8.3 A keyword-only filters dictionary keeps the API explicit and allows
    additional filter fields without changing the method signature.
8.4 pyflakes reports F811: redefinition of unused name 'search' (the first
    definition is replaced by the second one).
"""


class ProductSearch:
    def __init__(self, products: list[dict]) -> None:
        self.products = products

    def search(self, query: str, *, filters: dict | None = None) -> list[dict]:
        q = query.lower()
        result = [p for p in self.products if q in p["title"].lower()]

        if filters is None:
            filters = {}

        for key, value in filters.items():
            result = [p for p in result if p.get(key) == value]
        return result


def sample_search() -> ProductSearch:
    return ProductSearch([
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "iPhone 14", "brand": "Apple"},
        {"title": "Galaxy S24", "brand": "Samsung"},
    ])


def test_search_without_filters():
    assert len(sample_search().search("iphone")) == 2


def test_search_with_filters():
    result = sample_search().search("iphone", filters={"brand": "Apple"})
    assert [item["title"] for item in result] == ["iPhone 15", "iPhone 14"]


def test_search_returns_empty_for_no_match():
    assert sample_search().search("pixel") == []
