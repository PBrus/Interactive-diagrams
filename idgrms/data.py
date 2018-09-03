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
    """
    Read a one-line file header.

    Parameters
    ----------
    filename : str
        The name (with a path if neccessary) of the file which contains
        columns with integers and floats separated by spaces. The file
        must begin with a one-line header. The header should describe
        each column and begin with a single '#' sign then a space and the
        rest of columns labels.

    Returns
    -------
    file_header : ndarray
        A 1D array which elements are unicode strings (labels of each column).
    """
    file_header = _read_file(filename, max_lines_number=1,
                             comment_mark="//", data_type=None)

    return file_header[1:]

def read_file_content(filename):
    """
    Read a content of a file without a header.

    Parameters
    ----------
    filename : str
        The name (with a path if neccessary) of the file which contains
        columns with integers and floats separated by spaces. The first
        column should contain integers (required by another functions),
        the rest of them - floats. The file must begin with a one-line
        header (see read_file_header() function).

    Returns
    -------
    file_content : ndarray
        A 2D array which elements are floats.
    """
    file_content = _read_file(filename)

    return file_content

def read_group_file(filename):
    """
    Read a content of a file.

    Parameters
    ----------
    filename : str
        The name (with a path if neccessary) of the file which contains
        one column with integers.

    Returns
    -------
    file_content : tuple
        A tuple which contains integers.
    """
    file_content = tuple(_read_file(filename, data_type=int))

    return file_content

def unique_columns_list(nested_lists):
    """
    Flatten the nested list (two levels) and leave unique elements.

    Parameters
    ----------
    nested_lists : list
        A list which contains sublists.

    Returns
    -------
    list
        A list with unique elements from sublists.
    """
    return [*{*[item for sublist in nested_lists for item in sublist]}]

def get_necessary_data_column(file_content, file_header, column_index):
    """
    Get a specific column from the ndarray object.

    Parameters
    ----------
    file_content : ndarray
        An array with floats values. The data should be read from a file.
    file_header : ndarray
        An array which stores a header from the file where file_content
        comes from.
    column_index : int
        Indicates which column to use.

    Returns
    -------
    tuple
        A tuple is made of the column index, the label of column
        and the column's data.
    """
    index = abs(column_index) - 1
    column_data = np.ma.array([])
    column_data = np.append(column_data, file_content[:,index:index+1])

    return column_index, file_header[index], column_data

def get_data(filename, columns_argument):
    """
    Get specific columns with data.

    Parameters
    ----------
    filename : str
        The name (with a path if neccessary) of the file which contains
        columns with integers and floats separated by spaces. The first
        column should contain integers (required by another functions),
        the rest of them - floats. The file must begin with a one-line
        header (see read_file_header() function).
    columns_argument : list
        A nested list which contains sublists. Each sublist is made of
        two integers. The numbers are indexes of columns to be used.

    Returns
    -------
    tuple
        A nested tuple contains subtuples. Each subtuple is made of
        the returned value by the get_necessary_data_column() function.
    """
    data = ()
    file_header = read_file_header(filename)
    file_content = read_file_content(filename)
    unique_columns = unique_columns_list(columns_argument)

    for column_index in unique_columns:
        data += (get_necessary_data_column(file_content, file_header,
                                           column_index),)

    return data

# if the --grp option is switched on, do this:
def get_points_numbers(filename):
    file_content = read_file_content(filename)

    return tuple(file_content[:,0:1].flatten().astype(int))

def get_single_group_data(filename, color_argument, points_numbers):
    indexes = ()
    file_content = read_group_file(filename)

    for number in file_content:
        indexes += (points_numbers.index(number),)

    return (indexes, color_argument)

def get_group_data(data_filename, group_arguments):
    group_data = ()
    points_numbers = get_points_numbers(data_filename)

    for group_argument in group_arguments:
        group_data += (get_single_group_data(*group_argument, points_numbers),)

    return group_data
