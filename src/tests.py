
import unittest

from lazy_seq import LazySeq, recur


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


if __name__ == "__main__":
    unittest.main()
