# hardcoded csv location
# kiss!
# minimal libraries - can use os
from collections.abc import Callable

csv_location =  './data/MOCK_DATA.csv'

def remove_empty_rows(csv_iter: list[dict]) -> list[dict]:
    return list(filter(lambda row: row['id'] != '', csv_iter))


def perform_aggregation(col: str, aggregation_method: str, csv_iter: list[dict]) -> int:
    method = get_aggregation_method(aggregation_method)
    res = 0
    # get all values in col

    return method([int(row[col]) for row in csv_iter])

def get_aggregation_method(key: str) -> Callable:
    return {'sum': sum, 'avg': lambda lst: sum(lst)/len(lst)}[key]

def get_file_content(location: str = './data/MOCK_DATA.csv') -> str:
    """
    Reads and returns content from file on disk.
    :param location: url to location of (csv) file, defaults to ``'./data/MOCK_DATA.csv'``
    :return: file content
    """
    f = open(location)
    return f.read()


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


def get_user_calculation_choice() -> tuple[str, str]:
    col = input('Please choose a column name:')
    calculation_key = input('Please choose a calculation:').lower()

    return col, calculation_key


def load_csv(location: str = './data/MOCK_DATA.csv') -> list[dict]:
    """
    Reads and returns csv at ``location`` from disk
    :param location: url to location of csv file, defaults to ``'./data/MOCK_DATA.csv'``
    :return: list of dict objects representing rows in csv with headers as keys and cell content as values
    """
    # load csv file from disk
    # print how many rows and columns the csv has
    csv_iter = remove_empty_rows(parse_csv(get_file_content(location)))
    num_rows = len(csv_iter)
    num_cols = len(csv_iter[0])
    print(f'{num_cols} columns and {num_rows} rows loaded')
    return csv_iter


if __name__ == '__main__':
    csv = load_csv()
    col_name, agg_meth = get_user_calculation_choice()
    print(perform_aggregation(col_name, agg_meth, csv))

