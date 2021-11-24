import sys
from xml.dom.minidom import parseString

def main():
    args = sys.argv
    if len(args) == 1:
        help()
        exit()

def gc_list():
    pass
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
        help_file = open("man.txt", "r")
        help_text = help_file.read()
        print("\n")
        print(help_text)
        help_file.close()
    except Exception as e:
        print("An exception occured while trying to print help. Please report this at https:/github.com/boredhero/git_context\n Stacktrace:\n")
        print(e)

if __name__ == "__main__":
    main()