import pandas as pd
import numpy as np

import trueskill
import itertools
from datetime import datetime
#from itertools import chain  #import itertools
from collections import defaultdict

import math
from trueskill import Rating
from math import sqrt
from scipy import stats
from scipy.stats import norm

from pikachu.elo_config import team1_tag_col, team2_tag_col, result_col


def win_prob(rAlist=[Rating()], rBlist=[Rating()]):
    """
    Function that calculates the win probability of the two rating lists
    rAlist :    list of ratings
    rBlist :    list of ratings
    return the probability that the first team will win as a float
    """
    deltaMu = sum([x.mu for x in rAlist]) - sum([x.mu for x in rBlist])
    rsss = sqrt(
        sum([x.sigma**2 for x in rAlist]) + sum([x.sigma**2 for x in rBlist]))
    return norm.cdf(deltaMu / rsss)


def iter_frame(player_dict, dataframe, position1, position2):
    """
    Function that iterates over the specified dataframe of match results and 
    updates the TrueSkill rating of the players in a dictionary object.
    Also results in lists that show the progression of the rating and predicitons over the matches
    player_dict :   Dictionary object of the players and the Trueskill rating. This is updated throughout the function
    dataframe :     Dataframe which contains the match result that are used to update the ratings
    position1 :     Column names detailling the different players in team1
    position2 :     Column names detailling the different players in team2
    returns the updated player_dict, a list of matchresults and predictions and a list showing the progression of individual players
    """
    progression_list = []
    progression_players = []
    #this should iter over all the matches and update the elos
    for index, row in dataframe.iterrows():
        #construct the teams from the playersdict

        team1 = [player_dict[row[z]] for z in position1]
        team2 = [player_dict[row[z]] for z in position2]

        players1 = [row[z] for z in position1]
        players2 = [row[z] for z in position2]

        #save current predicted win chance of the past and win probability in a list or df
        progression_list.append([
            row[team1_tag_col], row[team2_tag_col],
            win_prob(team1, team2), row[result_col]
        ])
        #save the rating
        progression_players.append(
            [[row[z], player_dict[row[z]],
              datetime.now()] for z in position1 + position2])

        player_dict = save_ratings(update_elo(row[result_col]),
                                   players1 + players2, player_dict)

    return player_dict, progression_list, progression_players


#function that creates new rating groups
def update_elo(first_win, envir, team1, team2):
    """
    Function that updates the rating objects based on who won
    first_win : boolean that is 1 if team1 won and 0 if team 2 won
    envir :     Trueskill environment object
    team1 :     list of rating objects of the players of the first team
    team2 :     list of rating object of the players of the second team
    returns a list of list of updated ratings of the players
    """
    if first_win == 1:
        rating_groups = envir.rate([team1, team2], ranks=[0, 1])
    else:
        rating_groups = envir.rate([team1, team2], ranks=[1, 0])

    return rating_groups


def save_ratings(groups, players, p_dict):
    """
    Function that updates the players dictionary with the new rating objects.
    groups :        a nested list of the new rating objects
    players :       List of players that have new ratings
    player_dict :   dictionary of players and their ratings, which you update 
    """
    # save new ratings
    i = 0
    for player in players:
        if i <= 4:
            p_dict[player] = groups[0][i]
        elif i > 4:
            p_dict[player] = groups[1][i - 5]
        i += 1
    return p_dict