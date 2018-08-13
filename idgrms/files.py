import numpy as np


def _read_file(filename, max_lines_number=None,
               comment_mark="#", data_type=float):
    try:
        with open(filename, 'r') as file_descriptor:
            file_content = np.genfromtxt(
                file_descriptor, max_rows=max_lines_number,
                comments=comment_mark, dtype=data_type, encoding="utf-8")
    except FileNotFoundError:
        print("File {} doesn't exist!".format(filename))
        exit(1)

    return file_content

def read_file_header(filename):
    file_header = _read_file(filename, max_lines_number=1,
                             comment_mark="//", data_type=None)

    return file_header[1:]

def read_file_content(filename):
    file_content = _read_file(filename)

    return file_content

def unique_columns_list(nested_lists):
    return [*{*[int(item) for sublist in nested_lists for item in sublist]}]

def revert_negative_value(value):
    return value if value > 0 else -value

def get_necessary_data_column(file_content, file_header, column_index):
    index = revert_negative_value(column_index) - 1
    column_data = np.ma.array([])
    column_data = np.append(column_data, file_content[:,index:index+1])

    return column_index, file_header[index], column_data

def get_data(filename, columns_argument):
    data = ()
    file_header = read_file_header(filename)
    file_content = read_file_content(filename)
    unique_columns = unique_columns_list(columns_argument)

    for column_index in unique_columns:
        data += (get_necessary_data_column(file_content, file_header,
                                           column_index),)

    return data
