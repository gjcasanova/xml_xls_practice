import pandas as pd
import xml.etree.ElementTree as ET
import pathlib

directory_path = pathlib.Path().resolve().absolute()


def read_excel(relative_path):
    file_path = directory_path.joinpath(relative_path)
    dataframe = pd.read_excel(file_path, sheet_name='grades')
    return dataframe


def write_excel():
    pass


def read_xml():
    pass


def write_xml():
    pass


def generate_xml(dataframe):
    root = ET.Element('root')
    students = ET.SubElement(root, 'students')

    for it in dataframe.index:
        student = ET.SubElement(students, 'student')
        name = ET.SubElement(student, 'name')
        name.text = f"{dataframe['first_name'][it]} {dataframe['first_name'][it]}"
        students.append(student)

        grades = ET.SubElement(student, 'grades')
        ET.SubElement(grades, 'grade').text = 'Hello'

    print(ET.tostring(root))


def main():
    grades_dataframe = read_excel('xls/grades.xlsx')
    generate_xml(grades_dataframe)


if __name__ == '__main__':
    main()
