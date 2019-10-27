import logging
import os
import random

small_letters = 'abcdefghijklmnopqrstuvwxyz'
big_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '1234567890'
signs = '~`!@#$%^&*()_+=-[]{}|\\"\'/?.,<>'


def password_generator(length, groups=(small_letters, big_letters, numbers, signs)):
    if length < len(groups):
        raise Exception('Password can not be shorter than list of groups')

    alphabet = ''.join(groups)

    while True:
        password = ''.join(random.choices(alphabet, k=length))
        password_set = set(password)
        if all([set(group).intersection(password_set) for group in groups]):
            return password


def configure_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=os.path.expanduser('~/.copter/stdout.log'),
                        filemode='w+')


if __name__ == '__main__':
    print(password_generator(20))

