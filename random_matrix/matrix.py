from random import randint, choice
from xml.dom import minidom
import csv


def filling_rows():
    row=[]
    alphabet = 'abcdefghijklmnoprstqwvuxyz'
    for i in range(10):
        flag = randint(0,1)
        if flag == 0: row.append(randint(0,100))
        else:row.append(choice(alphabet))
    return row

def find_number_params():
    digits = get_digits()
    params = []
    for row in digits:
        max = row[0]
        min = row[0]
        sum = 0
        number = 0
        for c in row:
            if c >= max:
                max = c
            if c <= min:
                min = c
            sum += int(c)
            number += 1
        avg = sum/number
        params.append([max, min, avg])
    return params

def filling_matrix():
    matrix = []
    for i in range(10):
        matrix.append(filling_rows())
    return matrix

def write_txt_file():
    file = open("matrix.txt", "w")
    matrix = filling_matrix();
    for rows in matrix:
        for char in rows:
            try:
                file.write(char + ' ')
            except TypeError:
                tochar = str(char)
                file.write(tochar + ' ')
        file.write('\n')
    file.close()

def read_from_txt_file():
    file = open('matrix.txt','r')
    symbols_in_matrix = []
    for row in file:
        symbols_in_row = row.split(" ")
        symbols_in_matrix.append(symbols_in_row)
    file.close()
    return symbols_in_matrix

def get_letters():
    letters = []
    symbols = read_from_txt_file()
    for rows in symbols:
        letters_in_row = []
        for symbols in rows:
            try:
                char = int(symbols)
            except ValueError:
                char = symbols
                if char != '\n': letters_in_row.append(char)
                letters_in_row.sort()
        letters.append(letters_in_row)
    return letters

def get_digits():
    digits = []
    symbols = read_from_txt_file()
    for rows in symbols:
        digits_in_row = []
        for symbols in rows:
            try:
                char = int(symbols)
                digits_in_row.append(char)
            except ValueError:
                continue
        digits.append(digits_in_row)
    return digits

def write_csv():
    csv_file = open('data.csv','w')
    columns = ['max', 'min', 'avg']
    number_params = find_number_params()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(columns)
    for rows in number_params:
        csv_writer.writerow(rows)
    csv_file.close()

def write_xml():
    letters = get_letters()
    doc = minidom.Document()
    root = doc.createElement('letters_in_rows')
    doc.appendChild(root)
    for i in range(10):
        tagname = str(i+1)
        leaf = doc.createElement(tagname)
        text = doc.createTextNode("".join(letters[i]))
        leaf.appendChild(text)
        root.appendChild(leaf)
    xml_str = doc.toprettyxml(indent="  ")
    with open("letters.xml", "w") as f:
        f.write(xml_str)

if __name__ == "__main__":
    filling_rows()
    filling_matrix()
    write_txt_file()
    read_from_txt_file()
    get_digits()
    get_letters()
    find_number_params()
    write_xml()
    write_csv()

