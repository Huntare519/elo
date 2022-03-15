from unicodedata import name


class player:
    ' documentation placeholder'

    def __init__(self, fname, lname, starting_elo=1000):
        self.first_name = fname
        self.last_name = lname
        self.elo = starting_elo

    def get_name(self):
        return self.first_name + self.last_name

    def get_elo(self):
        return self.elo
