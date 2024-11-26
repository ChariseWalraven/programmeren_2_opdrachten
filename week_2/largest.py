import time as t


def read_numbers_lc(filename):
    with open(filename) as f:
        return [int(line) for line in f.read().split('\n')]


def read_numbers_gc(filename):
    with open(filename) as f:
        return (int(line) for line in f.read().split('\n'))

duration_unit = 'μs (microseconds)'
multiplier = 1_000_000

start_time = t.time()
numbers = read_numbers_lc('numbers.txt')
lc_duration = (t.time() - start_time) * multiplier

start_time = t.time()
numbers = read_numbers_gc('numbers.txt')
gc_duration = (t.time() - start_time) * multiplier

print(f'duration with list comprehension: {lc_duration} {duration_unit}',
      f'duration with generator comprehension: {gc_duration} {duration_unit}',
      f'difference {lc_duration - gc_duration} {duration_unit}',
      f'list comprehension took longer than generator comprehension? {lc_duration > gc_duration}',
      sep='\n', )

print(max(numbers))
