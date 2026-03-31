from dataclasses import dataclass, field
from itertools import batched
from typing import Any, Generator, Iterable, Self, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class Fibo:
    def __init__(self, n: int) -> None:
        self.n = n
        self.index = 0
        self.prev = 0
        self.curr = 1

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self.index >= self.n:
            raise StopIteration

        if self.index == 0:
            result = 0
        elif self.index == 1:
            result = 1
        else:
            result = self.prev + self.curr
            self.prev, self.curr = self.curr, result

        self.index += 1
        return result


class RetrieveRemoteData:
    def __init__(self, per_page: int) -> None:
        self.per_page = per_page

    def __iter__(self) -> Generator[int, Any, None]:
        page = 1
        while True:
            query = Query(per_page=self.per_page, page=page)
            page_data = request(query)
            for item in page_data.results:
                yield item
            if page_data.next is None:
                break
            page = page_data.next
