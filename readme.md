# Responder - Helper app for Tizzle.

## Purpose:
This little program runs in the background and checks for commands sent by the message receiver. It will allow the intended receiver to stop any recurring messages if they are so inclined to do so. This is just an added feature that is basically just bells and whistles and it will fight against any spam attempts. However it must be launched to be effective. One would argue that I could have made this a part of the application but that would mean Tizzle as big as its getting would have to run all the time. This takes the burden off and runs a bit quieter.

## How it works:
Whenever a recurring, (hourly, minute, daily, weekly, monthly) message is created, the message is appended with a simple "Stop" message to allow the receiver to disable the texts right then. (Reply 'Stop Message_ID' to stop.). The application simply runs on a loop every 3 minutes (Adjustable via the `WAIT_TIME` constant.) and checks the email inbox of the account you use to send the text messages. When it finds the stop command it deletes it, so there is ever only one,  and then disables the message task in question. A log is kept and it runs pretty effectively. It must be stopped from Tizzle. Or with `Ctrl+C`. Commands can be sent all at once but only one message can be stopped at a time. You can query the `status` and send a `stop` command and `shutdown` the responder in one text.<br><br>
The application runs in its own window. You can send the following commands from the text message as replies:
 - status
 - stop < message ID >
 - shutdown
 - restart

 Only the contact set up in the settings file can `restart` or `shutdown` of course. But the application can be controlled pretty well from text replies.
 So far I have only tested this with responses from users of AT&T, Cricket, Metro, and Verizon. Can't be sure the responder will effectively handle the 
 MMS Texts sent as emails back to the account you run Tizzle off of. It may work as is, but could be some bugs as far as how the messages are parsed.
 <br>

Run Responder:
```
:\>python \path\to\responder\main.py
```

Run Responder from Tizzle:
```
:\>python tizz responder -start
```
```
:\>python tizz responder -stop
```
<br>
<br>
