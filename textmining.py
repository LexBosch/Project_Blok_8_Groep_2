from collections import Counter
from itertools import combinations
from Bio import Entrez, Medline
from artikel import Artikel
import urllib.request
import artikel
import author

mail = "lexbosch@live.nl"

def query_maken(Zoektermenlijst):
    querystring = ""
    zoekQueryLijst = []
    zoekcombinaties = combinations(Zoektermenlijst, 2)
    for i in list(zoekcombinaties):
        zoek1 = i[0]
        zoek2 = i[1]
        querystring = zoek1 + " AND " + zoek2
        zoekQueryLijst.append(querystring)
    return zoekQueryLijst


def zoekArtikelen(zoekQueryLijst):
    PubmedResult = []
    Entrez.email = mail
    articleObject = []
    for item in zoekQueryLijst:
        handle_first = Entrez.esearch(db="pubmed", term=item, retmax=100, retmode="xml")
        zoekResultaat = Entrez.read(handle_first)
        handle_first.close()
        pubmedIDLijst = zoekResultaat["IdList"]
        try:
            PubmedResult = zoekInformatie(pubmedIDLijst)
            articleObject += (createArticleObject(PubmedResult))
        except UnboundLocalError as ule:
            #No articles found
            pass
            print("errored")
    return PubmedResult, articleObject


def zoekInformatie(pubmedIDLijst):
    ids = ', '.join(pubmedIDLijst)
    handle_seccond = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="xml")
    try:
        results = Entrez.read(handle_seccond)["PubmedArticle"]
    except RuntimeError:
        # todo: exceptionhandeling
        print()
    return results


def artikelLijstMaken(results):
    # todo functie uitwerken
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
                    except KeyError:
                        temp_name_dict = {}
            except KeyError:
                name_dict.append({"fore": "No authors found", "last": ""})
                article_dict["Author"] = name_dict
            except TypeError:
                print()
            if article_dict:
                all_article_dicts.append(article_dict)
    return all_article_dicts

def objectmaken(all_article_dicts):
    artikel.Artikel_vullen(all_article_dicts)



def keywordsLijst(results, oldTermlist):
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
    hoogsteKeysLijst = []
    info = Counter(term_list)
    hoogste = info.most_common(5)
    for item in hoogste:
        hoogsteKeysLijst.append(item[0])
    return hoogsteKeysLijst


def createArticleObject(ArticleList):
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
            except TypeError:
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
                    #No authors found
                    pass
        except IndexError:
            pass
    return newArticleList



def createAuthorObject(AuthorList):
    newAuthorList = []
    for singleAuthor in AuthorList:
        try:
            newAuthorList.append(author.Author(
                singleAuthor["Initials"],
                "",
                singleAuthor["LastName"]
            ))
        except KeyError:
            #Author not correctly noted
            pass
    return newAuthorList


def textming_Start(ZoektermenLijst, aantal_zoeken, oldTermlist):
    oldTermlist += ZoektermenLijst
    aantal_zoeken = aantal_zoeken - 1
    zoekQueryLijst = query_maken(ZoektermenLijst)
    # print(zoekQueryLijst)
    results, pubmedIDLijst = zoekArtikelen(zoekQueryLijst)
    # print(pubmedIDLijst)
  #  results, ArticleTermList = zoekInformatie(pubmedIDLijst)
    # print(results)
   # all_article_dicts = artikelLijstMaken(results)
   # objectmaken(all_article_dicts)
    # artikelInfoDict =
    if aantal_zoeken > 0:
        term_list = keywordsLijst(results, oldTermlist)
        # print(term_list)
        hoogsteKeysLijst = filterterm_list(term_list)
        # print(hoogsteKeysLijst)
        print(hoogsteKeysLijst)
        NewpubmedIDLijst, oldtermlist = textming_Start(hoogsteKeysLijst, aantal_zoeken, oldTermlist)
        return (pubmedIDLijst + NewpubmedIDLijst), oldtermlist
    # else:
    #     return artikelInfoDict
    return pubmedIDLijst, oldTermlist

