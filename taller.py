import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import pathlib

directory_path = pathlib.Path().resolve().absolute()


def write_xml(tree, relative_path):  # Escribir xml
    file_path = directory_path.joinpath(relative_path)
    tree.write(file_path, encoding='utf8', xml_declaration=True)


def read_xls(relative_path):  # Leer excel
    # Extraer datos
    file_path = directory_path.joinpath(relative_path)
    dataframe = pd.read_excel(file_path, sheet_name='grades')

    # Calculamos el promedio y lo guardamos en la columna 'final_grade'
    dataframe['final_grade'] = np.mean(dataframe[['grade_1', 'grade_2', 'grade_3']], axis=1)

    # Asig. de datos bajo condiciones
    conditions = [
        ((dataframe['final_grade'] >= 0) & (dataframe['final_grade'] < 5)),
        ((dataframe['final_grade'] >= 5) & (dataframe['final_grade'] < 7)),
        ((dataframe['final_grade'] >= 7) & (dataframe['final_grade'] <= 10)),
    ]

    choices = [
        'reprobate', 'extension', 'approved'
    ]

    # Calculamos el veredicto de acuerdo a las condiciones y opciones anteriores
    dataframe['veredict'] = np.select(conditions, choices, default='error')

    # Guardamos los cambios
    write_xls(dataframe, 'xls/grades.xlsx', 'final_report')
    return dataframe


def write_xls(dataframe, relative_path, sheet_name):  # Escribir excel
    file_path = directory_path.joinpath(relative_path)
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)


def generate_xml(dataframe):  # Genera
    root = ET.Element('root')
    students = ET.SubElement(root, 'students')

    for it in dataframe.index:
        student = ET.SubElement(students, 'student')
        # Agregamos el atributo id en cada estudiante
        student.set('id', str(dataframe['id'][it]))

        name = ET.SubElement(student, 'name')
        name.text = f"{dataframe['first_name'][it]} {dataframe['last_name'][it]}"

        grades = ET.SubElement(student, 'grades')

        for i in range(1, 4):
            grade = ET.SubElement(grades, 'grade')
            grade.text = str(dataframe[f'grade_{i}'][it])

        ET.SubElement(grades, 'final_grade').text = str(dataframe['final_grade'][it])
        ET.SubElement(grades, 'veredict').text = str(dataframe['veredict'][it])

    tree = ET.ElementTree(root)
    write_xml(tree, 'xml/grades1.xml')


def main():
    dataframe = read_xls('xls/grades.xlsx')
    print(dataframe)
    generate_xml(dataframe)


if __name__ == '__main__':
    main()
