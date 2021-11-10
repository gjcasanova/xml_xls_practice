import pandas as pd
import numpy as np
import xml.etree.cElementTree as ET
import pathlib

directory_path = pathlib.Path().resolve().absolute()


def read_excel(relative_path):
    file_path = directory_path.joinpath(relative_path)
    dataframe = pd.read_excel(file_path, sheet_name='grades')
    dataframe['total_grade'] = np.mean(dataframe[['grade_1', 'grade_2', 'grade_3']], axis=1)

    conditions = [
        ((dataframe['total_grade'] >= 0) & (dataframe['total_grade'] < 5)),
        ((dataframe['total_grade'] >= 5) & (dataframe['total_grade'] < 7)),
        ((dataframe['total_grade'] >= 7) & (dataframe['total_grade'] <= 10))
    ]

    choices = ['reprobate', 'extension', 'approved']

    dataframe['veredict'] = np.select(conditions, choices, default='error')

    write_excel(dataframe, 'xls/grades.xlsx', 'final_report')

    return dataframe


def write_excel(dataframe, relative_path, sheet_name):

    file_path = directory_path.joinpath(relative_path)
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        dataframe.to_excel(writer, sheet_name='final_report', index=False)


def read_xml():
    pass


def write_xml(tree, relative_path):
    file_path = directory_path.joinpath(relative_path)
    tree.write(file_path, encoding='utf8', xml_declaration=True)


def generate_xml(dataframe):
    root = ET.Element('root')
    students = ET.SubElement(root, 'students')

    for it in dataframe.index:
        student = ET.SubElement(students, 'student')
        student.set('id', str(dataframe['id'][it]))
        name = ET.SubElement(student, 'name')
        name.text = f"{dataframe['first_name'][it]} {dataframe['last_name'][it]}"

        grades = ET.SubElement(student, 'grades')

        for i in range(1, 4):
            ET.SubElement(grades, 'grade').text = str(dataframe[f'grade_{i}'][it])

        ET.SubElement(grades, 'final_grade').text = str(dataframe['total_grade'][it])
        ET.SubElement(grades, 'veredict').text = str(dataframe['veredict'][it])

    tree = ET.ElementTree(root)
    write_xml(tree, 'xml/grades.xml')


def main():
    grades_dataframe = read_excel('xls/grades.xlsx')
    generate_xml(grades_dataframe)


if __name__ == '__main__':
    main()
