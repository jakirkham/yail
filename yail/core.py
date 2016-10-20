__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Oct 20, 2016 11:42$"


import itertools

import toolz.itertoolz   # noqa  # pylint: disable=W0611

from toolz.itertoolz import (
    accumulate,               # pylint: disable=W0611
    concat,
    sliding_window,           # pylint: disable=W0611
)  # noqa

from toolz.compatibility import (
    range,                         # noqa  # pylint: disable-msg=W0611,W0622
    map,                           # noqa  # pylint: disable-msg=W0611,W0622
    zip,                           # noqa  # pylint: disable-msg=W0611,W0622
    zip_longest,                   # noqa  # pylint: disable-msg=W0611,W0622
)  # noqa


def generator(it):
    """ Creates a generator type from the iterable.

    Args:

        it(iterable):            An iterable to make a generator.

    Returns:

        generator:               A generator made from the iterable.

    Examples:

        >>> generator(range(5))  # doctest: +ELLIPSIS
        <generator object generator at 0x...>

        >>> list(generator(range(5)))
        [0, 1, 2, 3, 4]
    """

    for each in it:
        yield each


def empty():
    """ Creates an empty iterator.

    Examples:

        >>> list(empty())
        []
    """

    return iter([])


def single(val):
    """ Creates an iterator with a single value.

    Args:

        val(any):               Single value to add to the iterator.

    Returns:

        iterable:               An iterable yielding the single value.

    Examples:

        >>> list(single(1))
        [1]
    """

    yield val


def cycles(seq, n=1):
    """ Cycles through the sequence n-times.

    Basically the same as ``itertools.cycle`` except that this sets
    an upper limit on how many cycles will be done.

    Note:

        If ``n`` is `None`, this is identical to ``itertools.cycle``.

    Args:

        seq(iterable):           The sequence to grab items from.
        n(integral):             Number of times to cycle through.

    Returns:

        generator:               The cycled sequence generator.

    Examples:

        >>> list(cycles([1, 2, 3], 2))
        [1, 2, 3, 1, 2, 3]
    """

    if n is None:
        return(itertools.cycle(seq))

    assert (n >= 0), "n must be positive, but got n = " + repr(n)
    assert ((n % 1) == 0), "n must be an integer, but got n = " + repr(n)

    return concat(itertools.tee(seq, n))


def duplicate(seq, n=1):
    """ Gets each element multiple times.

    Like ``itertools.repeat`` this will repeat each element n-times.
    However, it will do this for each element of the sequence.

    Args:

         seq(iterable):           The sequence to grab items from.
         n(integral):             Number of repeats for each element.

    Returns:

         generator:               A generator of repeated elements.

    Examples:

         >>> list(duplicate([1, 2, 3], 2))
         [1, 1, 2, 2, 3, 3]
    """

    assert (n >= 0), "n must be positive, but got n = " + repr(n)
    assert ((n % 1) == 0), "n must be an integer, but got n = " + repr(n)

    return concat(map(lambda _: itertools.repeat(_, n), seq))


def indices(*sizes):
    """ Iterates over a length/shape.

        Takes a size or sizes (unpacked shape) and iterates through all
        combinations of the indices.

        Args:
            *sizes(int):            list of sizes to iterate over.

        Returns:
            iterable:               an iterator over the sizes.


        Examples:

            >>> list(indices(3, 2))
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    """

    return(itertools.product(*[range(_) for _ in sizes]))


def pad(seq, before=0, after=0, fill=None):
    """ Pads a sequence by a fill value before and/or after.

    Pads the sequence before and after using the fill value provided
    by ``fill`` up to the lengths specified by ``before`` and
    ``after``. If either ``before`` or ``after`` is ``None``, pad
    the fill value infinitely on the respective end.

    Note:
        If ``before``is ``None``, the sequence will only be the fill
        value.

    Args:

        seq(iterable):          Sequence to pad.
        before(integral):       Amount to pad before.
        after(integral):        Amount to pad after.
        fill(any):              Some value to pad with.

    Returns:

        iterable:               A sequence that has been padded.

    Examples:

        >>> list(pad(range(2, 4), before=1, after=2, fill=0))
        [0, 2, 3, 0, 0]

    """

    all_seqs = []

    if before is None:
        return itertools.repeat(fill)
    elif before > 0:
        all_seqs.append(itertools.repeat(fill, before))

    all_seqs.append(seq)

    if after is None:
        all_seqs.append(itertools.repeat(fill))
    elif after > 0:
        all_seqs.append(itertools.repeat(fill, after))

    return concat(all_seqs)
