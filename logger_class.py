# Logger.py

from datetime import datetime
from tkinter.messagebox import showinfo

class RespondLogger():
    ''' 
    Handles all actiions related to any logging program Status reports and errors.
    ''' 

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
        '''
           Logs the error and reports with a message to alert user.
           Will also pop up  message box to alert the user of any doom that
           needs to be surveyed
        '''        
        error = "ERROR: " + error 
        self.log_task(error)       
        if report: 
            showinfo('ERROR:', {report})

    def get_time(self) -> str:
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S").split()[1]