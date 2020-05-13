"""
Scoreboard Class
"""

class Scoreboard():

    def __init__(self):
        """
        Initialize an empty string for now, will take active player array
        and sort accordingly
        """

        self.sorted_scores = []

    def get_score(self, active_players):
        """
        Loads active players array, strips score and player name to sort into array
        """
        self.sorted_scores = []

        def Sort(sub_li):
            return(sorted(sub_li, key = lambda x: x[1], reverse=True))

        for player in active_players:
            self.sorted_scores.append([player.name, player.score])

        return Sort(self.sorted_scores)
