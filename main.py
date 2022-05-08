#responder.py

# A simple sister application to "Tizzle" that will disable a message Task according to instructions
# found in the Email inbox associated with the account.
#
# Purpose:
#    When Tizzles are sent on a recurring scedule the user should be able to stop anymore incoming texts
#    at will if they do not want\need to wait out the cycle. USer will simply reply to the text message
#    with : "Stop <MessageID>". THe message ID is included in the text.
#
# Loop:
#   Login to email  
#   Check for a specific email
#   Delete email
#   If Found:
#      define task
#         handle instruction
#   sleep 5 mins  
#   
# Program attempts to catch all errors and restart so that app will run ubtil it is manually shut down
#
# My first attempt at using 100% OOD. Im sure its not the best it can be. and it likely doesnt even need 
# OOD But SInce I PLan on rewritting Tizzle because it needs it, I am practicing.

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
    responder:   Responder = Responder(SET_FILE)    
    instruction: list[str]
    pid:               int = getpid()
    
    responder.log.log_task(f'Responder Started. PID: {pid}')

    try:
        while(hunting):            
           responder.log.log_task('Checking email...')
           loggedin: bool = responder.email.login()

           if loggedin:
              instruction = responder.email.get_instructions_delete_email()  

              if instruction:
                  if'stop' in instruction:     
                       responder.log.log_task(f'Disable instruction found: {instruction}')
                       responder.disable_task(instruction)
                       responder.email.logout()  
                  else:
                       responder.handle_instructions(instruction)  
              else:
                  # No instruction
                  # Logout and wait...
                  responder.email.logout()
           else: 
               # Login error check to see whats wrong.
                responder.log.log_error_report(
                    f'Failure to log in to email @ {responder.settings["imap_credentials"][0]}',
                    f'Could not login to {responder.settings["imap_credentials"][0]} Check your settngs. ',
                    report=f'Error loggin in to: {responder.settings["imap_credentials"][0]}'
                    )  
                hunting = False
                raise Exception('Error logging into email account.')

           # Wait..     
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
    