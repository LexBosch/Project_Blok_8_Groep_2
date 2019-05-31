import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail(object):
    def __init__(self, userMail, sessionName):
        self.mailToadress = userMail
        self.sessionName = sessionName
        self.scriptEmail = "GourdsGroup@gmail.com"
        self.emailPassword = "projectgroep1"
        send(self)


def send(self):
    createMail(self)
    sendMail(self)


def createMail(self):
    """ The function makeMessage constructs an e-mail message

    :param mailToAdress: The adress used to send an e-mail to
    :param mailFromAdress: The adress used to send an e-mail
    :return: message is a String containen the e-mail message
    """
    body = """Your job "{0}" at GourdsGroup has finished processing.\nHead over to 'http://bittergourd.info/graph' to see the result""".format(
        self.sessionName)
    subject = "Your job {0} is done".format(self.sessionName)

    msg = MIMEMultipart()
    msg['TO'] = self.mailToadress
    msg['from'] = self.scriptEmail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    self.message = msg.as_string()


def sendMail(self):
    """ The function sendMail makes connection with the server, connects to the e-mail adress and sends the message.

    :param message: Is a String containen the e-mail message
    :param mailFromServer: The server used to send an e-mail
    :param mailFromAdress: The adress used to send an e-mail
    :param mailFromPassword:  The password for the used e-mail
    :param mailToAdress: The adress used to send an e-mail to
    :return: -
    """
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(self.scriptEmail, self.emailPassword)

    server.sendmail(self.scriptEmail, self.mailToadress, self.message)
    server.quit()
