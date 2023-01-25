from typing import Generator

from .typing import T


def paginate_generator(
    generator: Generator[T, None, None],
    limit: int
) -> Generator[list[T], None, None]:
    """
    Paginate a generator by a given limit (page size).

    Example:
        >>> g = range(10000)
        >>> for page in paginate_generator(g, 100):
        >>>     print(page)

    :param generator: the generator to be paginated
    :type generator: Generator[T, None, None]
    :param limit: number of items per page
    :type limit: int
    :return: a generator of pages, where each page is a list of items
    :rtype: Generator[list[T], None, None]
    :Note:
        If limit is zero (or negative for that matter), it returns the whole generator as a list
    """
    page: list[T] = []
    for item in generator:
        page.append(item)
        if len(page) == limit:
            yield page
            page = []
    if page:  # Last page
        yield page
