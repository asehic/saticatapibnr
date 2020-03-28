# Shared State local implementation using files

import os, errno, pickle

global_dictionary = {}
folder_path = '.ss' # no trailing /

def put(key, value):
    global global_dictionary, folder_path
    global_dictionary[key] = value
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(folder_path + '/' + key, 'wb') as pickle_file:
        pickle.dump(value, pickle_file)

def get(key):
    global global_dictionary, folder_path
    if not os.path.exists(folder_path + '/' + key):
        try:
            del global_dictionary[key]
        except KeyError:
            pass
        value = None
    else:
        if key in global_dictionary:
            value = global_dictionary[key]
        else:
            with open(folder_path + '/' + key, 'rb') as pickle_file:
                value = pickle.load(pickle_file)
                global_dictionary[key] = value
    return value

def delete(key):
    global global_dictionary, folder_path
    try:
        del global_dictionary[key]
    except KeyError:
        pass
    try:
        os.remove(folder_path + '/' + key)
    except OSError as e:
        if e.errno != errno.ENOENT: # no such file or directory
            raise
    # if not os.listdir(folder_path):
    #     try:
    #         os.remove(folder_path)
    #     except OSError as e:
    #         if e.errno != errno.ENOENT: # no such file or directory
    #             raise