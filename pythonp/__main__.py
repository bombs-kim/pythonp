#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import ast
from collections import defaultdict
import importlib
from itertools import chain, islice
import sys

try:
    from _collections_abc import Iterable, Sequence
except:
    from collections import Iterable, Sequence


# ## Handy global vairables defined
# TODO


# ## Examples
# TODO


def stripped_str(v):
    v = str(v)
    if len(v) and v[-1] == '\n':
        return v[:-1]
    return v


def p(value, *args, **kwargs):
    # TODO: Add dostring
    if isinstance(value, str):
        print(stripped_str(value), *args, **kwargs)
        return

    try:
        values = iter(value)
    except TypeError:
        # If value is not iterable, just print it
        print(stripped_str(value), *args, **kwargs)
        return

    if args:
        raise Exception("Giving extra arguments with a sequence of strs is not allowed")

    # TODO: Decide default end character for a sequence input
    #       Which one would be better, '' or '\n'?
    # kwargs['end'] = kwargs.get('end', '')
    for v in values:
        print(stripped_str(v), *args, **kwargs)


# [Abstract base classes(ABC's) used]
# Iterable: What you can get an iterator from. A container.
# Iterator: What you can call next() on.
# Sequence: What supports all the operations on a read-only sequence, such
#           as __contains__, __reversed__, index and count methods
# Note that Iterable and Iterator are not mutually exclusive in python,
# which can be confusing from time to time. For example, every iterator
# is an iterable.


class SubscriptableStdin(Iterable):
    def __iter__(self):
        for line in sys.stdin:
            yield line

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            return next(islice(self, key, key+1))
        elif isinstance(key, slice):
            return islice(self, key.start, key.stop, key.step)
        raise KeyError('Error')


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


# TODO: Maybe lines -> ls for brevity
lines = SubscriptableStdin()
_lines = LazySequence(lines)


def exec_and_eval_last(code, globals):
    stmts = list(ast.iter_child_nodes(ast.parse(code)))
    if not len(stmts):
        raise Exception("No statements given")

    if isinstance(stmts[-1], ast.Expr):
        if len(stmts) > 1:
            exec(compile(ast.Module(
                body=stmts[:-1]), filename="<ast>", mode="exec"), globals)
        return eval(compile(ast.Expression(body=stmts[-1].value), filename="<ast>", mode="eval"), globals)

    exec(code, globals)


def _make_new_writer(old_writer, flag: list):
    self = old_writer.__self__

    # TODO: change this to bound method if needed
    # For example, like
    # https://stackoverflow.com/questions/1015307/python-bind-an-unbound-method
    def new_writer(value):
        """Detects write events and set flag"""
        self.write = old_writer
        flag[0] = True
        old_writer(value)

    return new_writer


def exec_one(code, globals):
    # TODO: How bout copying a globals() before passing it
    write_called = [False]
    stdout = sys.stdout
    write_backup, buffer_write_backup = stdout.write, stdout.buffer.write

    stdout.write = _make_new_writer(
        stdout.write, write_called)
    stdout.buffer.write = _make_new_writer(
        stdout.buffer.write, write_called)
    result = exec_and_eval_last(code, globals)

    stdout.write, stdout.buffer.write = write_backup, buffer_write_backup

    # If nothing was written to stdout print the last expression
    if not write_called[0] and result is not None:
        p(result)



class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def make_find_name(builtins):
    """In some edge cases, accessing builtins in eval or exec
       is not easy at all. To cover all the cases, we make a
       clsoure including `builtins` and make them always accessible
    """

    def find_name(key):
        """In eval or exec, the global scope is a default dict and
           this function defines fallback behaviors in case of
           __missing__
        """
        try:
            return getattr(builtins, key)
        except AttributeError:
            pass
        try:
            return importlib.__import__(key)
        except KeyError:
            raise KeyError(key)

    return find_name


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='pythonp')
    parser.add_argument('-e', '--each',
                        action='store_true',
                        help="evalute code on each 'line'")
    parser.add_argument('code', nargs=1)
    args = parser.parse_args()

    try:
        # In case of python 3
        import builtins as __builtins__
    except ImportError:
        pass

    # Automatic importing support
    fname = make_find_name(__builtins__)
    g = keydefaultdict(fname)
    g.update(globals())

    if args.each:
        del g['lines'], g['_lines']
        for l in sys.stdin:
            g['l'] = l
            exec_one(args.code[0], g)
    else:
        exec_one(args.code[0], g)


if __name__ == '__main__':
    main()
