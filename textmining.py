from collections import Counter
from itertools import combinations
from Bio import Entrez, Medline
mail = "lexbosch@live.nl"

##print("hoi", Zoektermen)

def filterKeywords(new_data_term_list):
    lijst = []
    for item in new_data_term_list.keys():
        lijst.append(item)
        #print(lijst)
        #print(new_data_term_list)
        newdict = {}
        info = Counter(new_data_term_list)
        hoogste = info.most_common(4)
        for item in hoogste:
            newdict.update({item[0] : item[1]})
            print(item[0], " :", item[1])

    print(newdict)
    return lijst

def combineerTermen(Zoektermen, lijst):
    zoeklijst = []
    lijt2 = []
    zoeken = Zoektermen.split(" AND ")
    lijt2  = zoeken

    print("tweedelijst", lijt2)
    nieuwe_lijst = lijst + lijt2
    print(nieuwe_lijst)
    zoekstring = ""
    combinaties = combinations(nieuwe_lijst, 2)
    for i in list(combinaties):
        zoekterm1 = i[0]
        zoekterm2 = i[1]
        zoekstring = zoekterm1 + " AND " + zoekterm2
        zoeklijst.append(zoekstring)
        zoek_Extra_Artikelen(zoekstring)
    return zoeklijst


def zoek_Extra_Artikelen(zoekstring):
    titel = ""
    count=0
    titellijst = []
    Entrez.email = mail
    handle = Entrez.esearch(db="pubmed", term=zoekstring, retmax=463)
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]
    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    for record in records:
        titel = record.get("TI", "?")
        titellijst.append(titel)
        count += 1
        print("runtime", count)
        print(zoekstring)
        print(idlist)
        print(titellijst)
        print(count)



