from copy import deepcopy

from zad1.QuitError import QuitError


def manage_context(args, rtn=False):
    args_with_quit = deepcopy(args)
    args_with_quit.append("Quit")
    if rtn:
        args_with_quit.insert(len(args_with_quit) - 1, "Return")
    for i, line in enumerate(args_with_quit):
        print(f"{i + 1}. {line}")
    while True:
        try:
            choice = int(input("Choose option: "))
            if choice == len(args_with_quit):
                raise QuitError("User used quit")
            return args_with_quit[choice - 1]
        except IndexError:
            print("Option does not exist! Choose again!")
        except ValueError:
            print("Enter a number!")
