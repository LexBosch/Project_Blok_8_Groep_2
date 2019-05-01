from Bio import Entrez


# Autor: Lex Bosch 31-04-2018
# Class able to process terms to PubMed query utilizing BioPython
class PubMedMining:
    # String containing the terms of the query
    term = ""
    # Email used to register yourself to the PubMed database
    mail = ""
    # List with resulting ID's
    id_list = []
    # List with resulting details of ID's
    result_list = []

    # Initializer For the class
    # Input:    am_mining: integer: amount of ID's to be returned
    #           mail: String: Email to be submitted to PubMed
    def __init__(self, am_mining, mail):
        self.amount_mining = am_mining
        self.mail = mail

    # Adds terms to the term query
    # Input:    term: String: Term to be appended to the PubMed query
    #           operator: String: NOT, OR or AND.
    def add_term(self, term, operator):
        if self.term == "":
            self.term = term
        else:
            if operator != "AND" and operator != "NOT" and operator != "OR":
                raise TypeError("Only functional operators are AND, NOT and OR")
            else:
                self.term += operator + "({0})".format(term)

    # Starts the ID PubMed search using the term String
    # Output: Creates a list containing the ID's of the articles
    #          Returns false if no details are found
    def start_id_search(self):
        Entrez.email = self.mail
        handle = Entrez.esearch(db='pubmed',
                                sort='relevance',
                                retmax=self.amount_mining,
                                retmode='xml',
                                term=self.term)
        results = Entrez.read(handle)
        self.id_list = results

    # Starts the search of the details using the ID list
    # Output: Create list containing all the details
    def start_details_search(self):
        if not self.id_list:
            return False
        else:
            Entrez.email = self.mail
            ids = ','.join(self.id_list)
            handle = Entrez.efetch(db='pubmed',
                                   retmode='xml',
                                   id=ids)
            try:
                self.result_list = Entrez.read(handle)["PubmedArticle"]
            except RuntimeError:
                return False

    # Returns the ID list
    # Output: id_list
    def get_id_list(self):
        return self.id_list

    # Return the details list
    # Output: result_list
    def get_details_list(self):
        return self.result_list
