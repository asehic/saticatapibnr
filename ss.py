# Shared State local implementation using files

import os, pickle

global_dictionary = {}
folder_path = '.ss'

def put(key, value):
    global global_dictionary, folder_path
    global_dictionary[key] = value
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(folder_path + '/' + key, 'wb') as pickle_file:
        pickle.dump(value, pickle_file)

def get(key):
    global global_dictionary, folder_path
    if key in global_dictionary:
        value = global_dictionary[key]
    else:
        with open(folder_path + '/' + key, 'rb') as pickle_file:
            value = pickle.load(pickle_file)
            global_dictionary[key] = value
    return value