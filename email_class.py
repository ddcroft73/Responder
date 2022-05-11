#email.py

#from logger import Logger

import imaplib
import email

from logger_class import RespondLogger


class EmailHandler():
    ''' Handles all actions asociated with email'''    
    imap = None 

    def __init__(self,  user: str,  pword: str,  contact: str, imap_server: str,  logger: RespondLogger):
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

    def get_email_delete_email(self) -> list[str]:
        ''' 
        Gets the contents of the inbox and searches for instructions
        If found then the instruction is passed on and the email is deleted.
        '''        
        raw_msg: str|None = None
        cnt: int = 0
        self.imap.select("INBOX")
        _, messages = self.imap.search(None, 'ALL')

        messages: list[str] = messages[0].split(b' ')
        try:
            # Should only ever be one message in this box all mail is deleted on exit
            for mail in messages:
                _, msg = self.imap.fetch(mail, "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        raw_msg = email.message_from_bytes(response[1])
                        raw_msg = str(raw_msg).lower()    
                        cnt+=1
                        self.log.log_task(f"Email found: {cnt}") 
                self.imap.store(mail, "+FLAGS", "\\Deleted")   

            self.imap.expunge()  
            self.log.log_task(f"Email deleted.")  

        except:
           # no emails keep shlooking 
           pass 
        
        return raw_msg 
 
    def logout(self):
         '''Logs the account out while waiting for emails'''
         self.imap.close()
         self.imap.logout()
