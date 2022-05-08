#email.py

#from logger import Logger

import imaplib
import email
from re import findall


class EmailHandler():
    ''' Handles all actions asociated with email'''    
    imap = None 

    def __init__(self,  user: str=None,  pword: str=None,  contact: str=None, imap_server: str=None,  logger=None):
        self.user = user
        self.pword = pword
        self.contact = contact
        self.imap_server = imap_server
        self.log = logger

    def login(self) -> bool:
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.imap.login(self.user, self.pword)  
        except:
            return False 
        return True

    def get_instructions_delete_email(self) -> tuple:
        ''' 
        Gets the contents of the inbox and searches for instructions
        If found then the instruction is passed on and the email is deleted.
        '''
        messages: list
        # stop m123
        targets: list[str]     = [r'(stop m\d\d\d)', r'status', r'shutdown' ]
        result:  list[str]|str = []

        self.imap.select("INBOX")
        _, messages = self.imap.search(None, 'ALL')
        messages = messages[0].split(b' ')
        try:
            for mail in messages:
                _, msg = self.imap.fetch(mail, "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        msg = str(msg).lower()                
                        for target in targets:        
                            #proactivley flatten the results
                            result.append(''.join(findall(target, msg)))
             
            self.imap.store(mail, "+FLAGS", "\\Deleted")    
            self.imap.expunge()     
            
            result = self.__flatten_result(result)  
        except:
           # no emails to parse  
           pass

        if result:                                     
            # strip off the blank results
            self.log.log_task(f"Email deleted, passing instruction to handler: '{result}'") 
            return result
        else:
            return # None    

    def __flatten_result(self, lst: str) -> str:
        '''
        flattens a list where only one item is not bank
        '''
        for item in lst:
            if item != '':
              return item

        return 'No Results'      

    def logout(self):
         '''Logs the account out while waiting for emails'''
         self.imap.close()
         self.imap.logout()
