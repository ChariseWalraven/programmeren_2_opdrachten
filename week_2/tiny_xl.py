# hardcoded csv location
# kiss!
# minimal libraries - can use os
csv_location =  './data/MOCK_DATA.csv'
f = open(csv_location)

contents = f.read()


def parse_csv(file_contents: str, row_delimiter: str = '\n', col_delimiter: str = ',') -> list[dict]:
    rows = [str_row.split(col_delimiter) for str_row in file_contents.split(row_delimiter)]
    header_row = rows[0]
    content_rows = rows[1::]

    return [dict(zip(header_row, c_row)) for c_row in content_rows]


print(parse_csv(contents))