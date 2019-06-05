import json
import databaseconnectie


def showPage():
    print("ter")


def get_Sessions():
    """Gets all the sessionNames and dates the sessions are created

    :return: List with dictionaries with all the names and dates of the sessions
    """

    lijst_met_sessies = []
    resultaatsessieID, resultaatsessietitel, resultaatsessiedatum = databaseconnectie.sessiesophalen()
    for sessienummer in range(0, len(resultaatsessieID)):
        string = "{0} | {1}".format(resultaatsessietitel[sessienummer],resultaatsessiedatum[sessienummer])
        lijst_met_sessies.append(
            {
                "sessionName": string,
                "sesId":resultaatsessietitel[sessienummer]
            }
        )

    print(lijst_met_sessies)
    return lijst_met_sessies


def createNewGraph(SessionObject):
    jsonFile = terms(SessionObject.get_zoekwoorden())

    newJson = {}

    fo = open("static/adFiles/graph_files/data{0}.json".format(SessionObject.get_titel()), "w")
    fo.write(json.dumps(jsonFile))
    fo.close()


def terms(termObjList):
    termID = 0
    jsonFile = []
    listOfOtherTerms = termObjList
    for termObj in termObjList:
        termID += 1
        jsonFile.append(createTermNode(termObj, termID))
        for otherTermOjcect in listOfOtherTerms[termID:]:
            connScore = 0
            articleList = []
            for article in termObj.get_artikelen():
                if article in otherTermOjcect.get_artikelen():
                    articleList.append({"titel": article.get_titel(),
                                        "pubdate": article.get_pub_datum(),
                                        "pmId": article.get_pubmed_id(),
                                        "authors": createAuthorList(article)})
            newArticleList = []
            for article in articleList:
                if article not in newArticleList:
                    newArticleList.append(article)
                    connScore += 0.05
            edgeName = str(termID) + "00100" + str(termObjList.index(otherTermOjcect) + 1)
            if (connScore > 0):
                jsonFile.append(createArticleEdge(termID, termObjList.index(otherTermOjcect) + 1, connScore, edgeName,
                                                  newArticleList))

    return jsonFile


def createAuthorList(article):
    authorList = []
    for author in article.get_authors():
        authorList.append({
            "fore": author.get_initial(),
            "last": author.get_last_name()
        })
    return authorList


def createTermNode(termObj, termID):
    termNode = {
        "data": {
            "id": "",
            "idInt": 0,
            "name": "",
            "score": 0.006769776522008331
        },
        "group": "nodes",
        "removed": False,
        "selected": False,
        "selectable": True,
        "locked": False,
        "grabbed": False,
        "grabbable": True
    }
    termNode["data"]["id"] = '{0}'.format(str(termID))
    termNode["data"]["id"] = termID
    termNode["data"]["name"] = termObj.get_term()
    termNode["data"]["score"] = 0.2
    return termNode


def createArticleEdge(termId1, termId2, score, linkId, articleList):
    articlEdge = {
        "data": {
            "source": "",
            "target": "",
            "weight": 0.1,
            "group": "coexp",
            "networkId": 1205,
            "networkGroupId": 18,
            "intn": True,
            "rIntnId": 58,
            "id": "12"
        },
        "position": {},
        "group": "edges",
        "removed": False,
        "selected": False,
        "selectable": True,
        "locked": False,
        "grabbed": False,
        "grabbable": True,
        "classes": ""
    }
    articlEdge["data"]["source"] = termId1
    articlEdge["data"]["target"] = termId2
    articlEdge["data"]["weight"] = score
    articlEdge["data"]["id"] = linkId
    articlEdge["data"]["articles"] = articleList

    return articlEdge
