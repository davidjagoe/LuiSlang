
from copy import copy


class LazySeq(object):
    
    def __init__(self, procedure):
        self._procedure = procedure
        self._list = []

    def __copy(self):
        new = LazySeq(self._procedure)
        # A particularly naive part of this implementation. However,
        # this is 'easily' fixed by using persistent data structures.
        new._list = copy(self._list)
        return new

    def cons(self, item):
        seq = self.__copy()
        seq._list.append(item)
        return seq

    def __next(self):
        seq = self._procedure()
        self._list = self._list + seq._list
        self._procedure = seq._procedure
        return self

    def __realize(self, n):
        # TODO: need to do this iteratively instead of recursively to
        # prevent stack overflow
        if n < len(self):
            return self
        else:
            self = self.__next()
            return self.__realize(n)

    def take(self, n):
        self = self.__realize(n)
        return self._list[:n]

    def drop(self, n):
        self = self.__realize(n)
        seq = self.__copy()
        seq._list = self._list[n:]
        return seq

    def nth(self, n):
        self = self.__realize(n)
        return self._list[n]

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return str(self._list)


class Binding(object):

    def __init__(self, fn, *args, **kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        return self._fn(*self._args, **self._kwargs)


# Syntactic sugar; using recur is more readable in user code
recur = Binding


def iterate(fn, arg):
    val = fn(arg)
    return LazySeq(recur(iterate, fn, val)).cons(arg)


def constantly(x):
    def _x(*args):
        return x
    return _x


def repeat(x):
    return LazySeq(recur(repeat, x)).cons(x)


def cycle(xs):
    first = xs[0]
    xs_ = xs[1:] + [first]
    return LazySeq(recur(cycle, xs_)).cons(first)
