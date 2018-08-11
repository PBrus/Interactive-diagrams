import numpy as np


def _read_file(filename, max_lines_number=None, comment_mark="#"):
    try:
        with open(filename, 'r') as file_descriptor:
            file_content = np.genfromtxt(
                file_descriptor, max_rows=max_lines_number,
                comments=comment_mark, dtype=None, encoding="utf-8")
    except FileNotFoundError:
        print("File {} doesn't exist!".format(filename))
        return

    return file_content

def read_file_header(filename):
    file_header = _read_file(filename, max_lines_number=1, comment_mark="//")

    return file_header[1:]

def read_file_content(filename):
    file_content = _read_file(filename)

    return file_content
