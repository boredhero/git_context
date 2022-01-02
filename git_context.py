import bios
import sys
import os

HOME = os.path.expanduser('~')

def main():
    args = sys.argv
    print(args)
    if len(args) == 1:
        gc_help()
        exit(0)
    elif len(args) == 3 and args[1] == "help":
        gc_help()
        exit(0)
    elif len(args) == 3 and args[1] == "list":
        gc_list()
        exit(0)
    elif args[1] == "create":
        if len(args) < 6:
            print("More args required for git create")
            exit(0)
        else:
            gc_create(args)
            exit(0)
    else:
        gc_help()
        exit(0)
def gc_list():
    data = read_data()
    if data["Contexts"] is None:
        print("There are currently no contexts. To see how to get started, see 'git_context help'\n")
    else:
        print("Context Data:\n")
        print(data)
        exit(0)
def gc_add(args):
    username = args[2]
    email = args[3]
    key_type = args[4]
    filepath = args[5]
    if key_type != "ed25519" and key_type != "rsa":
        print(f"Error: git-context add: Key types ed25519 and rsa are valid, you entered {key_type}")
        exit(1)
    if username is None or username is "" or username is " ":
        print("Error: git-context add: You did not specify a git username. Aborting.")
        exit(1)
    if email is None or email is "" or email is " ":
        print("Error: git-context add: You did not specify an email. Aborting.")
        exit(1)
    if filepath is None or filepath is "" or filepath is " ":
        print("Error: git-context add: You did not specify a file path. Aborting.")
        exit(1)
    if os.path.isfile(filepath) is False:
        print(f"Error: git-context add: Unable to find specified keyfile ('{filepath}'). Aborting.")
        exit(1)
    # If we've passed all these checks, we're clear to add it to our data storage
    data = read_data()
    data["Contexts"][username] = {"email": email, "key_type": key_type, "username": username, "filename": filepath}
    write_data(data)
    exit(0)
def gc_create(args):
    username = args[2]
    email = args[3]
    key_type = args[4]
    filename = generate_ssh_keypair(email, key_type)
    if filename is None:
        print("Error creating keys for git-context create. Aborting. Please manually create keys and use git-context add")
        exit(1)
    else:
        data = read_data()
        data["Contexts"][username] = {"email": email, "key_type": key_type, "username": username, "filename": filename}
        write_data(data)
    return
def gc_delete(args):
    pass
def gc_get(args):
    pass
def gc_set(args):
    pass
def gc_clone(args):
    pass
def gc_help(args):
    try:
        paths = read_global_paths()
        info = bios.read(paths["info_path"], file_type="yaml")
        help_file = open(paths["man_path"], "r")
        help_text = help_file.read()
        print(f"{info['pretty_name']} - v{info['version']} '{info['version_nickname']}' by {info['author']}\n")
        print(help_text)
        help_file.close()
        return
    except Exception as e:
        print("An exception occured while trying to print help. Please report this at https:/github.com/boredhero/git_context\n Stacktrace:\n")
        print(e)
        path = os.getcwd()
        print(f"Current Working Directory: {path}")
        exit(1)

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
        exit(1)
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
            exit(1)
    except Exception as e:
        print("An unknown error occured\n Stacktrace: \n")
        print(e)
        exit(1)

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
            exit(1)
    try:
        paths = read_global_paths()
        bios.write(paths["data_path"], d, file_type="yaml")
        return
    except Exception as e:
        print("An unknown error occured while trying to write data\n Stacktrace: \n")
        print(e)
        exit(1)

def generate_ssh_keypair(email, key_type="ed25519"):
    """
    :param str email:
    :param str key_type: Must be "ed25519" or "rsa"

    :returns: str (filename) if successful, False otherwise
    """
    ssh_path = os.path.join(HOME, ".ssh")
    filenames = next(os.walk(ssh_path), (None, None, []))[2]
    # Input Section
    password = ask_password()
    if password is None:
        password = ""
    filename = input("Please enter a filename for your key (no spaces or special chars):")
    if filename == "" or filename == " ":
        res = generate_ssh_keypair(email, password, key_type)
        return res
    # End Input section
    if filename in filenames:
        print(f"WARNING: INVALID FILENAME!\nYour filename '{filename}' already exists in ~/.ssh/")
        print("Please choose a filename that is not among the followling list\n")
        print(filenames + "\n")
        filename = input("Please enter a new filename: ")
        res = generate_ssh_keypair(email, password, filename, key_type)
        return res
    if key_type == "ed25519":
        cmd = f'ssh-keygen -t ed25519 -C "{email}" -N "{password}" -f ~/.ssh/{filename} <<<y'
        print(f"Attempting to execute: {cmd}")
        try:
            stream = os.popen(cmd)
            output = stream.read()
            print(output)
            return filename
        except Exception as e:
            print("An error occured trying to create ed25519 key. Please manually create a key and use git-context add to create this profile.\nStacktrace:\n")
            print(e)
            return False
    elif key_type == "rsa":
        cmd = f'ssh-keygen -t rsa -b 4096 -C "{email}" -N "{password}" -f ~/.ssh/{filename} <<<y'
        print(f"Attempting to execute: {cmd}")
        try:
            stream = os.popen(cmd)
            output = stream.read()
            print(output)
            return filename
        except Exception as e:
            print("An error occured trying to create rsa key. Please manually create a key and use git-context add to create this profile.\nStacktrace:\n")
            print(e)
            return False
    else:
        print(f"Error: Key type must be 'ed25519' or 'rsa'. Passed '{key_type}' instead.\nPlease generate your own SSH keys and add them with 'git_context add'")
        return False

def ask_password():
    y_n = input("Would you like a password? (Yy/Nn): ")
    if y_n == "" or y_n == " " or y_n == "N" or y_n == "n" or y_n == "No" or y_n == "no":
        return None
    elif y_n == "Y" or y_n == "y" or y_n == "Yes" or y_n == "yes":
        password = input("Please enter a password: ")
        return password
    else:
        print("Error: Invalid input to Y/N Question")
        password = ask_password()
        return password

if __name__ == "__main__":
    main()