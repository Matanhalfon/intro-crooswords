###################################
# ex5.py
# matan halfon,matan.halfon,205680648
# Omri Yavne, omri.yavne, 316520097
# intro2cs ex5 2017-2018
# Describe : A program that find word in a 3d crossword accordingly to direaction input
###################################

import crossword as CR
import sys
import os

# global variables

DETH_SEARCH = 'a'
LENGTH_SEARCH = 'b'
WIDTH_SEARCH = 'c'
DIRECTION = ['a', 'b', 'c']
DELIMETER = '***'
ALL_DIRECTION = 'rludzwxy'
MAT_ERROR = "ERROR: Matrix file mat.txt does not exist."
WORD_LIST_ERROR = "ERROR: Word file word_list.txt does not exist"
PARAMETERS_ERROR = "ERROR: invalid number of parameters. \
Please enter word_file matrix_file output_file directions"
DIRECTION_ERROR = "ERROR: invalid directions"

def direction_cheake(string):
    "A function that cheaks if the direction parameter are legal"
    DIRECTION = ['a','b','c']
    string_list = []
    for i in string:
        string_list.append(i)
    for i in range(len(string_list)):
        if string_list[i] not in DIRECTION:
            return False
    return True

def d3_list(mat):
    '''A function that parses the 3d matrix into
    three lists, that we can work with'''
    mat_list = []
    d3_mat = []
    for line in mat:
        row = line.rstrip().replace(',', '').lower()
        mat_list.append(row)
    num_of_matrix = 1
    for string in mat_list:
        if string == DELIMETER:
            num_of_matrix += 1
    list1 = []
    for j in range(len(mat_list)):
        if mat_list[j] == mat_list[len(mat_list) - 1]:
            list1.append(list(mat_list[j]))
            d3_mat.append(list1[:])
        elif mat_list[j] != DELIMETER:
            list1.append(list(mat_list[j]))
        elif mat_list[j] == DELIMETER:
            d3_mat.append(list1[:])
            list1.clear()
    return d3_mat


def deep_search(d3_matrix, word_list):
    '''A function that does a deep searching
    for words in the three lists'''
    word_to_return = []
    for i in range(len(d3_matrix)):
        word_to_return.extend(CR.search_crossword(ALL_DIRECTION, d3_matrix[i], word_list))
    return word_to_return


def length_matrix_convert(d3_matrix):
    '''A function that converts the matrix
    into a length matrix'''
    new_matrix = []
    list1 = []
    for i in range(len(d3_matrix[0])):
        for j in range(len(d3_matrix)):
            list1.append(d3_matrix[j][i])
        new_matrix.append(list1[:])
        list1.clear()
    return new_matrix


def length_search(matrix, word_list):
    ''' A function that searches the words
    in the length matrix'''
    length_matrix = length_matrix_convert(matrix)
    return deep_search(length_matrix, word_list)


def width_matrix_convert(d3_matrix):
    ''' A function that converts the mat
    to a width matrix'''
    new_matrix = []
    list_row = []
    single_matrix = []
    for i in range(len(d3_matrix[0][0])):
        for j in range(len(d3_matrix)):
            for k in range(len(d3_matrix[0])):
                list_row.append(d3_matrix[j][k][i])
            single_matrix.append(list_row[:])
            list_row.clear()
        new_matrix.append(single_matrix[:])
        single_matrix.clear()
    return new_matrix


def width_search(matrix, word_list):
    ''' A function that searches for words
    in the width mat'''
    new_matrix = width_matrix_convert(matrix)
    return (deep_search(new_matrix, word_list))


def D3_search(direction, matrix_3d, word_list):
    ''' this function receives direction,
    a matrix and a words lists, and searches
    in all directions, for relevant words
    in the matrix'''
    word__from_search = []
    list_for_file = []
    if DETH_SEARCH in direction:
        word__from_search.extend(deep_search(matrix_3d, word_list))
    if LENGTH_SEARCH in direction:
        word__from_search.extend(length_search(matrix_3d, word_list))
    if WIDTH_SEARCH in direction:
        word__from_search.extend(width_search(matrix_3d, word_list))
    return CR.word_fix(word__from_search)


def main(word_path, mat_path, output_file, direction):
    ''' The main function that accesses a path
    and activates all the other functions'''
    if len(sys.argv) != 5:
        print(PARAMETERS_ERROR)
    elif not os.path.isfile(word_path):
        print(WORD_LIST_ERROR)
    elif not os.path.isfile(mat_path):
        print(MAT_ERROR)
    elif direction_cheake(direction)==False:
        print(DIRECTION_ERROR)
    else:
        d3_matrix = d3_list(open(mat_path))
        word_list = CR.open_words(open(word_path))
        words_to_return = CR.concat_list(D3_search(direction, d3_matrix, word_list))
        f = open(output_file, 'w')
        f.write(str(words_to_return))
        f.close()


if __name__ == '__main__':
    ''' In this function,
    the program is called from a terminal'''
    WORD_PATH = sys.argv[1]
    MATRIX_PATH = sys.argv[2]
    OUTPUT_PATH = sys.argv[3]
    DIRECTION = sys.argv[4]
    main(WORD_PATH, MATRIX_PATH, OUTPUT_PATH, DIRECTION)
