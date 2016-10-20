__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Oct 20, 2016 11:42$"


import itertools

import toolz.itertoolz

from toolz.itertoolz import (
    concat,
)

from toolz.compatibility import (
    range,
    map,
    zip,
    zip_longest,
)


def empty():
    """ Creates an empty iterator.

    Examples:

        >>> list(empty())
        []
    """

    return iter([])


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
