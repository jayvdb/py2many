from bar import bar1
from baz import baz1
(let (x (bar1)))
(let (y (baz1)))
(assert (= x 0))
(assert (= y "foo"))
