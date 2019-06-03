class Author(object):
    def __init__(self, initial, insertion, last_name):
        self.__initial = initial
        self.__insertion = insertion
        self.__last_name = last_name

    def get_initial(self):
        return str(self.__initial)

    def get_insertion(self):
        return str(self.__insertion)

    def get_last_name(self):
        return str(self.__last_name)

