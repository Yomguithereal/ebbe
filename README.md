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
* [fail_fast](#fail_fast)
* [uniq](#uniq)
* [with_prev](#with_prev)
* [with_prev_and_next](#with_prev_and_next)
* [with_next](#with_next)
* [with_is_first](#with_is_first)
* [with_is_last](#with_is_last)
* [without_first](#without_first)

*Utilities*

* [getpath](#getpath)
* [pathgetter](#pathgetter)
* [noop](#noop)
* [sorted_uniq](#sorted_uniq)

*Decorators*

* [decorators.fail_fast](#decoratorsfail_fast)
* [decorators.with_defer](#with_defer)

### as_chunks

Iterate over chunks of the desired size by grouping items as we iterate over them.

```python
import ebbe

list(ebbe.as_chunks(3, [1, 2, 3, 4, 5]))
>>> [[1, 2, 3], [4, 5]]
```

### fail_fast

Take an iterable (but this has been geared towards generators, mostly), and tries to access the first value to see if an Exception will be raised before returning an equivalent iterator.

This is useful with some badly-conceived generators that checks arguments and raise if they are not valid, for instance, and if you don't want to wrap the whole iteration block within a try/except.

This logic is also available as a [decorator](#failfastdecorator).

```python
import ebbe

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

Filter repeated items seen next to each other in the given iterator.

```python
import ebbe

list(ebbe.uniq([1, 1, 1, 2, 3, 4, 4, 5, 5, 6]))
>>> [1, 2, 3, 4, 5, 6]

# BEWARE: it does not try to remember items (like the `uniq` command)
list(ebbe.uniq([1, 2, 2, 3, 2]))
>>> [1, 2, 3, 2]
```

### with_prev

Iterate over items along with the previous one.

```python
import ebbe

for previous_item, item in ebbe.with_prev(iterable):
  print(previous_item, 'came before', item)

list(ebbe.with_prev([1, 2, 3]))
>>> [(None, 1), (1, 2), (2, 3)]
```

### with_prev_and_next

Iterate over items along with the previous and the next one.

```python
import ebbe

for previous_item, item, next_item in ebbe.with_prev_and_next(iterable):
  print(previous_item, 'came before', item)
  print(next_item, 'will come after', item)

list(ebbe.with_prev_and_next([1, 2, 3]))
>>> [(None, 1, 2), (1, 2, 3), (2, 3, None)]
```

### with_next

Iterate over items along with the next one.

```python
import ebbe

for item, next_item in ebbe.with_next(iterable):
  print(next_item, 'will come after', item)

list(ebbe.with_next([1, 2, 3]))
>>> [(1, 2), (2, 3), (3, None)]
```

### with_is_first

Iterate over items along with the information that the current item is the first one or not.

```python
import ebbe

for is_first, item in ebbe.with_is_first(iterable):
  if is_first:
    print(item, 'is first')
  else:
    print(item, 'is not first')

list(ebbe.with_is_first([1, 2, 3]))
>>> [(True, 1), (False, 2), (False, 3)]
```

### with_is_last

Iterate over items along with the information that the current item is the last one or not.

```python
import ebbe

for is_last, item in ebbe.with_is_last(iterable):
  if is_last:
    print(item, 'is last')
  else:
    print(item, 'is not last')

list(ebbe.with_is_last([1, 2, 3]))
>>> [(False, 1), (False, 2), (True, 3)]
```

### without_first

Iterate over the given iterator after skipping its first item. Can be useful if you want to skip headers of a CSV file for instance.

```python
import ebbe

list(ebbe.without_first([1, 2, 3]))
>>> [2, 3]

for row in ebbe.without_first(csv.reader(f)):
  print(row)
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

### noop

Noop function (a function that can be called with any arguments and does nothing). Useful as a default to avoid complicating code sometimes.

```python
from ebbe import noop

noop() # Does nothing...
noop(4, 5) # Still does nothing...
noop(4, index=65) # Nothing yet again...
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
