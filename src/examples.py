
from lazy_seq import LazySeq, recur, iterate, repeat, cycle

def inc(x):
    return x + 1

print "Demonstrate the use of iterate"
print "clojure: (take 5 (iterate inc 10)) --> (10 11 12 13 14)"
print iterate(inc, 10).take(5) # --> [10, 11, 12, 13, 14]
print iterate(inc, 10).drop(10).take(10)

print "Demonstrate the use of repeat"
print "clojure: (take 4 (repeat [1 2])) --> ([1 2] [1 2] [1 2] [1 2])"
seq = repeat([1, 2])
print seq.take(4)
print seq.take(10)

print "Demonstrate the use of cycle"
print "clojure: (take 5 (cycle [1 2 3])) --> (1 2 3 1 2)"
x = cycle([1, 2, 3]) # --> infinite lazy seq
print x.take(5)      # --> [1,2,3,1,2]
print x.drop(1).take(4) # --> [2,3,1,2] ; no work done - uses auto-cached results
print x.nth(0) # Can't do this with iterators! --> 1
# or this
x_offset_1 = x.drop(1) # --> new lazy sequence pre-cached with results
print x.take(5) # same as before; with auto-cached results - no work done
print x_offset_1.take(5) # only 1 computation --> [2, 3, 1, 2, 3]

print """Clojure version of fib using iterate:
 (defn fib-step [[a b]]
   [b (+ a b)])
 
 (defn fib-seq []
   (map first (iterate fib-step [0 1])))
 """

# Equivalent in python:

def fib_step(a_b):
    a, b = a_b
    return [b, a+b]

def fib_seq():
    return iterate(fib_step, (0, 1))

print map(lambda x: x[0], fib_seq().take(5))
    
