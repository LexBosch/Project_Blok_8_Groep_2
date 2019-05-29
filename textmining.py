from collections import Counter
from itertools import combinations
from Bio import Entrez, Medline
import urllib.request

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
    Entrez.email = mail
    pubmedIDLijst = []
    for item in zoekQueryLijst:
        handle_first = Entrez.esearch(db="pubmed", term=item.lower(), retmax=50, retmode="xml")
        zoekResultaat = Entrez.read(handle_first)
        handle_first.close()
        pubmedIDLijst += zoekResultaat["IdList"]
    return pubmedIDLijst


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
    pass


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
    hoogste = info.most_common(10)
    for item in hoogste:
        hoogsteKeysLijst.append(item[0])

    return hoogsteKeysLijst


def textming_Start(ZoektermenLijst, aantal_zoeken, oldTermlist):
    oldTermlist += ZoektermenLijst
    aantal_zoeken = aantal_zoeken - 1
    zoekQueryLijst = query_maken(ZoektermenLijst)
    # print(zoekQueryLijst)
    pubmedIDLijst = zoekArtikelen(zoekQueryLijst)
    # print(pubmedIDLijst)
    results = zoekInformatie(pubmedIDLijst)
    # print(results)
    # pubmedArtikelenLijst = artikelLijstMaken(results)
    # artikelInfoDict =
    if aantal_zoeken > 0:
        term_list = keywordsLijst(results, oldTermlist)
        # print(term_list)
        hoogsteKeysLijst = filterterm_list(term_list)
        # print(hoogsteKeysLijst)
        print(hoogsteKeysLijst)
        return (results + textming_Start(hoogsteKeysLijst, aantal_zoeken, oldTermlist))
    # else:
    #     return artikelInfoDict
    return results

