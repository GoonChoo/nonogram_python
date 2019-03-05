import ast
import urllib.request
import numpy as np

from nonogram import Nonogram
from nonogram import Header
import nono_db


def get_header_from_array(array):
    row = 0
    max_header_row_len = 0
    header = [[] for i in range(array.shape[0])]
    while row < array.shape[0]:
        column = 0
        while column < array.shape[1]:
            cell = array[row][column]
            column += 1
            cell_counter = 1
            while column < array.shape[1] and cell == array[row][column]:
                column += 1
                cell_counter += 1
            if cell:
                header[row].append(cell_counter)
        if max_header_row_len < len(header[row]):
            max_header_row_len = len(header[row])
        row += 1
    return header


def parse_nonogram(url):
    with urllib.request.urlopen(url) as f:
        # string_file = str(f.read())
        string_file = f.read().decode('utf-8')

        # find id
        index_start = string_file.find('''name="crossword_id" value="''')
        index_start = string_file.find('''value="''', index_start)
        index_start = string_file.find('''"''', index_start)
        index_end = string_file.find('''"''', index_start+1)
        str_id = string_file[index_start + 1:index_end]

        # find name
        index_start = string_file.find('''<title>''')
        index_start = string_file.find('''>''', index_start) + 1
        index_start = string_file.find('''«''', index_start) + 1
        index_end = string_file.find('''»''', index_start)
        str_name = string_file[index_start:index_end]

        # find data
        index_start = string_file.find('''var d=[[''')
        index_start = string_file.find('''[''', index_start)
        index_end = string_file.find(''';''', index_start)
        str_data = string_file[index_start:index_end]
    nono_data = ast.literal_eval(str_data)
    return int(str_id), str_name, nono_data


def save_nonogram_from_url(url):
    try:
        nono_id, nono_name, d = parse_nonogram(url)
    except Exception as e:
        # print('Ссылка не туда')
        print(e)
    else:
        columns_number = d[1][0] % d[1][3] + d[1][1] % d[1][3] - d[1][2] % d[1][3]  # ширина
        rows_number = d[2][0] % d[2][3] + d[2][1] % d[2][3] - d[2][2] % d[2][3]  # высота
        colors_number = d[3][0] % d[3][3] + d[3][1] % d[3][3] - d[3][2] % d[3][3]

        nono_answer = np.full((rows_number, columns_number), 0)
        # print('Columns number =', columns_number)
        # print('Rows number', rows_number)
        v = colors_number + 5
        black_rows_number = d[v][0] % d[v][3] * (d[v][0] % d[v][3]) + d[v][1] % d[v][3] * 2 + d[v][2] % d[v][3]
        decoder = d[v + 1]

        for x in range(v + 2, v + 1 + black_rows_number + 1):
            for v in range(d[x][0] - decoder[0] - 1, d[x][0] - decoder[0] + d[x][1] - decoder[1] - 1):
                nono_answer[d[x][3] - decoder[3] - 1][v] = d[x][2] - decoder[2]

        header_rows = get_header_from_array(nono_answer)
        header_columns = get_header_from_array(nono_answer.T)
        header = Header(header_rows, header_columns)
        nonogram = Nonogram(nono_id, nono_name, header, nono_answer)
        nono_db.write_nonogram_to_db(nonogram)


# url1 = 'https://www.nonograms.ru/nonograms/i/19419'
# url1 = 'https://www.nonograms.ru/nonograms/i/19421'


def parser():
    for i in range(20566, 20567):
        url = r'https://www.nonograms.ru/nonograms/i/' + str(i)
        save_nonogram_from_url(url)


parser()

# nono = Nonogram
# print('Nonogram ', end='')
# nono = nono_db.get_nonogram_from_id(19001)
# if nono:
#     print('load')
# else:
#     print('not load')
