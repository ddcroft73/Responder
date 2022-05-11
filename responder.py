# responder.py
from subprocess import run
from sys import executable
from time import sleep
from email_class import EmailHandler
from logger_class import RespondLogger
from fileacces import FileAccess
from re import findall
from constants import *


class Responder():

    ''' ties in all the classes and does the work '''

    settings: dict = {}
    commands_this_run:   list[str] = []

    def __init__(self, settings_location: str,  pid: int):
        
        self.log:  RespondLogger = RespondLogger(LOG_FILE)
        self.db:        FileAccess = FileAccess(self.log)
        self.settings            = self.db.load_data(settings_location)      
        self.email: EmailHandler = EmailHandler( self.settings['imap_credentials'][0], self.settings['imap_credentials'][1], 
                                   self.settings['admin_contact'], self.settings['imap_server'], self.log)   
        self.pid: int = pid
        self.log.log_task(f'Responder Started. PID: {self.pid}')
        self.start_time: str = self.log.get_time()



#-------------------------------------------------------------------------------------------------------------------------
    def disable_task(self, task_name_: str) -> None:
        '''
        Disable a task in the WTS
        '''        
        command: str = ["schtasks.exe", "/CHANGE",  "/TN", task_name_, "/DISABLE"]
        # log the task
        self.log.log_task(f'Disabling: {task_name_}')  
        
        return_code: int = run(command).returncode  
        if (return_code == SUCCESS):
            self.log.log_task(f'Disabled: {task_name_}')
            self.__change_message_status(task_name_, 'Disabled.')
        else:
            self.log.log_error_report(f'Attempting to disable: {task_name_}.')
#-------------------------------------------------------------------------------------------------------------------------
    def parse_email(self, raw_email_: str) -> dict[str, str]:
        '''
        searches an email message for a dict of regex targets, returns any found
        to a similar dict else None for nothing
        '''
        targets: dict[str,str] = {
            'status'  : r'status',
            'stop'    : r'(stop m\d*)',
            'shutdown': r'shutdown',
            'phone'   : r'(from: <\d*)'
        }
        dict_results: dict[str,str, str] = {}

        for target, pattern in targets.items():
            results: list[str] = findall(pattern, raw_email_)  
                 
            if results:
                #there should only ever be one of each command issued at a time.
                for item in results:
                    # clean up the quarry. 
                    if target == 'stop':  
                        item = item.split()[1]
                    if target == 'phone': 
                        item = item.split('<')[1]
                dict_results[target] = item 
            else: 
                dict_results[target] = None

        return dict_results
#-------------------------------------------------------------------------------------------------------------------------
    def handle_instructions(self, data_: dict[str,str], msg_: str=None) -> None:
        '''
        handles any request issued from a client.
        '''            
        self.log.log_task(f"Received {self.__num_commands(data_)} commands from '{self.__get_user(data_['phone'])[NAME]}'")
        user_commands: tuple[str, str, str] = self.__get_commands(data_)   
        
        for command in user_commands:
            self.__distibute_commands(command[0], command[1], command[2])

        return        
#-------------------------------------------------------------------------------------------------------------------------
    def __distibute_commands(self, command:str, payload: str, user_phone: str) -> None:        
        '''
        executes a users command.
        ''' 
        msg: str
        arg: str
        sub_command:   str  
        this_user:     str = self.__get_user(phone_num_=user_phone)[NAME]
        admin_contact: str = self.settings['admin_contact']

        self.log.log_task(f"Command: {command.upper()} issued.")
        match command:
            case 'status':
                self.commands_this_run.append(command + f' @ {self.log.get_time()}\n')
                msg = ('\n'
                    f'Status Report:\n'
                    f'Responder is running\n'
                    f'Started at: {self.start_time}\n'
                    f'Admin Contact: {admin_contact}\n'
                    f'Commands since start:\n'
                    f'{"".join(self.commands_this_run)}\n'
                )
                sub_command = 'send'
                arg = admin_contact

                # Status should only be avaialble to the admin contact.
                if this_user != admin_contact:
                    # notify this user they cannot query for status.
                    msg = ('Status reports are only available to the administrator. ')
                    self.log.log_task(f'USER: {this_user} queried responder for a status report.')
                    arg = this_user

            case 'shutdown':
                # shutdown should only be avaialble to the admin contact.
                command, msg, sub_command, arg = self.__shutdown_responder(admin_contact, this_user)               
                
            case 'stop':
                self.__stop_message(payload, user_phone)
                self.commands_this_run.append(f'stop {payload} From User: "{this_user}". '
                                              f'Received @ {self.log.get_time()} \n')
                return # work here is done.
                
            case _:
                self.log.log_task(f"Unknown request: {command}")
                self.commands_this_run.append(f'Unknown command {command} From User: "{this_user}". '
                                              f'Received @ {self.log.get_time()} \n')
                return


        self.__execute_command(command, sub_command, arg, msg)       

#-------------------------------------------------------------------------------------------------------------------------
    def __execute_command(self, command_: str, sub_: str, arg_: str, msg_: str) -> None:
        '''
        carries out a user command.
        '''
        tizz_command: list[str] = [executable, TIZZLE, sub_, arg_, msg_ ]  
        
        if command_ == 'shutdown':
            tizz_command = tizz_command[:-1]

        return_code: int = run(tizz_command).returncode
        if (return_code == SUCCESS):
            self.log.log_task(f"Request: {command_.upper()} handled.\n")
            sleep(1) # Let the command register in the log
        else:
            self.log.log_error_report(f'Attempting to handle  "{command_.upper()}"')
#-------------------------------------------------------------------------------------------------------------------------
    def __shutdown_responder(self, admin_contact_: str, this_usr_: str) -> tuple[str,str,str,str]:
        '''
        handles the shutdown sequence.
        '''
        if this_usr_ != admin_contact_:
            # notify this user they cannot query for status.
            command = "INVALID USER"
            sub_command = 'send'
            msg = ('Shutdown command is only available to the administrator. ')
            self.log.log_task(f'USER: {this_usr_} tried to shudown Responder.')
            arg = this_usr_
        else:    
            command = 'goodbye messsage'
            msg = f'Responder shutdown. Good-Bye.'
            sub_command = 'send'
            arg = admin_contact_
            self.__execute_command(command, sub_command, arg, msg)

            sleep(2)
            self.log.log_task(f"Shutting down.")
            command = 'shutdown'
            msg = ''
            sub_command = 'responder'
            arg = '--stop'

        return command, msg , sub_command, arg
#-------------------------------------------------------------------------------------------------------------------------
    def __stop_message(self, msg_id_: str, phone_: str) -> None:
        '''
        Stops a users message. If the user is not a part of a group, it will disable the
        entire message. If group message, it will only disable the message for that member.
        '''
        msg_id_ = msg_id_.upper()
        user_name: str = self.__get_user(phone_)[NAME]
        
        destination: str| None = self.__get_message_type(msg_id_)        
        if destination == 'group':
            self.log.log_task(f'GROUP MEMBER: "{user_name}" of GROUP '
                              f'"{self.__get_message(msg_id_)[DESTINATION]}" Stopping message "{msg_id_}"')
            # open the contacts db, and edit the msg_id list for this contact.
            self.__disable_user_message(user_name, msg_id_)

        elif destination == 'contact':
            self.log.log_task(f'CONTACT: "{user_name}" stopping {msg_id_}')            
            self.disable_task(msg_id_)            
        else:
            # notify the sender, 
            command = 'File Not Found'
            msg = f"{msg_id_} does not not exist. Perhaps you've previously disabled it or mistyped the ID."
            sub_command = 'send'
            arg = user_name
            self.__execute_command(command, sub_command, arg, msg)

            self.log.log_task(f'{msg_id_} does not not exist. Aborting.') 
#-------------------------------------------------------------------------------------------------------------------------
    def __disable_user_message(self, user_: str, msg_id_: str) -> None:
        '''
        stops a message for one meber in a group.
        '''
        msg_id_ = msg_id_.upper()
        user_ = user_.title()
        # Look up this user and remove the message ID if its there.
        # it may have been removed previuosly
        contacts: list[list[str]] = self.db.load_data(CONTACTS_DB)
        for contact in contacts:
            if contact[NAME] == user_:
                if msg_id_ in contact[MSG_LIST]:
                     contact[MSG_LIST].remove(msg_id_)
                     self.db.write_data(contacts, CONTACTS_DB)
                     self.log.log_task(f'MESSAGE ID: {msg_id_} was removed from "{user_}".')
                else:
                    self.log.log_task(f'MESSAGE ID: {msg_id_} was not found. Perhaps it is already disabled.')
#-------------------------------------------------------------------------------------------------------------------------
    def __num_commands(self, data_: dict[str,str]) -> int:
        '''
        returns the count on the commands sent by the user.
        '''
        cnt: int = 0
        for command in data_.values():
            if command is not None:
                cnt+=1
        return (cnt - 1) # DOnt record the phoe number as a command
#-------------------------------------------------------------------------------------------------------------------------
    def __get_message_type(self, msg_id_: str) -> str:
        '''
        returns 'group' if its a group 'contact' if contact
        None if doesnt exist
        '''     
        # get the mesage destination and cross ref that with the contact names
        # if its not a contact, it is a group
        message: str = self.__get_message(msg_id_.upper())
        if message is not None:
            # If this is a name of a group, it will not be in the conacts DB
            user: str = self.__get_user(name_=message[DESTINATION])

            if user is None:
                return 'group'
            elif user is not None:
                return 'contact' 
        else:
            return 
#-------------------------------------------------------------------------------------------------------------------------
    def __get_message(self, msg_id_: str) -> str | None:
        '''
        returns a message by the ID or None
        '''     
        try:
            messages: list[list[str]] = self.db.load_data(DB)
            for msg in messages:
                if msg[ID] == msg_id_.upper():
                    return msg
            return 

        except Exception as er:
            self.log.log_error_report(str(er))
#-------------------------------------------------------------------------------------------------------------------------
    def __get_user(self, phone_num_: str=None, name_: str=None) -> str:
        '''
        gets the info of the user associated with this number, or name
        '''        
        try:
            contact_info: list[list[str]] = self.db.load_data(CONTACTS_DB)
            for contact in contact_info:
                if phone_num_ is not None:
                    if contact[PHONE] == phone_num_:
                        return contact

                if name_ is not None:
                   if contact[NAME] == name_.title():
                        return contact             
            return     

        except Exception as er:
            self.log.log_error_report(str(er))  
#-------------------------------------------------------------------------------------------------------------------------
    def __get_commands(self, data_: dict[str,str]) -> tuple[str, str]:
        '''
        parses the dict and returns a list of the commands sent by a user.
        eyrns the phone number to ID the user with all commands. 
        '''
        # extract the phone number
        phone: str = data_['phone']
        return [
            (target, command, phone) 
            for target, command in data_.items() 
            if command is not None and target != 'phone'
        ]   
#-------------------------------------------------------------------------------------------------------------------------
    def __change_message_status(self, msg_id_: str, _status: str) -> None:
        """
        Changes the status of a message used by disable
        """        
        msg_id_ = msg_id_.upper()
        try:
            messages: list[list[str]] = self.db.load_data(DB)
            for msg in messages:
                if (msg[ID] == msg_id_):
                    msg[STATUS] = _status
                    self.db.write_data(messages, DB)

        except Exception as er:
            self.log.log_error_report(str(er))    


