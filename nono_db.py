import os
import pickle

import nonogram

def get_db_dir():
    return os.getcwd() + '\\db\\'

def write_nonogram_to_db(nonogram):
    directory = get_db_dir()
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print('Не смог создать или найти папку')
        print(e)

    else:
        file_name = directory + str(nonogram.id) + '-' + nonogram.name + '.non'
        try:
            with open(file_name, 'wb') as f:
                pickle.dump(nonogram, f, 2)
            print('Nonogram {0} writen to db'.format(nonogram.name))
        except OSError as e:
            print('Не смог создать файл')
            print(e)

def get_file_name_from_id(id):
    dir = get_db_dir()
    names = get_file_names_all()
    for s in names:
        index = s.find('-')
        if index != -1:
            f_id = int(s[0:index])
            if id == f_id:
                return s
    return None


def get_nonogram_from_id(id):
    file_name = get_file_name_from_id(id)
    if file_name:
        file_name = get_db_dir() + file_name
        try:
            with open(file_name, 'rb') as f:
                nonogram = pickle.load(f)
                return nonogram
        except OSError as e:
            print('Не смог прочитать файл')
            print(e)
            return None
    else:
        return None

def get_nonogram_from_file_name(name):
    if file_name_is_in_db(name):
        full_name = get_db_dir() + name
        try:
            with open(full_name, 'rb') as f:
                nonogram = pickle.load(f)
                return nonogram
        except OSError as e:
            print('Не смог прочитать файл')
            print(e)
            return None

def file_name_is_in_db(name):
    names = get_file_names_all()
    for n in names:
        if n == name:
            return True
    return False

def get_file_names_all():
    dir = get_db_dir()
    names = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        names.extend(filenames)
    return names