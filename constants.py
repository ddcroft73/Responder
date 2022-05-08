#constants.py

from os.path import(
    dirname as os_dirname,
    realpath as os_realpath,
    join as os_join
)

# Hardcoded  access to Tizzle: DONT FORGET TO SET UP THE CONSTANTS TO POINT TO TIZZLE
TIZZLE_DIR:  str = r'C:\projects\python\Tizzle'
TIZZLE_PROG: str = 'tizz.py'

TIZZLE:      str = os_join(TIZZLE_DIR, TIZZLE_PROG)
DB_DIR:      str = 'db'
# access to the messages database
DB:          str = os_join(TIZZLE_DIR, DB_DIR, "message_db.json")


PROG_NAME: str = 'main.py'
SETTINGS:  str = 'settings.json'
LOG:       str = 'responder.log'
PROG_DIR:  str = os_dirname(os_realpath(__file__))                                 # == ./responder
MAIN_DIR:  str = '\\'.join(PROG_DIR.split('\\'))[:-len(PROG_DIR.split('\\')[-1])]  # == The parent(main) directory of the entire application.

SET_FILE:  str = os_join(PROG_DIR, SETTINGS)
LOG_FILE:  str = os_join(PROG_DIR, LOG)



# File Constants for meddling with the message Database
SUCCESS:   int = 0
STATUS:    int = 7
ID:        int = 0

WAIT_TIME: int = 60*5  # debug Normal is 60*3 

#print(f'{MAIN_DIR = }\n {TIZZLE = }\n {PROG_DIR = }\n {SET_FILE = }\n {LOG_FILE = }\n' )