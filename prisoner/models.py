# -*- coding: utf-8 -*-
from otree.db import models
import otree.models


doc = """
Prisoner's dilemma game. Single treatment. Two players are asked separately whether they want to cooperate or Defect.
Their choices directly determine the payoffs.

<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/prisoner">here</a></p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'prisoner'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    betray_amount = models.MoneyField(
        doc="""amount a player makes if he chooses 'Defect' and the other chooses 'Cooperate'""",
        default=0.30,
    )

    friends_amount = models.MoneyField(
        doc="""amount both players make if both players choose 'Cooperate'""",
        default=0.20,
    )
    betrayed_amount = models.MoneyField(
        doc="""amount a player makes if he chooses 'Cooperate' and the other chooses 'Defect'""",
        default=0.10,
    )

    enemies_amount = models.MoneyField(
        doc="""amount both players make if both players choose 'Defect'""",
        default=0.00,
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        default=None, verbose_name='What is your decision?',
        choices=['Cooperate', 'Defect'],
        doc="""This player's decision"""
    )

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    def set_payoff(self):
        """Calculate player payoff"""
        payoff_matrix = {'Cooperate': {'Cooperate': self.treatment.friends_amount,
                                       'Defect': self.treatment.betrayed_amount},
                         'Defect':   {'Cooperate': self.treatment.betray_amount,
                                       'Defect': self.treatment.enemies_amount}}

        self.payoff = (payoff_matrix[self.decision]
                                    [self.other_player().decision])


def treatments():
    return [Treatment.create()]