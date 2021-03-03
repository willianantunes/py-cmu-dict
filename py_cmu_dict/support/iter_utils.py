from itertools import islice


def chunker(iterable, size):
    """
    See more details at: `https://stackoverflow.com/a/54431431/3899136`
    """

    def chunker_generator(generator, size):
        iterator = iter(generator)
        for first in iterator:

            def chunk():
                yield first
                for more in islice(iterator, size - 1):
                    yield more

            yield [k for k in chunk()]

    if not hasattr(iterable, "__len__"):
        # Generators don't have len, so fall back to slower method that works with generators
        for chunk in chunker_generator(iterable, size):
            yield chunk
        return

    it = iter(iterable)

    for i in range(0, len(iterable), size):
        yield [k for k in islice(it, size)]
