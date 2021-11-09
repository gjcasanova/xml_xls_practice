import pandas as pd
import xml.etree.ElementTree as ET
import pathlib

directory_path = pathlib.Path().resolve().absolute()


def read_xml():
    pass


def write_xml():
    pass


def read_xls(relative_path):
    file_path = directory_path.joinpath(relative_path)
    dataframe = pd.read_excel(file_path, sheet_name='grades')
    return dataframe


def write_xls():
    pass


def main():
    print(directory_path)
    dataframe = read_xls('xls/grades.xlsx')
    print(dataframe)


if __name__ == '__main__':
    main()
