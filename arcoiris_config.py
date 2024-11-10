import os

CHARACTER_SPACE = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
PASSWORD_SIZE = 6
HASH_SIZE = 10
TABLE_SIZE = 70000
CHAIN_SIZE = 400

DIR = "arcoiris"
NAME = f"password_size-{PASSWORD_SIZE} | hash_size-{HASH_SIZE} | table_size-{TABLE_SIZE} | chain_size-{CHAIN_SIZE}.json"
PATH = os.path.join(DIR, NAME)