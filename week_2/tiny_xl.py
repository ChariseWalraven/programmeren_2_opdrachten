# hardcoded csv location
# kiss!
# minimal libraries - can use os
from collections.abc import Callable
from typing import TextIO


csv_location = './data/MOCK_DATA.csv'


def remove_empty_rows(csv_iter: list[dict]) -> list[dict]:
    return list(filter(lambda row: row['id'] != '', csv_iter))


def call_method(
        csv_iter: list[dict],
        col: str, method_key: str,
        method_args: list | None = None,
) -> str:
    (method, is_aggregation) = get_method_by_key(method_key)
    res = str(method([int(row[col]) for row in csv_iter]) \
        if is_aggregation \
        else method(csv_iter, *method_args))
    return res


def get_method_by_key(method_key: str) -> tuple[Callable, bool]:
    methods = {
        'sum': (sum, True),
        'avg': (lambda lst: sum(lst) / len(lst), True),
        'add': (write_row_to_csv, False),
    }

    return methods[method_key]


def get_file_content(location: str = './data/MOCK_DATA.csv') -> tuple[str, TextIO]:
    """
    Reads and returns content from file on disk.
    :param location: url to location of (csv) file, defaults to ``'./data/MOCK_DATA.csv'``
    :return: file content
    """
    f = open(location, 'r+')
    return f.read(), f


def parse_csv(file_contents: str, row_delimiter: str = '\n', col_delimiter: str = ',') -> list[dict]:
    """
    Parses csv and returns results as a list with dicts representing the data
    :param file_contents: the file contents as a string, e.g. from the ``.read()`` method of the result of ``open()``
    :param row_delimiter: the character used to separate rows in the csv, defaults to ``'\n'`` (newline)
    :param col_delimiter: the character used to separate columns in the csv, defaults to ``','`` (comma)
    :return: list of dict objects representing rows in csv with headers as keys and cell content as values
    """
    rows = [str_row.split(col_delimiter) for str_row in file_contents.split(row_delimiter)]
    header_row = rows[0]
    content_rows = rows[1::]

    return [dict(zip(header_row, c_row)) for c_row in content_rows]


def write_row_to_csv(user_input_row: str, f: TextIO):
    f.write(user_input_row)


def get_row_dict(csv_iter, row_to_add):
    headers = csv_iter[0].keys()
    row_to_add = dict(zip(headers, row_to_add.split(',')))
    return row_to_add


def get_calculation_and_args() -> tuple[str, str | None]:
    calculation = input('Please choose a calculation:')

    calculation_list = calculation.split(' ')

    calculation_key = calculation_list[0].lower()
    # get arguments if they exist
    calculation_args = ' '.join(calculation_list[1::])

    return calculation_key, calculation_args


def get_col_name(method_key: str):
    (method, is_aggregate) = get_method_by_key(method_key)
    if is_aggregate:
        return input('Please choose a column name:')
    return


def load_csv(location: str = './data/MOCK_DATA.csv') -> tuple[list[dict], TextIO]:
    """
    Reads and returns csv at ``location`` from disk
    :param location: url to location of csv file, defaults to ``'./data/MOCK_DATA.csv'``
    :return: list of dict objects representing rows in csv with headers as keys and cell content as values
    """
    # load csv file from disk
    # print how many rows and columns the csv has
    file_content, csv_file = get_file_content(location)
    csv_iter = remove_empty_rows(parse_csv(file_content))
    num_rows = len(csv_iter)
    num_cols = len(csv_iter[0])
    print(f'{num_cols} columns and {num_rows} rows loaded')
    return csv_iter, csv_file

def output_result(method_key: str, col:str, result: str) -> None:
    if get_method_by_key(method_key)[1]:
        print(f'The {method_key} of {col}: {result}')
    else:
        print(result)



if __name__ == '__main__':
    csv, csv_f = load_csv()
    key, args = get_calculation_and_args()
    col_name = get_col_name(key)

    method_result = call_method(csv, col_name, key, [args, csv_f])

    output_result(key, col_name, method_result)
