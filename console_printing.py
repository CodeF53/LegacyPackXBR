import os
import shutil
import sys

term_size = shutil.get_terminal_size()[0] - 1


def remove_lines(num_lines):
    for i in range(num_lines):
        remove_line()


def remove_line():
    os.system('')
    sys.stdout.write("\033[F")
    print(" " * term_size)
    os.system('')
    sys.stdout.write("\033[F")


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(ctr(f'{prefix} |{bar}| '))
    print(ctr(f'{percent}% {suffix}'))
    # Print New Line on Complete
    if iteration == total:
        print()


def ctrs(string, string2):
    return string.center(term_size, ' ').replace(string, string2)


def ctr(string):
    return string.center(term_size, ' ')


def ral(string):
    return string.rjust(term_size, ' ')
