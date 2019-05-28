import threading
import time
from datetime import date


class pubMedThread(threading.Thread):
    def __init__(self, termList, sessionName, currentDate, threadName):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.termList = termList
        self.sessionName = sessionName
        self.currentDate = currentDate

    def run(self):
        # call textmining
        print()


def StartPubMedSearch(searchTermList, sessionName, threadName):
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    newThread = pubMedThread(searchTermList, sessionName, currentDate, threadName)
    newThread.start()
