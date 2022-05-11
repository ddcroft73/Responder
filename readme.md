# Responder - Helper app for Tizzle.

## Purpose:
This little program runs in the background and checks for commands sent by the message receiver. It will allow the intended receiver to stop any recurring messages if they are so inclined to do so. This is just an added feature that is basically just bells and whistles and it will fight against any spam attempts. However it must be launched to be effective. One would argue that I could have made this a part of the application but that would mean Tizzle as big as its getting would have to run all the time. This takes the burden off and runs a bit quieter.

## How it works:
Whenever a recurring, (hourly, minute, daily, weekly, monthly) message is created, the message is appended with a simple "Stop" message to allow the receiver to disable the texts right then. (Reply 'Stop Message_ID' to stop.). The application simply runs on a loop every 3 minutes (Adjustable via the `WAIT_TIME` constant.) and checks the email inbox of the account you use to send the text messages. When it finds the stop command it deletes it, so there is ever only one,  and then disables the message task in question. A log is kept and it runs pretty effectively. It must be stopped from Tizzle. Or with `Ctrl+C`. Commands can be sent all at once but only one message can be stopped at a time. You can query the `status` and send a `stop` command and `shutdown` the responder in one text.<br>

Run Responder:
```
:\>python \path\to\responder\main.py
```

Run Responder from Tizzle:
```
:\>python tizz responder -start
```
Terminate Responder: (Currently the most efficient method)
```
:\>python tizz responder -stop
```
<br>
<br>

## Problems:
Threading:<br>
`Fatal Python error: _enter_buffered_busy: could not acquire lock for <_io.BufferedWriter name='<stdout>'> at interpreter shutdown, possibly due to daemon threads Python runtime state: finalizing (tstate=0x000001af141b2e30)`

I cannot get it to launch more than once per session without it causing an error. I can only get it to return the terminal with `daemon=True`, but it would seem that once that thread is destroyed you can't reuse it. I have tried `concurrent.futures.ThreadPoolExecutor()` with similar results. I only need to use two threads. The one Tizzle is in and one for the Responder. The problem arises when I terminate Responder. It's like I can't get an additional thread and it seems odd to have to use a bunch of threads, that only are ever destroyed when you close the terminal. It may just be best to launch in its own terminal. I'm sure this is a rather common problem, and as soon as learn about multi-threading, or threading in general I'll address this issue.
