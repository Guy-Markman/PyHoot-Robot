"""Encrypter and removing data to the image
You have to move the picture to the directory encrypter to it to work"""
## @file encrypter/encrypter.py Enc

# WIP
import os


def main():

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
            raw_input("Only add or remove")


if __name__ == "__main__":
    main()
