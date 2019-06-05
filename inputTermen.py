import threading
from datetime import date
import textmining
from Object import sessie, zoekwoord
import visualiseGraph
import databaseconnectie
import mail
import mysql



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
        visualiseGraph.createNewGraph(sessionobject)
        try:
            databaseconnectie.databasevullen(sessionobject)
        except mysql.connector.errors.IntegrityError:
            #Still seems to work just fine
            pass
        databaseconnectie.sessiesophalen()
        mail.Mail(self.email, self.sessionName)




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

                for meshterm in singeleterm["To"]:
                    if meshterm in singleArticle["terms"]:
                        articleList.append(singleArticle["articleObject"])
            termList.append(zoekwoord.Zoekwoord(singeleterm["From"], articleList, singeleterm["To"]))
        return termList




def StartPubMedSearch(searchTermList, sessionName, email, depthSearch):
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    newThread = pubMedThread(searchTermList, sessionName, currentDate, email, int(depthSearch))
    newThread.start()
