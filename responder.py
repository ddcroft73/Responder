# responder.py
from subprocess import run
from sys import executable
from json import(
    load as json_load,
    dump as json_dump
)

from time import sleep
from tkinter.messagebox import showinfo

from email_class import EmailHandler
from logger_class import EasyLogger
from constants import *
from sys import exit


class Responder():
    ''' The Application class'''
    settings: dict = {}
    email: EmailHandler
    log: EasyLogger    

    def __init__(self, settings_location: str):
        #Open the settings file and get the settings
        self.settings = self.load_data(settings_location)
        # access the logger class
        self.log = EasyLogger(LOG_FILE)
        # access the email class
        self.email = EmailHandler(
             self.settings['imap_credentials'][0], 
             self.settings['imap_credentials'][1], 
             self.settings['contact'],
             self.settings['imap_server'],
             self.log
        )              

    def load_data(self, fname: str):
        ''' get the settings form the settings json file'''
        try:
            with open(fname, "r") as file:
                data: list = json_load(file)

        except FileNotFoundError as er:
            # Report that the file aint there... Use a tkinter window since this app should run in the BG
            # to inform right away there is a problem
            self.log.log_error_report(er, report=f"Cannot find: {fname}. \nApplication cannot continue.")
            exit()
        return data        

    def write_data(self, _data: list, database: str) -> None:
        """Writes changes made to the messages database.] """
        with open(database, "w") as file:
            json_dump(_data, file, indent=4)    
            

    def disable_task(self, instruction: str) -> None:
        '''
        Disable a task in the WTS
        '''        
        task_name = instruction.split()[1]
        command: str = ["schtasks.exe", "/CHANGE",  "/TN", task_name, "/DISABLE"]
        # log the task
        self.log.log_task(f'Disabling: {task_name}')  
        
        return_code: int = run(command).returncode  
        if (return_code == SUCCESS):
            self.log.log_task(f'Disabled: {task_name}')
            self.__change_message_status(task_name, 'Disabled')
        else:
            self.log.log_task(f'ERROR: Attempting to disable: {task_name}.')

    def handle_instructions(self, request_: str, msg_: str=None) -> None:
        '''
        handles any request issued from a client.
        '''        
        msg: str
        arg: str
        sub_command: str = ""

        self.log.log_task(f"Command: {request_.upper()} issued.")
        match request_:
            case 'status':
                msg = 'Status Report from - RESPONDER\nResponder is Running...'
                sub_command = 'send'
                arg = self.settings['contact']
                pass
            case 'shutdown':
                self.log.log_task(f"Shutting down.")
                msg = ''
                sub_command = 'responder'
                arg = '--stop'
                pass
            case 'start':
                pass
            case _:
                self.log.log_task(f"Unknown request: {request_}")
                return

        tizz_command: list[str] = [executable, TIZZLE, sub_command, arg, msg ]  
        if request_ == 'shutdown':
            tizz_command = tizz_command[:-1]

        return_code: int = run(tizz_command).returncode
        if (return_code == SUCCESS):
             self.log.log_task(f"Request: {request_.upper()} handled.")
             sleep(1) # Let the command take effect


    def __change_message_status(self, _msg_id: str, _status: str) -> None:
        """
        Changes the status of a message used by disable
        Same function used in Tizzle
        """        
        messages: list[list[str]] = self.load_data(DB)
        for msg in messages:
            if (msg[ID] == _msg_id.upper()):
                msg[STATUS] = _status
        self.write_data(messages, DB)


