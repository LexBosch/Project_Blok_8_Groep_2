# Auteur: Carleen
# webapplicatie textmingV1.2

from collections import Counter
from itertools import combinations
from Bio import Entrez
from Object import artikel, author
import re

mail = "lexbosch@live.nl"


def query_maken(Zoektermenlijst):
    """Query maken
    Deze methode zet de termen die zijn ingevuld op de website in een lijst.
    input: Zoektermenlijst: (String)
    return zoekQueryLijst: [Lijst van Strings]
    """
    querystring = ""
    zoekQueryLijst = []
    zoekcombinaties = combinations(Zoektermenlijst, 2)
    for i in list(zoekcombinaties):
        zoek1 = i[0]
        zoek2 = i[1]
        querystring = "(" + zoek1 + ") AND (" + zoek2 + ")"
        zoekQueryLijst.append(querystring)
    return zoekQueryLijst


def zoekArtikelen(zoekQueryLijst):
    """zoekArtikelen
    Deze functie zoekt met de zoektermen die in de zoekQueryLijst staan naar artikelen op pubmed.
    De ID's van de gevonden artikelen worden in PubmedIDLijst gezet.
    :param zoekQueryLijst: [Lijst van Strings]
    :return: PubmedResult: [Lijst van Pubmedoutput]
    :return: articleObject: [lijst van artikelen]
    """
    PubmedResult = []
    terms = []
    Entrez.email = mail
    articleObject = []
    for item in zoekQueryLijst:
        handle_first = Entrez.esearch(db="pubmed", term=item, retmax=100, retmode="xml")
        zoekResultaat = Entrez.read(handle_first)
        terms += getMeshTerms(zoekResultaat, terms)
        handle_first.close()
        pubmedIDLijst = zoekResultaat["IdList"]
        try:
            PubmedResult = zoekInformatie(pubmedIDLijst)
            articleObject += (createArticleObject(PubmedResult))
        except UnboundLocalError as ule:

            pass
            print("errored")
    return PubmedResult, articleObject, terms


def getMeshTerms(meshTrack, foundTerms):
    MeshTermList = []
    for searchTerm in meshTrack["TranslationSet"]:
        if not searchTerm["From"] in turnToList(foundTerms):
            newMashTerms = {"From": searchTerm["From"].lower(),
                            "To": []
                            }
            listWithNewTerms = searchTerm["To"].split(" OR ")
            for singleNewTerm in listWithNewTerms:
                if "AND" not in singleNewTerm:
                    result = re.search('"(.*)"', singleNewTerm)
                    resultingTerm = result.group(1)
                    if not resultingTerm in newMashTerms["To"]:
                        newMashTerms["To"].append(resultingTerm.lower())
            MeshTermList.append(newMashTerms)
    return MeshTermList


def turnToList(ListWithDicts):
    newlist = []
    for dict in ListWithDicts:
        newlist.append(dict["From"])
    return newlist


def zoekInformatie(pubmedIDLijst):
    """zoekInformatie
    Deze functie haalt per Id de informatie van de artikelen op.
    :param pubmedIDLijst: [lijst van Strings]
    :return: results: pubmedoutput
    """
    ids = ', '.join(pubmedIDLijst)
    handle_seccond = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="xml")
    try:
        results = Entrez.read(handle_seccond)["PubmedArticle"]
    except RuntimeError as RT:
        RT.args
        # todo: exceptionhandeling
        print()
    return results


<<<<<<< HEAD
def artikelLijstMaken(results):
    """artikelLijstMaken
    Deze functie haalt de informatie van elk artikel op en zet dit in een lijst.
    :param results: pubmedoutput
    :return: all_article_dicts [lijst van Stringelementen]
    """
    term_list = {}
    all_article_dicts = []
    for paper in results:
        if paper:
            article_dict = {}
            try:
                # PubmedIDs
                article_dict["ID"] = paper["MedlineCitation"]["PMID"]
                # Artikel data (Deze mist nogal vaak)
                article_dict["year"] = paper["MedlineCitation"]["DateCompleted"]["Year"]
                # Titel van het artikel
                article_dict["title"] = paper["MedlineCitation"]["Article"]["ArticleTitle"]
                # Authors van het artikel
                name_dict = []
                for author in paper["MedlineCitation"]["Article"]["AuthorList"]:
                    temp_name_dict = {"fore": author["Initials"], "last": author["LastName"]}
                    name_dict.append(temp_name_dict)
                article_dict["Author"] = name_dict
                # temp

                # endtemp
            except KeyError:
                # PubmedIDs
                article_dict["ID"] = paper["MedlineCitation"]["PMID"]
                # Artikel data (Deze mist nogal vaak)
                article_dict["year"] = "Onbekend"
                # Titel van het artikel
                article_dict["title"] = paper["MedlineCitation"]["Article"]["ArticleTitle"]
                # Authors van het artikel
                name_dict = []
            try:
                for author in paper["MedlineCitation"]["Article"]["AuthorList"]:
                    try:
                        temp_name_dict = {"fore": author["Initials"], "last": author["LastName"]}
                        name_dict.append(temp_name_dict)
                    except KeyError as KE:

                        temp_name_dict = {}
            except KeyError:
                name_dict.append({"fore": "No authors found", "last": ""})
                article_dict["Author"] = name_dict
            except TypeError as TE:

                print()
            if article_dict:
                all_article_dicts.append(article_dict)
    return all_article_dicts





def keywordsLijst(results, oldTermlist):
    """keywordsLijst
    Deze functie maakt een dictionary aan met keywords en het aantal keer hoe vaak ze voorkomen.
    :param results: [lijst van strings]
    :param oldTermlist: [lijst van String]
    :return: term_list: {term : Count}
    """
    term_list = {}
    for paper in results:
        try:
            keyword = paper['MedlineCitation']['KeywordList'][0]
            for term in keyword:
                term = term.lower()
                if not term in oldTermlist:
                    if term in term_list:
                        term_list[term] += 1
                    else:
                        term_list[term] = 1
        except TypeError:
            pass
        except IndexError:
            pass
    return term_list


def filterterm_list(term_list):
    """filterterm_list
    Deze functie pakt de termen die het vaakst voorkomen en zet deze in een lijst.
    :param term_list: {term : count}
    :return: hoogsteKeyLijst: [lijst van Strings]
    """
    hoogsteKeysLijst = []
    info = Counter(term_list)
    hoogste = info.most_common(5)
    for item in hoogste:
        hoogsteKeysLijst.append(item[0].lower())
    return hoogsteKeysLijst


def createArticleObject(ArticleList):
    """createArticleObject
    Deze functie haalt informatie uit de artikelen en zet deze in een dictionary en vervolgens in een lijst.
    :param ArticleList: pubmedoutput
    :return: newArticleList: [{lijst van dictionaries}]
    """
    newArticleList = []
    for singleArticle in ArticleList:
        articleAndTermsDict = {}
        try:
            articleAndTermsDict["articleObject"] = (artikel.Artikel(
                singleArticle["MedlineCitation"]["PMID"],
                singleArticle["MedlineCitation"]["Article"]["ArticleTitle"],
                singleArticle["MedlineCitation"]["DateCompleted"]["Year"],
                createAuthorObject(singleArticle["MedlineCitation"]["Article"]["AuthorList"])
            ))
            articleAndTermsDict["terms"] = singleArticle['MedlineCitation']['KeywordList'][0]
            newArticleList.append(articleAndTermsDict)
        except KeyError:
            try:
                articleAndTermsDict["articleObject"] = (artikel.Artikel(
                    singleArticle["MedlineCitation"]["PMID"],
                    singleArticle["MedlineCitation"]["Article"]["ArticleTitle"],
                    singleArticle["MedlineCitation"]["Article"]["ArticleDate"]["Year"],
                    createAuthorObject(singleArticle["MedlineCitation"]["Article"]["AuthorList"])
                ))
                articleAndTermsDict["terms"] = singleArticle['MedlineCitation']['KeywordList'][0]
                newArticleList.append(articleAndTermsDict)

            except IndexError:
                print("dateError")
            except TypeError as TE:
                TE.args
                try:
                    articleAndTermsDict["articleObject"] = (artikel.Artikel(
                        singleArticle["MedlineCitation"]["PMID"],
                        singleArticle["MedlineCitation"]["Article"]["ArticleTitle"],
                        singleArticle["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"],
                        createAuthorObject(singleArticle["MedlineCitation"]["Article"]["AuthorList"])
                    ))
                    articleAndTermsDict["terms"] = singleArticle['MedlineCitation']['KeywordList'][0]
                    newArticleList.append(articleAndTermsDict)

                except IndexError:
                    pass
                except KeyError:
                    # No authors found
                    pass
        except IndexError:
            pass
    return newArticleList


def createAuthorObject(AuthorList):
    """createAuthorObject
    Deze functie haalt de initialen en achternaam uit een lijst.
    :param AuthorList: pubmedoutput
    :return: newAuthorList : [lijst van String]
    """
    newAuthorList = []
    for singleAuthor in AuthorList:
        try:
            newAuthorList.append(author.Author(
                singleAuthor["Initials"],
                "",
                singleAuthor["LastName"]
            ))
        except KeyError:
            # Author not correctly noted
            pass
    return newAuthorList


def textming_Start(ZoektermenLijst, aantal_zoeken, oldTermlist):
    """textmining_Start
    Functie die verschillende andere functies aanroept.
    Deze functie zorgt ook voor de uiteindelijke resultaten.
    :param ZoektermenLijst: [lijst van Strings]
    :param aantal_zoeken: (Int)
    :param oldTermlist: [lijst van Strings]
    :return: PubmedIDLijst: [lijst van Strings]
    :return: oldTermList: [lijst van Strings]
    """
    aantal_zoeken = aantal_zoeken - 1
    zoekQueryLijst = query_maken(ZoektermenLijst)
    results, pubmedIDLijst, termsWithMesh = zoekArtikelen(zoekQueryLijst)
    oldTermlist += termsWithMesh
    if aantal_zoeken > 0:
        term_list = keywordsLijst(results, oldTermlist)
        hoogsteKeysLijst = filterterm_list(term_list)
        NewpubmedIDLijst, oldtermlist = textming_Start(hoogsteKeysLijst, aantal_zoeken, oldTermlist)
        return (pubmedIDLijst + NewpubmedIDLijst), oldtermlist
    return pubmedIDLijst, oldTermlist
