# Database class to handle access to message and contacts info


from json import(
    load as json_load,
    dump as json_dump
)

class Database:
    '''
    THis class handles all access to any json files\makeshit databases.
    '''

    def __init__(self, log) -> None:
        self.log = log
        
    def load_data(self, fname_: str):
        ''' get the settings form the settings json file'''
        try:
            with open(fname_, "r") as file:
                data: list = json_load(file)
                
        except FileNotFoundError:
            # Use a tkinter window since this app should run in the BG to inform right away there is a problem
            self.log.log_error_report('File Not Found', report=f"Cannot find: {fname_}. \nApplication cannot continue.")
            exit()
        return data        

    def write_data(self, _data_: list, database_: str) -> None:
        """Writes changes made to the messages database.] """
        try:
            with open(database_, "w") as file:
                json_dump(_data_, file, indent=4)    
        except FileNotFoundError:
            self.log.log_error_report(f'{database_} not found.', report=f'{database_} not found.')
            exit()
    