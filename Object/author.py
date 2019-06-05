class Author(object):
    """
    Class object of the Authors of pubmed articles
    """
    def __init__(self, initial, insertion, last_name):
        """
        Initialyzes the Author object
        :param initial: Initials of the Author
        :param insertion: Insertion of the Author
        :param last_name: Last name of the Author
        """
        self.__initial = initial
        self.__insertion = insertion
        self.__last_name = last_name

    def get_initial(self):
        """
        returns the Authors initals
        :return: Authors initals
        """
        return str(self.__initial)

    def get_insertion(self):
        """
        returns authors insertions
        :return: authors insertions
        """
        return str(self.__insertion)

    def get_last_name(self):
        """
        Returns authors last name
        :return: authors last name
        """
        return str(self.__last_name)

