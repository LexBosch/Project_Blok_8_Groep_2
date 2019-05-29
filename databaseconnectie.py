import mysql.connector
from mysql.connector import errorcode
from sessie import Session
from zoekwoord import Zoekwoord
from artikel import Artikel
from author import Author

# sessie opvragen, vanuit daar in stappen van erd terug vragen wat er bij hoort.
# dit in dictioariry zetten, dus wordt subdictionary

def main():

    voorbeeldlijst_session = {"Title_session":"test1244543", "Date_session":""}
    voorbeeldlijst_search_querry = {"Term":"testterm"}
    voorbeeldlijst_information_article = {"PubMedID": 50, "Title": "Testtitel", "Year_publication": 2020}
    voorbeeldlijst_author = {"Initial": "SR", "Insertion": "", "Last_name": "Hospel"}
    connectie(voorbeeldlijst_session, voorbeeldlijst_search_querry, voorbeeldlijst_information_article, voorbeeldlijst_author)


def connectie(voorbeeldlijst_session, voorbeeldlijst_search_query, voorbeeldlijst_information_article, voorbeeldlijst_author):

    try:
        cnx = mysql.connector.connect(user='owe7_pg1@hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      password='blaat1234',
                                      host='hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      database='owe7_pg1')

        #tabel_session_vullen(voorbeeldlijst_session, cnx)
        #sessionID = input("welke sessie id?: ")
        #get_session(sessionID, cnx)
        #tabel_search_query_vullen(voorbeeldlijst_search_query, cnx)
        #get_search_query(sessionID, cnx)
        #tabel_information_article_vullen(voorbeeldlijst_information_article, cnx)
        #get_information_article(sessionID, cnx)
        #tabel_author_vullen(voorbeeldlijst_author, cnx)
        sid = 1
        get_session(sid, cnx)
        search_id = get_zoekwoorden(sid, cnx)
        artikel_id = get_articelen(search_id, cnx)
        get_autheurs(artikel_id, cnx)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cnx.close()


def tabel_session_vullen(voorbeeldlijst_session, cnx):
    ###session vullen

    titel = voorbeeldlijst_session["Title_session"]

    if not (voorbeeldlijst_session["Date_session"]):
        datum = voorbeeldlijst_session["Date_session"] = "curdate()"
    else:
        datum = voorbeeldlijst_session["Date_session"] = "'[0]'".format(voorbeeldlijst_session["Date_session"])

    query = """INSERT INTO owe7_pg1.session (Title_session, Date_session) VALUES('{0}',{1});""".format(titel, datum)
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    cnx.commit()
    mycursor2.close()


def get_session(sessionID, cnx):
    ###sessie id ophalen van de zoektermen

    resultaat = {}
    id = sessionID
    query = """select * from owe7_pg1.search_query where idSearch_query in (select Search_query_idSearch_query from owe7_pg1.session_has_search_query where Session_idSession = {0});""".format(id)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    for regel in myresult:
        print(regel)

        #Alle zoekwoorden ophalen
        huidige_sessie = Session("titel" "datum", "lijst_met_zoekwoorden")
        #hier nog toevoegen aan dictionariy


def tabel_search_query_vullen(voorbeeldlijst_search_query, cnx):
    ###search query vullen

    term = voorbeeldlijst_search_query["Term"]

    query = """INSERT INTO owe7_pg1.search_query (Term) VALUES('{0}');""".format(term)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    cnx.commit()
    mycursor2.close()


def get_search_query(sessionID, cnx):
    ###search query id ophalen van de artikelen

    resultaat = {}
    id = sessionID

    query = """select * from owe7_pg1.information_article where idInformation_article in (select Information_article_idInformation_article from owe7_pg1.information_article_has_search_query where Search_query_idSearch_query  = {0})""".format(id)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    for regel in myresult:
        print(regel)
        #hier nog toevoegen aan dictionariy


def tabel_information_article_vullen(voorbeeldlijst_information_article, cnx):
    ###information article vullen

    pubmedid = voorbeeldlijst_information_article["PubMedID"]
    titel = voorbeeldlijst_information_article["Title"]
    year = voorbeeldlijst_information_article["Year_publication"]

    query = """INSERT INTO owe7_pg1.information_article (PubMedID, Title, Year_publication) VALUES({0}, '{1}', {2});""".format(pubmedid,titel,year)
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    cnx.commit()
    mycursor2.close()


def get_information_article(sessionID, cnx):
    ###information article id ophalen van de autheurs

    resultaat = {}
    id = sessionID

    query = """select * from owe7_pg1.author where idAuthor in (select Author_idAuthor from owe7_pg1.author_has_information_article where Information_article_idInformation_article = {0})""".format(id)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    for regel in myresult:
        print(regel)
        #hier nog toevoegen aan dictionariy


def tabel_author_vullen(voorbeeldlijst_author, cnx):
    ###author vullen

    voornaam = voorbeeldlijst_author["Initial"]
    achternaam = voorbeeldlijst_author["Last_name"]

    if not (voorbeeldlijst_author["Insertion"]):
        tussenvoegsel = voorbeeldlijst_author["Insertion"] = "NULL"
    else:
        tussenvoegsel = voorbeeldlijst_author["Insertion"] = "'[0]'".format(voorbeeldlijst_author["Insertion"])

    query = """insert into owe7_pg1.author (Initial, Insertion, Last_name) values ( '{0}', {1}, '{2}');""".format(voornaam, tussenvoegsel, achternaam)

    mycursor1 = cnx.cursor()
    mycursor1.execute(query)
    cnx.commit()
    mycursor1.close()


def get_session(sid, cnx):
    query = """select * from owe7_pg1.session where idSession = {0};""".format(sid)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    for regel in myresult:
        zoekwoorden = get_zoekwoorden(sid, cnx)
        titel = regel[1]
        datum = regel[2]
        sessie = Session(titel, datum, zoekwoorden)
        sessie.get_zoekwoorden()

    return sessie

def get_zoekwoorden(sid, cnx):
    query = """select * from owe7_pg1.search_query where idSearch_query in (select Search_query_idSearch_query from owe7_pg1.session_has_search_query where Session_idSession = {0});""".format(sid)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    zoekwoorden = []
    for regel in myresult:
        artikelen = get_articelen(regel[0], cnx)
        term = regel[1]
        zoekwoord = Zoekwoord(term, artikelen)
        zoekwoorden.append(zoekwoord)
    return zoekwoorden

def get_articelen(search_id, cnx):
    query = """select * from owe7_pg1.information_article where idInformation_article in (select Information_article_idInformation_article from owe7_pg1.information_article_has_search_query where Search_query_idSearch_query  = {0})""".format(search_id)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    artikelen = []
    for regel in myresult:
        authors = get_autheurs(regel[0], cnx)
        pubmedid = regel[1]
        titel = regel[2]
        publicatiedatum = regel[3]
        artikel = Artikel(pubmedid, titel, publicatiedatum, authors)


        artikelen.append(artikel)

    return artikelen

def get_autheurs(artikel_id, cnx):

    query = """select * from owe7_pg1.author where idAuthor in (select Author_idAuthor from owe7_pg1.author_has_information_article where Information_article_idInformation_article = {0})""".format(artikel_id)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    authors = []
    for regel in myresult:
        initial = regel[1]
        insertion = regel[2]
        last_name = regel[3]
        author = Author(initial, insertion, last_name)
        authors.append(author)

    return authors

main()