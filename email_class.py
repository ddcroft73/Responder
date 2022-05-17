#email_class.py

import imaplib
import email
import html2text

class EmailHandler():
    ''' Handles all actions asociated with email'''    
    imap = None 

    def __init__(self,  user: str,  pword: str,  contact: str, imap_server: str,  logger):
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

    def get_email(self) -> list[str]:
        ''' 
        Gets the contents of the inbox and searches for instructions
        If found then the instruction is passed on and the email is deleted.
        '''        
        raw_msg: str|None = None
        body:    str|None = None
        cnt = 0
        self.imap.select("INBOX")
        _, messages = self.imap.search(None, 'ALL')

        messages: list[str] = messages[0].split(b' ')
        try:
            # Should only ever be one message in this box all mail is deleted on exit
            for mail in messages:
                _, msg = self.imap.fetch(mail, "(RFC822)")

                raw_email = msg[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)

                for part in email_message.walk():
                    # Could be useful for 2way communication.
                    body = html2text.html2text(str(part.get_payload()).lower()).strip('\n')

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

        return raw_msg, body


    

    def logout(self):
         '''Logs the account out while waiting for emails'''
         self.imap.close()
         self.imap.logout()

   