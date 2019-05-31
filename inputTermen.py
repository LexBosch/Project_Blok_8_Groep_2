import threading
import time
from datetime import date
import textmining
import sessie
import zoekwoord


class pubMedThread(threading.Thread):
    def __init__(self, termList, sessionName, currentDate, email, searchDepth):
        threading.Thread.__init__(self)
        self.termList = termList
        self.sessionName = sessionName
        self.currentDate = currentDate
        self.email = email
        self.searchDept = searchDepth

    def run(self):
        pubmedresults, termsfound = textmining.textming_Start(self.termList, self.searchDept, [])
        sessionobject = self.createSessionObject(pubmedresults, termsfound)
        #Sophie, hier kan je de database aanroepen
        print()




    def createSessionObject(self, articleResults, termsFound):
        return sessie.Session(
            self.sessionName,
            self.currentDate,
            self.createTermObject(articleResults, termsFound)
        )

    def createTermObject(self, found_articles, terms):
        termList = []
        for singeleterm in terms:
            articleList = []
            for singleArticle in found_articles:
                if singeleterm in singleArticle["terms"]:
                    articleList.append(singleArticle["articleObject"])
            termList.append(zoekwoord.Zoekwoord(singeleterm, articleList))
        return termList




def StartPubMedSearch(searchTermList, sessionName, email, depthSearch):
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    newThread = pubMedThread(searchTermList, sessionName, currentDate, email, int(depthSearch))
    newThread.start()
