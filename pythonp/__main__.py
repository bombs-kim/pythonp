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


def p(value, *args, **kwargs):
    # TODO: Add dostring
    if isinstance(value, str):
        print(value, *args, file=sys.stdout, **kwargs)
        return

    try:
        values = iter(value)
    except TypeError:
        # If value is not iterable, just print it
        print(value, *args, file=sys.stdout, **kwargs)
        return

    if args:
        raise Exception("Giving extra arguments with a sequence of strs is not allowed")

    # TODO: Decide default end character for a sequence input
    #       Which one would be better, '' or '\n'?
    # kwargs['end'] = kwargs.get('end', '')
    for v in values:
        print(v, *args, file=sys.stdout, **kwargs)


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
            if len(line) and line[-1] == '\n':
                line = line[:-1]
            yield line

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            return next(islice(self, key, key+1))
        elif isinstance(key, slice):
            return islice(self, key.start, key.stop, key.step)
        raise KeyError('Error')


# TODO: maybe remove this type and instruct users to use `list(lines)`
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


def is_python2():
    return sys.version_info[0] == 2


# MonitoredStdout and _make_new_writer is used to detect write event
# of sys.stdout in python2 and python3 respectively.

class MonitoredStdout(object):
    def __init__(self, sys, write_called):
        self.sys = sys
        self.write_called = write_called

    def write(self, value):
        self.sys.stdout = self.sys.__stdout__
        self.write_called[0] = True
        self.sys.__stdout__.write(value)


def _make_new_writer(old_writer, flag):
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
    # TODO: Maybe pass a copied globals() each time
    # to minimize side effects
    write_called = [False]
    stdout = sys.stdout

    if is_python2():
        sys.stdout = MonitoredStdout(sys, write_called)
    else:
        write_backup, buffer_write_backup = stdout.write, stdout.buffer.write
        stdout.write = _make_new_writer(
            stdout.write, write_called)
        stdout.buffer.write = _make_new_writer(
            stdout.buffer.write, write_called)

    result = exec_and_eval_last(code, globals)

    if is_python2():
        sys.stdout = sys.__stdout__
    else:
        stdout.write, stdout.buffer.write = write_backup, buffer_write_backup

    # If nothing was written to stdout print the last expression
    if not write_called[0] and result is not None:
        p(result)


def preprocess(code):
    vinfo = sys.version_info
    if vinfo[0] != 3 or vinfo[1] < 6:
        return code.replace("`", '"""')

    _chunks = code.split('`')
    chunks = []
    for idx, c in enumerate(_chunks[:-1]):
        chunks.append(c)
        if idx % 2 == 0:
            chunks.append('f')
        chunks.append('"""')
    chunks.append(_chunks[-1])
    return ''.join(chunks)


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
       by find_name function.
    """

    def find_name(key):
        """In eval or exec, the global scope is a default dict and
           this function defines fallback behaviors for __missing__ events.
        """
        try:
            return getattr(builtins, key)
        except AttributeError:
            pass
        try:
            if is_python2():
                return __import__(key)
            return importlib.__import__(key)
        except ImportError:
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
        # to avoid UnboundLocalError(local variable
        # __builtins__ referenced before assignment) in python 2,
        # the following line is needed
        global __builtins__

    # A hack to support automatic importing.
    # We use a defaultdict object
    # as the global for eval and exec later.
    fname = make_find_name(__builtins__)
    g = keydefaultdict(fname)
    g.update(globals())
    # import ipdb
    # ipdb.set_trace(context=15)
    code = preprocess(args.code[0])

    if args.each:
        lines = g['lines']
        del g['lines'], g['_lines']
        for l in lines:
            g['l'] = l
            exec_one(code, g)
    else:
        exec_one(code, g)


if __name__ == '__main__':
    main()
