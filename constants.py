#constants.py

from os.path import(
    dirname as os_dirname,
    realpath as os_realpath,
    join as os_join
)

# Hardcoded  access to Tizzle: DONT FORGET TO SET UP THis infromation!
TIZZLE_DIR:  str = r'C:\projects\python\Tizzle\src'
TIZZLE_MAIN_DIR: str = r'C:\projects\python\Tizzle'

TIZZLE_PROG: str = 'tizz.py'
TIZZLE:      str = os_join(TIZZLE_DIR, TIZZLE_PROG)
DB_DIR:      str = 'db'

PROG_NAME: str = 'main.py'
SETTINGS:  str = 'settings.json'
LOG:       str = 'responder.log'
PROG_DIR:  str = os_dirname(os_realpath(__file__))                                 # == ./responder
MAIN_DIR:  str = '\\'.join(PROG_DIR.split('\\'))[:-len(PROG_DIR.split('\\')[-1])]  # == The parent(main) directory of the entire application.

SET_FILE:  str = os_join(PROG_DIR, SETTINGS)
LOG_FILE:  str = os_join(PROG_DIR, LOG)

# access to the messages and contacts databases
DB:          str = os_join(TIZZLE_MAIN_DIR, DB_DIR, "message_db.json")
CONTACTS_DB: str = os_join(TIZZLE_MAIN_DIR, DB_DIR, "contacts.json")


# File Constants for meddling with the message Database
SUCCESS:   int = 0
STATUS:    int = 7
ID:        int = 0

# File Contstants to use with Contact Info
NAME:       int = 0
PHONE:      int = 1
PROVIDER:   int = 2
GROUP_NAME: int = 3
MSG_LIST:   int = 4

DESTINATION:int = 2

WAIT_TIME: int = 60*3 # debug Normal is 60*3 

#print(f'{MAIN_DIR = }\n {TIZZLE = }\n {PROG_DIR = }\n {SET_FILE = }\n {LOG_FILE = }\n' )