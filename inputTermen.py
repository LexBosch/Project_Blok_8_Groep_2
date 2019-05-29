import threading
import time
from datetime import date
import textmining


class pubMedThread(threading.Thread):
    def __init__(self, termList, sessionName, currentDate, email, searchDepth):
        threading.Thread.__init__(self)
        self.termList = termList
        self.sessionName = sessionName
        self.currentDate = currentDate
        self.email = email
        self.searchDept = searchDepth

    def run(self):
        textmining.textming_Start(self.termList, self.searchDept, [])
        print()


def StartPubMedSearch(searchTermList, sessionName, email, depthSearch):
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    newThread = pubMedThread(searchTermList, sessionName, currentDate, email, int(depthSearch))
    newThread.start()
