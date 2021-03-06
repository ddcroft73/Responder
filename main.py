#responder.py

# A simple sister application to "Tizzle" that will disable a message Task according to instructions
# found in the Email inbox associated with the account. Will also give status reports to the 'Contact"
# noted in the settings file, can be restarted, shutdown as well.

from time import sleep
from sys import exit
from responder import Responder
from constants import(
     SET_FILE, 
     WAIT_TIME
)
from os import getpid

def main(args=None) -> None:
    hunting:             bool = True
    responder:      Responder = Responder(SET_FILE, getpid())  
    email_message: str | None = None
    body:          str | None = None
    try:
        while(hunting):            
           responder.log.log_task('Checking email...')
           loggedin: bool = responder.email.login()

           if loggedin:
              email_message, body = responder.email.get_email()
              
              if email_message:
                 email_data: dict[str, str] = responder.parse_email(email_message, body)
                 if email_data is not None:
                     responder.handle_instructions(email_data)                          
           else: 
                raise Exception('Check login credintials in settings.json file.')

           responder.log.log_task('No email, waiting...')
           sleep(WAIT_TIME)    

    except Exception as er:
        hunting = False        
        responder.log.log_error_report('Logged in main \n' + str(er), report=er)
        exit()

    except KeyboardInterrupt:    
        # User shutdown
        responder.log.log_task(f'User shutdown.')
        hunting = False
        exit()
        
    
if __name__ == "__main__":     
    main()
