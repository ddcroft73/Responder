#email_class.py
import imaplib
import email
from re import findall

from h11 import Data

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
        gets the contents of the inbox, Which should only be one email. If there is more it will only
        return the last one. returns the From and the body so that commands and the user number can easily
        be extracted.
        '''        
        email_from: str | None = None
        email_body: str | None = None
        email_type: str | None = None

        self.imap.select('INBOX')
        _, data = self.imap.uid('search', None, "ALL") 
        try:        
            i = len(data[0].split())
            for x in range(i):
                latest_email_uid = data[0].split()[x]
                _, email_data = self.imap.uid('fetch', latest_email_uid, '(RFC822)')
                raw_email = email_data[0][1].lower()
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
            
                email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))

                # Body details
                for part in email_message.walk():
                    email_type = (part.get_content_type())
                    if part.get_content_type() in ["text/html", 'text/plain']:
                         
                        email_body = str(part.get_payload(decode=True))
                        if part.get_content_type() == "text/html":
                            email_body = self.__get_text_from_html(email_body)

                        elif part.get_content_type() == 'text/plain':
                            email_body = self.__clean_text(email_body)                               
                    else:
                        continue
                
                self.log.log_task(f"Email found.")     
        except:
            # no email
            pass

        # Delete if anything was found
        '''if email_body is not None:
             self.__delete_mail()'''

        return email_from, email_body, email_type


    def __delete_mail(self) -> None:
        '''
        Decided to make the delete part a seperate method.
        '''
        self.imap.select("INBOX")
        _, messages = self.imap.search(None, 'ALL')

        messages: list[str] = messages[0].split(b' ')
        # Should only ever be one message in this box all mail is deleted on exit
        for mail in messages:
            self.imap.store(mail, "+FLAGS", "\\Deleted")  
        self.imap.expunge()  
        self.log.log_task(f"Email deleted.")  
       
    def __clean_text(self, message_: str) -> str:
        '''
        Extracts just the text sent by the user.
        "b'stop m991'"
        '''
        return message_[2:-1]

    def __get_text_from_html(self, message_:str) -> str:
        '''
        Extracts from the html just the text sent by the user.
          Still trying to figure this one out. 
        '''
        
        return message_

    def logout(self):
         '''Logs the account out while waiting for emails'''
         self.imap.close()
         self.imap.logout()

