
import unittest

from lazy_seq import LazySeq, recur, iterate, repeat, cycle


class TestCaseFib(unittest.TestCase):

    def setUp(self):
        self.fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.ncalls = 0

    def _make_test_fib_function(self):
        def fib_iter(a, b):
            self.ncalls += 1
            return LazySeq(recur(fib_iter, b, a+b)).cons(a)
        def fib():
            return fib_iter(0, 1)
        return fib

    def test_computation_only_done_once(self):
        fib_fn = self._make_test_fib_function()
        f = fib_fn()
        self.assertEquals(len(f), 1)
        for i in range(10):
            self.assertEquals(f.nth(i), self.fibs[i])
            self.assertEquals(self.ncalls, i+1)
            self.assertEquals(len(f), i+1)
        for i in range(10):
            self.assertEquals(f.nth(i), self.fibs[i])
            self.assertEquals(self.ncalls, 10)
            self.assertEquals(len(f), 10)

    def test_sub_seqs(self):
        fib_fn = self._make_test_fib_function()
        f = fib_fn()
        self.assertEquals(self.ncalls, 1)
        f2 = f.drop(1)
        self.assertEquals(self.ncalls, 2)
        self.assertEquals(f.nth(5), 5); self.assertEquals(self.ncalls, 6)
        self.assertEquals(f2.nth(0), 1); self.assertEquals(self.ncalls, 6)
        self.assertEquals(f2.nth(5), 8); self.assertEquals(self.ncalls, 11) # 5 more

    def test_sub_seq_retains_completed_computations(self):
        fib_fn = self._make_test_fib_function()
        f = fib_fn()
        self.assertEquals(f.nth(5), 5); self.assertEquals(self.ncalls, 6)
        f2 = f.drop(1)
        self.assertEquals(f2.nth(4), 5); self.assertEquals(self.ncalls, 6)

    def test_iterate(self):
        def constantly(x):
            self.ncalls += 1
            return x
        i = iterate(constantly, 1)
        self.assertEquals(i.nth(0), 1)
        self.assertEquals(i.nth(100), 1)
        self.assertEquals(self.ncalls, 101)
        self.assertEquals(i.nth(50), 1)
        self.assertEquals(self.ncalls, 101)

    def test_iterate_2(self):
        def add_5(x):
            return x + 5
        i = iterate(add_5, 0)
        self.assertEquals(i.nth(0), 5)
        self.assertEquals(i.nth(5), 30)

    def test_repeat(self):
        x = repeat([1, 2, 3])
        self.assertEquals(x.take(3), [[1,2,3],[1,2,3],[1,2,3]])

    def test_cycle(self):
        x = cycle([1, 2, 3])
        expected = [1,2,3,1,2,3,1,2,3] # ...
        self.assertEquals(x.take(9), expected)


if __name__ == "__main__":
    unittest.main()
