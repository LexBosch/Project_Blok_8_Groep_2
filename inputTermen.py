import threading
import time
from datetime import date


class pubMedThread(threading.Thread):
    def __init__(self, termList, sessionName, currentDate, email):
        threading.Thread.__init__(self)
        self.termList = termList
        self.sessionName = sessionName
        self.currentDate = currentDate
        self.email = email

    def run(self):
        # call textmining
        print()


def StartPubMedSearch(searchTermList, sessionName, email):
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    newThread = pubMedThread(searchTermList, sessionName, currentDate, email)
    newThread.start()
