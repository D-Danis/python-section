from dataclasses import dataclass, field
from itertools import batched
from typing import Generator, Iterable, Iterator, Self, TypeAlias

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


class RetrieveRemoteData(Iterable):
    def __init__(self, per_page: int = 3) -> None:
        self.per_page = per_page
        self.page = Page(per_page=per_page, next=1)

    def __iter__(self) -> Generator[SomeRemoteData, None, None]:
        while self.page.next is not None:
            self.page = request(Query(per_page=self.per_page, page=self.page.next))
            yield from self.page.results


class Fibo(Iterator):
    def __init__(self, n: int):
        self.n = n
        self.last = [0, 1]
        self.next = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self.next == self.n:
            raise StopIteration

        self.next += 1

        if self.next == 1:
            return 0

        if self.next == 2:
            return 1

        result = sum(self.last)
        self.last = [self.last[1], result]

        return result
