import smtplib
import subprocess
import time


def GetInternalIP(interface):
    output = subprocess.check_output(["ifconfig", interface])
    output = output.decode('utf-8')

    # Parse ifconfig output
    lines = output.split("\n")
    ipAddr = lines[1].strip().split("  ")[0].split("inet")[1]
    return ipAddr


def SendMail():
    dateAndTime = time.strftime("%A, %d %m %Y %H:%M:%S (%Z)", time.localtime())

    subject = "Raspberry Pi event [{}]".format(ipAddr)
    body = "Current raspberry IP is: {}\n\n\n{}".format(ipAddr, dateAndTime)

    msg = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}".format(
        fromAddr, toAddr[0], subject, body)

    # Create SMTP Object
    smtpObj = smtplib.SMTP(smtpServer, smtpPort)

    smtpObj.ehlo()  # Identify client
    smtpObj.starttls()
    smtpObj.ehlo()  # Identify client under TLS

    smtpObj.login(smtpUser, smtpPass)

    smtpObj.sendmail(fromAddr, toAddr, msg)
    smtpObj.quit()
    return


interface = "wlan0"
prevIP = None  # NO TOCAR

smtpServer = "smtp.gmail.com"
smtpPort = 587
smtpUser = "from@gmail.com"
smtpPass = "******"

fromAddr = "<from@gmail.com>"
toAddr = ["<to@gmail.com>"]

# Workaround to gain time while some necessary network resources are being prepared
time.sleep(30)

ipAddr = GetInternalIP(interface)
SendMail()
