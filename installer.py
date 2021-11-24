from gettext import install
import os
import shutil, bios

SRC_DIR = os.getcwd()
HOME = os.path.expanduser('~')
if SRC_DIR == HOME:
    print(f"WARNING! SRC_DIR: {SRC_DIR} and HOME: {HOME} are the same. This will likely cause problems!")

def main():
    print("Welcome to the Git Context install script! We will now attempt to install the program for you!")
    print(f"SRC_DIR: {SRC_DIR} HOME: {HOME}")
    install_git_context_global_yml()
    create_install_dir()
    copy_git_context()
    handle_bashrc_zshrc()

def install_git_context_global_yml():
    global_paths = {
        "install_folder_path": f"{os.path.join(HOME, '.git_context')}",
        "executable_path": f"{os.path.join(HOME, '.git_context/git_context.py')}",
        "info_path": f"{os.path.join(HOME, '.git_context/info.yml')}",
        "data_path": f"{os.path.join(HOME, '.git_context/data.yml')}",
        "man_path": f"{os.path.join(HOME, '.git_context/man.txt')}"
    }
    write_path = os.path.join(HOME, ".git_context_global.yml")
    try:
        bios.write(write_path, global_paths, file_type="yaml")
        print("Installed ~/.git_context_global.yml")
        return
    except Exception as e:
        print("An unknown issue occured trying to create ~/.git_context_global.yml\nStacktrace:\n")
        print(e)
        return

def create_install_dir():
    install_dir_path = os.path.join(HOME, ".git_context")
    try:
        os.makedirs(install_dir_path, exist_ok=True)
        print("Created install directory ~/.git_context successfully!")
        return
    except Exception as e:
        print("An unknown error occured while trying to create install dir. Check your permissions!\nStacktrace:\n")
        print(e)
        exit()

def copy_git_context():
    try:
        install_dir_path = os.path.join(HOME, ".git_context")
        shutil.copy2(os.path.join(SRC_DIR, "git_context.py"), install_dir_path)
        shutil.copy2(os.path.join(SRC_DIR, "info.yml"), install_dir_path)
        shutil.copy2(os.path.join(SRC_DIR, "man.txt"), install_dir_path)
        shutil.copy2(os.path.join(SRC_DIR, "data.yml"), install_dir_path)
        shutil.copy2(os.path.join(SRC_DIR, "LICENSE"), install_dir_path)
        shutil.copy2(os.path.join(SRC_DIR, "README.md"), install_dir_path)
        shutil.copy2(os.path.join(SRC_DIR, "requirements.txt"), install_dir_path)
        print("Successfully installed program files in ~/.git_context!")
        return
    except Exception as e:
        print("An unknown exception occured trying to copy files to install directory! Check file permissions! Aborting.\nStacktrace:\n")
        print(e)
        exit()

def handle_bashrc_zshrc():
    bashrc_path = os.path.join(HOME, ".bashrc")
    zshrc_path = os.path.join(HOME, ".zshrc")
    bashrc_exists = os.path.exists(bashrc_path)
    zshrc_exists = os.path.exists(zshrc_path)
    if bashrc_exists:
        pass
    if zshrc_exists:
        pass
    if bashrc_exists == False and zshrc_exists == False:
        print("Unable to find a .bashrc or .zshrc file in your home directory, or you use a different shell")
        print('Please place: alias git-context="python3 $HOME/.git_context/git_context.py $pwd" or equivalent in your relevant rc file')
        return    


if __name__ == "__main__":
    main()