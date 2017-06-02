## @package PyHoot-Robot-extra.encrypter
# Encrypter and removing data to the image
# You have to move the picture to the directory encrypter to it to work
## @file encrpter/encrypter.py Implementation of @ref PyHoot-extra.encrypter

import os


def encrypt(picture):
    """Adding encrption to picture
    @param picture The picture we want to remove the encrption from"""
    while True:
        answer = raw_input(
            "Enter the answer. 'A', 'B', 'C' or 'D' only! ").upper()
        if answer in ["A", "B", "C", "D"]:
            break
        print "Invalid answer"

    fd = os.open(picture, os.O_RDWR | os.O_APPEND | os.O_BINARY)
    try:
        os.write(fd, answer)
    finally:
        os.close(fd)
    print "Added"


def remove_encyption(picture):
    """Removing encrption from picture
    @param picture The picture we want to remove the encrption from"""
    with open(picture, 'rb+') as fd:
        fd.seek(-1, os.SEEK_END)
        fd.truncate()


def main():
    """Main function"""

    ## The action we want to do (add or delete only)
    choice = ""
    while True:
        choice = raw_input(
            "Do you want to add or remove info? (add, remove) ").lower()
        if choice in ("add", "remove"):
            while True:

                ## The picture we will use, including extintion
                picture = raw_input(
                    "what picture do you want to %s info?" % choice)
                if os.path.isfile(picture):
                    if choice == "add":
                        encrypt(picture)
                    else:
                        remove_encyption(picture)
                    break
                else:
                    print "File not found"

            break
        else:
            raw_input("Only add or remove")


if __name__ == "__main__":
    main()
