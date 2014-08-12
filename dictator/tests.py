import otree.test
from otree.common import Money, money_range
import dictator.views as views
from dictator.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # basic assertions
        assert (self.treatment.allocated_amount == 1.0)
        assert (self.match.players_per_match == 2)

        # start game
        self.submit(views.Introduction)

        # dictator
        if self.player.index_among_players_in_match == 1:
            self.play_p1()

        self.submit(views.Results)

    def play_p1(self):
        self.submit(views.Offer, {"offer_amount": random.choice(self.match.offer_choices())})


