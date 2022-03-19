class Player:
    ' documentation placeholder'

    def __init__(self, fname, num_games=0, starting_elo=1000):
        self.first_name = fname
        self.num_games = num_games
        self.elo = starting_elo

    def get_games(self):
        return self.num_games

    def get_name(self):
        return self.first_name

    def get_elo(self):
        return self.elo
