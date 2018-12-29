#! /usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from itertools import chain, islice
try:
    from _collections_abc import Iterable, Sequence
except:
    from collections import Iterable, Sequence


# [Handy global vairables defined]
#
# p    : A handy print function with command line usage in mind
# line : First input line
# lines: All input lines including the first one. Note that this should be
#        considered as a stream. Therefore, you cannot reuse it even though
#        it's subscriptable and allows a one time random access.
# _lines : Lazy evaluted non-stream lines. You can access its element as many
#        times as you want. This is not evaluated until you use it to save up
#        memory.


# [Examples]
# Refer to python officials docs to learn useful string manipulating functions
# https://docs.python.org/3/library/string.html
#
# You are recommended to use generator expressions or list comprehensions
# with pythonc
# https://docs.python.org/3/howto/functional.html
#
# Concatenate filenames
# `ls | pythonc 'p(lines, end=",")'`
#
# Get files whose names are longer than 5
# `ls | pythonc 'p(l for l in lines if len(l)>5)'`
#
# Get the 4th column of the processs status
# `ps | pythonc 'p(l.split()[3] for l in lines[1:])'`
#
# You can also do some crazy stuffs becuase pythonc can do anything
# that python can do
# `ls | pythonc 'from random import sample; p(sample(_lines, 2))'`
# `ls | pythonc 'p(sum(len(l) for l in lines))'`


def p(value, *args, **kwargs):
    """A replacement for the builtin print function that can take a str
    or any sequence type as an input. In the latter case, it prints
    as many time as the number of elements in the sequence"""

    if type(value) is str:
        value = [value.strip()]

    try:
        value = (v.strip() for v in value)
    except TypeError:
        # If value is neither str or sequence type just print it.
        print(value, *args, **kwargs)
        return

    for v in value:
        print(v, *args, **kwargs)


# [Abstract base classes(ABC's) used]
# Iterable: What you can get an iterator from. A container.
# Iterator: What you can call next() on.
# Sequence: What supports all the operations on a read-only sequence, such
#           as __contains__, __reversed__, index and count methods
# Note that Iterable and Iterator are not mutually exclusive in python,
# which can be confusing from time to time. For example, every iterator
# is an iterable.

class SubscriptableIterable(Iterable):
    """A SubscriptableIterable constructs a Iterable from an Iterator."""
    def __init__(self, iterator):
        self.iterator = iterator
        self.used = False
    
    def check_used(self):
        if self.used:
            raise Exception('You cannot use SubscriptableChain twice')
        self.used = True
    
    def __iter__(self):
        self.check_used()
        return self.iterator

    def __getitem__(self, key):
        self.check_used()
        if isinstance(key, int) and key >= 0:
            return next(islice(self.iterator, key, key+1))
        elif isinstance(key, slice):
            return islice(self.iterator, key.start, key.stop, key.step)
        raise KeyError("Error")


class LazySequence(Sequence):
    """A LazySequence lazily constructs a Sequence from an iterable."""

    def __init__(self, iterable):
        self.iterable = iterable
        self.restored = False
    
    def get_container(self):
        if self.restored:
            return
        self.restored = True
        self.restored_iterable = list(self.iterable)
    
    def __len__(self):
        self.get_container()
        return len(self.restored_iterable)
    
    def __getitem__(self, key):
        self.get_container()
        return self.restored_iterable[key]


line = sys.stdin.readline()  # first line
lines = SubscriptableIterable(chain([line], sys.stdin.readlines()))
_lines = LazySequence(lines)


def main():
    exec(sys.argv[1], globals())


if __name__ == '__main__':
    main()
