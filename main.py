#responder.py

# A simple sister application to "Tizzle" that will disable a message Task according to instructions
# found in the Email inbox associated with the account. Will also give status reports to the 'Contact"
# noted in the settings file

from time import sleep
from sys import exit
from responder import Responder

from constants import(
     SET_FILE, 
     WAIT_TIME
)
from os import getpid

# Make it send a text to let user know the texts have stopped?
# Kind of defeats the purpose.

def main(args=None) -> None:
    hunting:          bool = True
    responder:   Responder = Responder(SET_FILE, getpid())  
    
    try:
        while(hunting):            
           responder.log.log_task('Checking email...')
           loggedin: bool = responder.email.login()

           if loggedin:
              email_message: str = responder.email.get_email_delete_email() 
              
              if email_message:
                 email_data: dict[str, str] = responder.parse_email(email_message)
                 responder.handle_instructions(email_data)                          
           else: 
               # Login error show POP UP so user checks to see whats wrong.
                responder.log.log_error_report(
                    f'Failure to log in to email @ {responder.settings["imap_credentials"][0]}',
                    f'Could not login to {responder.settings["imap_credentials"][0]} Check your settngs. ',
                    report=f'Error logging in to: {responder.settings["imap_credentials"][0]}'
                    )  
                hunting = False

           responder.log.log_task('No email, waiting...')
           sleep(WAIT_TIME)    

    except Exception as er:
        # log the error
        # terminate the app
        hunting = False
        responder.log.log_error_report(f'Exception! \n{er}', report=er)
        exit()

    except KeyboardInterrupt:    
        # User shutdown
        responder.log.log_task(f'User shutdown.')
        hunting = False
        exit()
        
    
if __name__ == "__main__":     
    main()
