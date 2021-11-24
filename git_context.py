import bios
import sys
import os

HOME = os.path.expanduser('~')

def main():
    args = sys.argv
    data = {"abc": 123}
    write_data(data)
    if len(args) == 1:
        gc_help()
        exit()
    elif len(args) == 3 and args[2] == "help":
        gc_help()
        exit()
    elif len(args) == 3 and args[2] == "list":
        gc_list()
        exit()
    else:
        gc_help()
        exit()
def gc_list():
    data = read_data()
    if data["Contexts"] is None:
        print("There are currently no contexts. To see how to get started, see 'git_context help'\n")
def gc_add():
    pass
def gc_create():
    pass
def gc_delete():
    pass
def gc_get():
    pass
def gc_set():
    pass
def gc_clone():
    pass
def gc_help():
    try:
        paths = read_global_paths()
        info = bios.read(paths["info_path"], file_type="yaml")
        help_file = open(paths["man_path"], "r")
        help_text = help_file.read()
        print(f"{info['pretty_name']} - v{info['version']} '{info['version_nickname']}' by {info['author']}\n")
        print(help_text)
        help_file.close()
    except Exception as e:
        print("An exception occured while trying to print help. Please report this at https:/github.com/boredhero/git_context\n Stacktrace:\n")
        print(e)
        path = os.getcwd()
        print(f"Current Working Directory: {path}")

## Util methods
def read_global_paths():
    '''
    Return global paths dictionary

    :returns: {}
    '''
    try:
        paths = bios.read(f"{HOME}/.git_context_global.yml", file_type="yaml")
        paths = dict(paths)
        return paths
    except Exception as e:
        print("An error occured trying to find ~/.git_context_global.yml file. Aborting.\nStacktrace: \n")
        print(e)
        exit()
def read_data():
    '''
    Return data as dictionary
    
    :returns: {}
    Will exit program if an error occured trying to create data.yml for the first time
    '''
    try:
        paths = read_global_paths()
        data = bios.read(paths["data_path"], file_type="yaml")
        data = dict(data)
        return data
    except FileNotFoundError:
        d = {"Contexts": None}
        try:
            paths = read_global_paths()
            bios.write(paths["data_path"], d, file_type="yaml")
            data = bios.read(paths["data_path"], file_type="yaml")
            return data
        except Exception as e:
            print("An unknown issue occured trying to write data.yml. Please report this at https://github.com/boredhero/git_context\n Stacktrace: \n")
            print(e)
            exit()
    except Exception as e:
        print("An unknown error occured\n Stacktrace: \n")
        print(e)
        exit

def write_data(d):
    '''
    Write Data

    :param dict d: Data dictionary to write
    '''
    if type(d) is not dict:
        try:
            d = dict(d)
        except Exception as e:
            print(e)
            exit()
    try:
        paths = read_global_paths()
        bios.write(paths["data_path"], d, file_type="yaml")
    except Exception as e:
        print("An unknown error occured while trying to write data\n Stacktrace: \n")
        print(e)
        exit()



if __name__ == "__main__":
    main()