# Logger.py

from datetime import datetime
from tkinter.messagebox import showinfo

class RespondLogger():
    ''' 
    Handles all actiions related to any logging program Status reports and errors.
    '''
    log_time: datetime    
    errors: list[str] = []

    def __init__(self, log_file: str, debug=False):
        self.log_file = log_file
        self.debug = debug

    def log_task(self, message: str):
        ''' opens a logfile and saves the time and description of occurence'''
        log_time = datetime.now()
        message = f'[{log_time}] - {message} \n'
        if not self.debug:
            try:
                with open(self.log_file, 'a') as log:
                    log.write(message)
            except Exception as er:
                print(er)  
        else:
            # print to screen            
            print(message)   
            
    def log_error_report(self, error: str, report: str=None):
        '''Logs the error and reports with a message to alert user.'''
        
        error = "ERROR: " + error 
        self.log_task(error)       
        #alert the user so if they are at the computer will see.
        if report: 
            showinfo('ERROR:', {report})

    def get_time(self) -> str:
        '''
        returns the time
        '''       
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S").split()[1]