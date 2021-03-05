[![Build Status](https://github.com/Yomguithereal/ebbe/workflows/Tests/badge.svg)](https://github.com/Yomguithereal/ebbe/actions)

# Ebbe

A collection of iterator-related functions for python that cannot be found in the however great `itertools` package.

## Installation

You can install `ebbe` with pip with the following command:

```
pip install ebbe
```

## Usage

* [as_chunks](#aschunks)
* [uniq](#uniq)
* [with_prev](#withprev)
* [with_next](#withnext)
* [with_is_first](#withisfirst)
* [with_is_last](#withislast)

### as_chunks

Iterate over chunks of the desired size by grouping items as we iterate over them.

```python
import ebbe

list(ebbe.as_chunks(3, [1, 2, 3, 4, 5]))
>>> [[1, 2, 3], [4, 5]]
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
