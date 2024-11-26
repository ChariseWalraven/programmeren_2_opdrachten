def read_numbers(filename):
    with open(filename) as f:
        return (int(line) for line in f.read().split('\n'))

numbers = read_numbers('numbers.txt')
print(max(numbers))
