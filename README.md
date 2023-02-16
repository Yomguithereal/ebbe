[![Build Status](https://github.com/Yomguithereal/ebbe/workflows/Tests/badge.svg)](https://github.com/Yomguithereal/ebbe/actions)

# Ebbe

A collection of typical helper functions for python that cannot be found in the however great standard library.

## Installation

You can install `ebbe` with pip with the following command:

```
pip install ebbe
```

## Usage

*Iterator functions*

* [as_chunks](#as_chunks)
* [as_grams](#as_grams)
* [fail_fast](#fail_fast)
* [uniq](#uniq)
* [distinct](#distinct)
* [with_prev](#with_prev)
* [with_prev_and_next](#with_prev_and_next)
* [with_next](#with_next)
* [with_is_first](#with_is_first)
* [with_is_last](#with_is_last)
* [without_first](#without_first)
* [without_last](#without_last)

*Utilities*

* [get](#get)
* [getter](#getter)
* [getpath](#getpath)
* [pathgetter](#pathgetter)
* [indexed](#indexed)
* [grouped](#grouped)
* [partitioned](#partitioned)
* [sorted_uniq](#sorted_uniq)
* [pick](#pick)
* [omit](#omit)

*Functional Programming*

* [noop](#noop)
* [compose](#compose)
* [rcompose](#rcompose)

*Formatting*

* [and_join](#and_join)
* [format_int](#format_int)
* [format_time](#format_time)

*Decorators*

* [decorators.fail_fast](#decoratorsfail_fast)
* [decorators.with_defer](#decoratorswith_defer)

*Benchmarking*

* [Timer](#timer)

### as_chunks

Iterate over chunks of the desired size by grouping items as we iterate over them.

```python
from ebbe import as_chunks

list(as_chunks(3, [1, 2, 3, 4, 5]))
>>> [[1, 2, 3], [4, 5]]
```

### as_grams

Iterate over grams (sometimes called n-grams or q-grams etc.) of the given iterable. It works with strings, lists and other sized sequences as well as with lazy iterables without consuming any superfluous memory while doing so.

```python
from ebbe import as_grams

list(as_grams(3, 'hello'))
>>> ['hel', 'ell', 'llo']

list(as_grams(2, (i * 2 for i in range(5))))
>>> [(0, 2), (2, 4), (4, 6), (6, 8)]
```

### fail_fast

Take an iterable (but this has been geared towards generators, mostly), and tries to access the first value to see if an Exception will be raised before returning an equivalent iterator.

This is useful with some badly-conceived generators that checks arguments and raise if they are not valid, for instance, and if you don't want to wrap the whole iteration block within a try/except.

This logic is also available as a [decorator](#failfastdecorator).

```python
from ebbe import fail_fast

def hellraiser(n):
  if n > 10:
    raise TypeError

  yield from range(n)

# You will need to do this to catch the error:
gen = hellraiser(15)

try:
  for i in gen:
    print(i)
except TypeError:
  print('Something went wrong when creating the generator')

# With fail_fast
try:
  gen = fail_fast(hellraiser(15))
except TypeError:
  print('Something went wrong when creating the generator')

for i in gen:
  print(i)
```

### uniq

Filter repeated items, optionally by key, seen next to each other in the given iterator.

```python
from ebbe import uniq

list(uniq([1, 1, 1, 2, 3, 4, 4, 5, 5, 6]))
>>> [1, 2, 3, 4, 5, 6]

# BEWARE: it does not try to remember items (like the `uniq` command)
list(uniq([1, 2, 2, 3, 2]))
>>> [1, 2, 3, 2]

# Using a key
list(uniq([(1, 2), (1, 3), (2, 4)], key=lambda x: x[0]))
>>> [(1, 2), (2, 4)]
```

### distinct

Filter repeated items, optionally by key, in the given iterator.

```python
from ebbe import distinct

list(distinct([0, 3, 4, 4, 1, 0, 3]))
>>> [0, 3, 4, 1]

list(distinct(range(6), key=lambda x: x % 2))
>>> [0, 1]
```

### with_prev

Iterate over items along with the previous one.

```python
from ebbe import with_prev

for previous_item, item in with_prev(iterable):
  print(previous_item, 'came before', item)

list(with_prev([1, 2, 3]))
>>> [(None, 1), (1, 2), (2, 3)]
```

### with_prev_and_next

Iterate over items along with the previous and the next one.

```python
from ebbe import with_prev_and_next

for previous_item, item, next_item in with_prev_and_next(iterable):
  print(previous_item, 'came before', item)
  print(next_item, 'will come after', item)

list(with_prev_and_next([1, 2, 3]))
>>> [(None, 1, 2), (1, 2, 3), (2, 3, None)]
```

### with_next

Iterate over items along with the next one.

```python
from ebbe import with_next

for item, next_item in with_next(iterable):
  print(next_item, 'will come after', item)

list(with_next([1, 2, 3]))
>>> [(1, 2), (2, 3), (3, None)]
```

### with_is_first

Iterate over items along with the information that the current item is the first one or not.

```python
from ebbe import with_is_first

for is_first, item in with_is_first(iterable):
  if is_first:
    print(item, 'is first')
  else:
    print(item, 'is not first')

list(with_is_first([1, 2, 3]))
>>> [(True, 1), (False, 2), (False, 3)]
```

### with_is_last

Iterate over items along with the information that the current item is the last one or not.

```python
from ebbe import with_is_last

for is_last, item in with_is_last(iterable):
  if is_last:
    print(item, 'is last')
  else:
    print(item, 'is not last')

list(with_is_last([1, 2, 3]))
>>> [(False, 1), (False, 2), (True, 3)]
```

### without_first

Iterate over the given iterator after skipping its first item. Can be useful if you want to skip headers of a CSV file for instance.

```python
from ebbe import without_first

list(without_first([1, 2, 3]))
>>> [2, 3]

for row in without_first(csv.reader(f)):
  print(row)
```

### without_last

Iterate over the given iterator but skipping its last item.

```python
from ebbe import without_last

list(without_last([1, 2, 3]))
>>> [1, 2]
```

### get

Operator function similar to `operator.getitem` but able to take a default value.

```python
from ebbe import get

get([1, 2, 3], 1)
>>> 2

get([1, 2, 3], 4)
>>> None

# With default value
get([1, 2, 3], 4, 35)
>>> 35
```

### getter

Operator factory similar to `operator.itemgetter` but able to take a default value.

```python
from ebbe import getter

get_second_or_thirty = getter(1, 30)

get_second_or_thirty([1, 2, 3])
>>> 2

get_second_or_thirty([1])
>>> 30

# Overriding default on the spot
get_second_or_thirty([1], 76)
>>> 76
```

### getpath

Operator function used to retrieve a value at given path in a nested structure or a default value if this value cannot be found.

```python
from ebbe import getpath

data = {'a': {'b': [{'c': 34}, 'test'], 'd': 'hello'}}

getpath(data, ['a', 'b', 0, 'c'])
>>> 34

getpath(data, ['t', 'e', 's', 't'])
>>> None

# Using a default return value
getpath(data, ['t', 'e', 's', 't'], 45)
>>> 45

# Using a string path
getpath(data, 'a.b.d', split_char='.')
>>> 'hello'
```

*Arguments*

* **target** *any*: target object.
* **path** *iterable*: path to get.
* **default** *?any* [`None`]: default value to return.
* **items** *?bool* [`True`]: whether to attempt to traverse keys and indices.
* **attributes** *?bool* [`False`]: whether to attempt to traverse attributes.
* **split_char** *?str*: if given, will split strings passed as path instead of raising `TypeError`.
* **parse_indices** *?bool* [`False`]: whether to parse integer indices when splitting string paths.

### pathgetter

Function returning a getter function working as [getpath](#getpath) and partially applied to use the provided path or paths.

```python
from ebbe import pathgetter

data = {'a': {'b': [{'c': 34}, 'test'], 'd': 'hello'}}

getter = pathgetter(['a', 'b', 0, 'c'])
getter(data)
>>> 34

getter = pathgetter(['t', 'e', 's', 't'])
getter(data)
>>> None

# Using a default return value
getter = pathgetter(['t', 'e', 's', 't'])
getter(data, 45)
>>> 45

# Using a string path
getter = pathgetter('a.b.d', split_char='.')
getter(data)
>>> 'hello'

# Using multiple paths
getter = pathgetter(
  ['a', 'b', 0, 'c'],
  ['t', 'e', 's', 't'],
  ['a', 'b', 'd']
)
getter(data)
>>> (34, None, 'hello')
```

*Arguments*

* **paths** *list*: paths to get.
* **items** *?bool* [`True`]: whether to attempt to traverse keys and indices.
* **attributes** *?bool* [`False`]: whether to attempt to traverse attributes.
* **split_char** *?str*: if given, will split strings passed as path instead of raising `TypeError`.
* **parse_indices** *?bool* [`False`]: whether to parse integer indices when splitting string paths.

*Getter arguments*

* **target** *any*: target object.
* **default** *?any* [`None`]: default value to return.

### indexed

Function indexing the given iterable in a dict-like structure. This is basically just some functional sugar over a `dict` constructor.

```python
from ebbe import indexed

indexed(range(3), key=lambda x: x * 10)
>>> {
  0: 0,
  10: 1,
  20: 2
}
```

### grouped

Function grouping the given iterable by a key.

```python
from ebbe import grouped

grouped(range(4), key=lambda x: x % 2)
>>> {
  0: [0, 2],
  1: [1, 3]
}

# Using an optional value
grouped(range(4), key=lambda x: x % 2, value=lambda x: x * 10)
>>> {
  0: [0, 20],
  1: [10, 30]
}

# Using the items variant
from ebbe import grouped_items

grouped_items((x % 2, x * 10) for i in range(4))
>>> {
  0: [0, 20],
  1: [10, 30]
}
```

### partitioned

Function partitioning the given iterable by key.

```python
from ebbe import partitioned

partitioned(range(4), key=lambda x: x % 2)
>>> [
  [0, 2],
  [1, 3]
]

# Using an optional value
partitioned(range(4), key=lambda x: x % 2, value=lambda x: x * 10)
>>> [
  [0, 20],
  [10, 30]
]

# Using the items variant
from ebbe import partitioned_items

partitioned_items((x % 2, x * 10) for i in range(4))
>>> [
  [0, 20],
  [10, 30]
]
```

### sorted_uniq

Function sorting the given iterable then dropping its duplicate through a single linear pass over the data.

```python
from ebbe import sorted_uniq

numbers = [3, 17, 3, 4, 1, 4, 5, 5, 1, -1, 5]
sorted_uniq(numbers)
>>> [-1, 1, 3, 4, 5, 17]

# It accepts all of `sorted` kwargs:
sorted_uniq(numbers, reverse=True)
>>> [17, 5, 4, 3, 1, -1]
```

### pick

Function returning the given dictionary with only the selected keys.

```python
from ebbe import pick

# Selected keys must be an iterable:
pick({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
>>> {'a': 1, 'c': 3}

# If you need the function to raise if one of the picked keys is not found:
pick({'a': 1, 'b': 2, 'c': 3}, ['a', 'd'], strict=True)
>>> KeyError: 'd'
```

### omit

Function returning the given dictionary without the selected keys.

```python
from ebbe import omit

# Selected keys must be a container:
omit({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
>>> {'b': 2}

# If need to select large numbers of keys, use a set:
omit({'a': 1, 'b': 2, 'c': 3}, {'a', 'c'})
>>> {'b': 2}
```

### noop

Noop function (a function that can be called with any arguments and does nothing). Useful as a default to avoid complicating code sometimes.

```python
from ebbe import noop

noop() # Does nothing...
noop(4, 5) # Still does nothing...
noop(4, index=65) # Nothing yet again...
```

### compose

Function returning the composition function of its variadic arguments.

```python
def times_2(x):
  return x * 2

def plus_5(x):
  return x + 5

compose(times_2, plus_5)(10)
>>> 30

# Reverse order
compose(times_2, plus_5, reverse=True)(10)
>>> 25
```

### rcompose

Function returning the reverse composition function of its variadic arguments.

```python
def times_2(x):
  return x * 2

def plus_5(x):
  return x + 5

rcompose(times_2, plus_5)(10)
>>> 25
```

### and_join

Join function able to group the last items with a custom copula such as "and".

```python
from ebbe import and_join

and_join(['1', '2', '3'])
>>> '1, 2 and 3'

and_join(['1', '2', '3'], separator=';', copula="y")
>>> '1; 2 y 3'
```

### format_int

Format given number as an int with thousands separator.

```python
from ebbe import format_int

format_int(4500)
>>> '4,500'

format_int(10000, separator=' ')
>>> '10 000'
```

### format_time

Format time with custom precision and unit from years to nanoseconds.

```python
from ebbe import format_time

format_time(57309)
>>> "57 microseconds and 309 nanoseconds"

format_time(57309, precision="microseconds")
>>> "57 microseconds

format_time(78, unit="seconds")
>>> "1 minute and 18 seconds"

format_time(4865268458795)
>>> "1 hour, 21 minutes, 5 seconds, 268 milliseconds, 458 microseconds and 795 nanoseconds"

assert format_time(4865268458795, max_items=2)
>>> "1 hour and 21 minutes"

format_time(4865268458795, short=True)
>>> "1h, 21m, 5s, 268ms, 458µs, 795ns"
```

### decorators.fail_fast

Decorate a generator function by wrapping it into another generator function that will fail fast if some validation is run before executing the iteration logic so that exceptions can be caught early.

This logic is also available as a [function](#failfast).

```python
from ebbe.decorators import fail_fast

def hellraiser(n):
  if n > 10:
    raise TypeError

  yield from range(n)

# This will not raise until you consume `gen`
gen = hellraiser(15)

@fail_fast()
def hellraiser(n):
  if n > 10:
    raise TypeError

  yield from range(n)

# This will raise immediately
gen = hellraiser(15)
```

### decorators.with_defer

Decorates a function calling it with a `defer` kwarg working a bit like Go's [defer statement](https://gobyexample.com/defer) so that you can "defer" actions to be done by the end of the function or when an exception is raised to cleanup or tear down things.

This relies on an [ExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack) and can of course be also accomplished by context managers but this way of declaring things to defer can be useful sometimes to avoid nesting in complex functions.

```python
from ebbe.decorators import with_defer

@with_defer()
def main(content, *, defer):
  f = open('./output.txt', 'w')
  defer(f.close)

  f.write(content)
```

### Timer

Context manager printing the time (to stderr by default) it took to execute wrapped code. Very useful to run benchmarks.

```python
from ebbe import Timer

with Timer():
  some_costly_operation()
# Will print "Timer: ...s etc." on exit

# To display a custom message:
with Timer('my operation'):
  ...

# To print to stdout
import sys

with Timer(file=sys.stdout):
  ...
```
