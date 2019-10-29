###################################
# ex5.py
# matan halfon,matan.halfon,205680648
# Omri Yavne, omri.yavne, 316520097
# intro2cs ex5 2017-2018
# Describe : A program that find word in a 2d crossword accordingly to direaction input
###################################

import sys
import os

# some global variables

UP = 'u'
DOWN = 'd'
RIGHT = 'r'
LEFT = 'l'
DIAGO_up_left = 'x'
DIAGO_up_right = 'w'
DIAGO_down_right = 'y'
DIAGO_down_left = 'z'
MAT_ERROR = "ERROR: Matrix file mat.txt does not exist."
WORD_LIST_ERROR = "ERROR: Word file word_list.txt does not exist"
PARAMETERS_ERROR = "ERROR: invalid number of parameters. \
Please enter word_file matrix_file output_file directions"
DIRECTION_ERROR = "ERROR: invalid directions"


def direction_cheake(string):
    "A function that cheaks if the direction parameter are legal"
    DIRECTION = ['u', 'd', 'r', 'l', 'w', 'z', 'y', 'x']
    string_list = []
    for i in string:
        string_list.append(i)
    for i in range(len(string_list)):
        if string_list[i] not in DIRECTION:
            return False
    return True


def counting(lst):
    "A function that count word in a list and return the the word that \
     found and the number of times in a tuple"
    lst2 = []
    for word in lst:
        the_count = lst.count(word)
        tup = word, the_count
        if tup in lst2:
            continue
        else:
            lst2.append((word, the_count))
    return lst2


def rotete_90(mat):
    '''A function that rotates the matrix
    by 90 deg clockwith '''
    new_mat = []
    for i in range(len(mat[0])):
        new_mat.append([])
    for row in range(len(new_mat)):
        for j in range(len(mat)):
             new_mat[row].append(mat[j][-1 - row])
    return (new_mat)


def open_words(word_path):
    '''A function that accesses a file and parses
    the word to a list'''
    the_word_list = []
    for line in word_path:
        word = line.rstrip().lower()
        the_word_list.append(word)
    return the_word_list


def d2_list(mat):
    '''A function that accesses a path for a file of a matrix
    and parses the data to a list of lists of
    the rows and columns'''
    mat_list = []
    for line in mat:
        row = line.rstrip().replace(',', '').lower()
        mat_list.append(list(row))
    return mat_list


def concat_list(str_lst):
    '''A function that concat strings
     into a string'''
    sentence = ''
    for item in range(len(str_lst)):
        item = str(str_lst[item])
        sentence = sentence + item
    return (sentence)


def run_right(mat, word_list):
    '''A function that checks for each row
     of the matrix, if word a from the words list
     is in it'''
    word_that_found = []
    for word in word_list:
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if list(mat[i][j:j + len(word)]) == list(word):
                    word_that_found.append(word)
    return word_that_found


def run_up_to_down(mat, word_list):
    '''A function that rotates the matrix in 90 degrees
     and then uses "run right function,
     so that the direction of the word's searching
     is now up to down'''
    new_mat = rotete_90(mat)
    return run_right(new_mat, word_list)


def run_left_to_right(mat, word_list):
    '''A function that uses the rotation function,
    and run right function, to rotate the matrix
    in 180 degrees, so the direction is now
    from left to right'''
    new_mat = rotete_90(rotete_90(mat))
    return run_right(new_mat, word_list)


def run_down_to_up(mat, word_list):
    ''''A function that uses the rotation function,
    and run right function, to rotate the matrix
    in 270 degrees, so the direction is now
    from down to up'''
    new_mat = rotete_90(rotete_90(rotete_90(mat)))
    return run_right(new_mat, word_list)


def word_in_string(string, the_word):
    '''A function that checks if
    a word is in a string'''
    for j in range(len(string)):
        if list(string[j:j + len(the_word)]) == list(the_word):
            return True
    return False


def the_basic_cordination(mat):
    '''A function that find the basic cordintion of the matrix \
    exmple for 2 on 2 matrix:\
    output=(0,0),(1,0),(0,1)'''
    all_basic = []
    for i in range(len(mat)):
        all_basic.append([i, 0])
    for j in range(len(mat[i])):
        if [0, j] in all_basic:
            continue
        else:
            all_basic.append([0, j])
    return all_basic


def diagonal_run(mat, pair, word_list):
    '''A function that searches for words
      from words list, in the matrix in
      diagonal  '''
    row_LENTHE = len(mat)
    col_LENTHE = len(mat[0])
    right, down = (1, 1)
    letter_list = []
    letter_in_duble_list = []
    word_that_found = []
    col_index, row_index = pair
    [col_corn, row_corn] = pair
    for i in range(min(row_LENTHE - row_corn, col_LENTHE - col_corn)):
        letter_list.append(mat[row_index][col_index])
        row_index += right
        col_index += down
    letter_in_duble_list.append(letter_list)
    word_that_found.append(run_right(letter_in_duble_list, word_list))
    return word_that_found


def run_diagonal_down_right(mat, word_list):
    '''A function that searches for words
    from words list, in the direction of
    down right diagonal'''
    word_that_found = []
    word_no_blank = []
    word_to_return = []
    pair_list = the_basic_cordination(mat)
    for i in range(len(pair_list)):
        word_that_found.append(diagonal_run(mat, pair_list[i], word_list))
    for j in range(len(word_that_found)):
        if word_that_found[j] != [[]]:
            word_no_blank.append(word_that_found[j])
    for i in range(len(word_no_blank)):
        word_to_return.append(str(word_no_blank[i][0][0]))
    return word_to_return


def run_diagonal_left_down(mat, word_list):
    '''A function that uses the function for diagonal
        search, and the function for the rotation of
        the matrix(90 degrees) and searches for words
          from words list, in the matrix in
         the direction of left down diagonal'''
    new_mat = rotete_90(mat)
    return run_diagonal_down_right(new_mat, word_list)


def run_diagonal_up_left(mat, word_list):
    '''A function that uses the function for diagonal
        search, and the function for the rotation of
        the matrix(180 degrees) and searches for words
          from words list, in the matrix in
         the direction of left up diagonal'''
    new_mat = rotete_90(rotete_90(mat))
    return run_diagonal_down_right(new_mat, word_list)


def run_diagonal_up_right(mat, word_list):
    '''A function that uses the function for diagonal
        serach, and the function for the rotation of
        the matrix(270 degrees) and searches for words
          from words list, in the matrix in
         the direction of up right diagonal'''
    new_mat = rotete_90(rotete_90(rotete_90(mat)))
    return run_diagonal_down_right(new_mat, word_list)


def search_crossword(direction, matrix, word_list):
    '''A function that addes to a list
     accordingly to the relevant direction of
     the words from the words list, that were
     found in the matrix'''
    word__from_search = []
    if RIGHT in direction:
        word__from_search.extend(run_right(matrix, word_list))
    if LEFT in direction:
        word__from_search.extend(run_left_to_right(matrix, word_list))
    if DOWN in direction:
        word__from_search.extend(run_up_to_down(matrix, word_list))
    if UP in direction:
        word__from_search.extend(run_down_to_up(matrix, word_list))
    if DIAGO_down_left in direction:
        word__from_search.extend(run_diagonal_left_down(matrix, word_list))
    if DIAGO_up_left in direction:
        word__from_search.extend(run_diagonal_up_left(matrix, word_list))
    if DIAGO_down_right in direction:
        word__from_search.extend(run_diagonal_down_right(matrix, word_list))
    if DIAGO_up_right in direction:
        word__from_search.extend(run_diagonal_up_right(matrix, word_list))
    return word__from_search


def word_fix(word_from_search):
    '''A function that sorts the words alphabetically.
    In addition we separate the words to different
    rows, by using \n'''
    list_for_file = []
    word_count = counting(word_from_search)
    for i in range(len(word_count)):
        list_for_file.append(word_count[i][0] + ',' + str(word_count[i][1]) + "\n")
    list_for_file.sort()
    if len(list_for_file)!=0:
        list_for_file[-1]=list_for_file[-1].rstrip()
    return list_for_file


def main(word_path, mat_path, output_file, direction):
    '''the main function, that involves
        other functions. This recieves:
        words list path, a matrix path, a file that the words that
        have been found will go in to path, and the
        direction/directions of search in the matrix.
        In addition, we define here some error messages for
        invaild parameters'''
    if len(sys.argv) != 5:
        print(PARAMETERS_ERROR)
    elif not os.path.isfile(word_path):
        print(WORD_LIST_ERROR)
    elif not os.path.isfile(mat_path):
        print(MAT_ERROR)
    elif direction_cheake(direction) == False:
        print(DIRECTION_ERROR)
    else:
        mati = d2_list(open(mat_path))
        word_list = open_words(open(word_path))
        word_from_search=search_crossword(direction, mati, word_list)
        words_to_return = concat_list(word_fix(word_from_search))
        f = open(output_file, 'w')
        f.write(str(words_to_return))
        f.close()


# if __name__ == '__main__':
#     '''A function that activates the program
#     and is called from a terminal'''
#     WORD_PATH = sys.argv[1]
#     MATRIX_PATH = sys.argv[2]
#     OUTPUT_PATH = sys.argv[3]
#     DIRECTION = sys.argv[4]
#     main(WORD_PATH, MATRIX_PATH, OUTPUT_PATH, DIRECTION)
