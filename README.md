[![Build Status](https://github.com/Yomguithereal/ebbe/workflows/Tests/badge.svg)](https://github.com/Yomguithereal/ebbe/actions)

# Ebbe

A collection of iterator-related functions for python that cannot be found in the however great `itertools` package.

## Installation

You can install `ebbe` with pip with the following command:

```
pip install ebbe
```

## Usage

*Functions*

* [as_chunks](#aschunks)
* [fail_fast](#failfast)
* [uniq](#uniq)
* [with_prev](#withprev)
* [with_next](#withnext)
* [with_is_first](#withisfirst)
* [with_is_last](#withislast)
* [without_first](#withoutfirst)

*Decorators*

* [decorators.fail_fast](#failfastdecorator)

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

@fail_fast
def hellraiser(n):
  if n > 10:
    raise TypeError

  yield from range(n)

# This will raise immediately
gen = hellraiser(15)
```
