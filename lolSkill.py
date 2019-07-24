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

#these all should go in the config file
path = "/Users/oswin/Projects/Python/Pikachu/data/matchinfo.csv"  #"C:\\Users\\o.frans\\Downloads\\data\\"

#df = pd.read_csv(path + "matchinfo.csv")
colors = ["red", "blue"]
positions = ["Top", "Jungle", "Middle", "ADC", "Support"]

positions1 = [
    "blue" + p for p in positions
]  #["blueTop", "blueMiddle", "blueJungle", "blueADC", "blueSupport"]

positions2 = ["red" + p for p in positions
              ]  #["redTop", "redMiddle", "redJungle", "redADC", "redSupport"]

# seperate by year
# df2015 = df[(df.Year == 2015)]
# df2016 = df[(df.Year == 2016)]
# df2017 = df[(df.Year == 2017)]
# df2018 = df[(df.Year == 2018)]


def stack_it(dataframe):
    #stack all unique players in one column
    #add teams to this
    dfList = []
    for pos in positions:
        for col in colors:
            dfList.append(dataframe[[col + pos, col + "TeamTag"
                                     ]].rename(index=str,
                                               columns={
                                                   col + pos: "player",
                                                   col + "TeamTag": "team"
                                               }))
    return pd.concat(dfList, ignore_index=True).drop_duplicates()


#instantiate a trueskill rating object in a dict for all the players
def prep_dict(stckd):
    player_dict = {}

    for p in list(stckd["player"]):
        player_dict[p] = trueskill.Rating()
    return player_dict


def win_prob(rAlist=[Rating()], rBlist=[Rating()]):
    deltaMu = sum([x.mu for x in rAlist]) - sum([x.mu for x in rBlist])
    rsss = sqrt(
        sum([x.sigma**2 for x in rAlist]) + sum([x.sigma**2 for x in rBlist]))
    return norm.cdf(deltaMu / rsss)


def main():
    #!!!!
    #figure out how to pass args and

    env = trueskill.global_env()
    # should this be a list?
    #works but note for future optimization

    df = pd.read_csv(path)
    stacked = stack_it(df)
    player_dict = prep_dict(stacked)

    player_dict, match_result, player_progression = iter_frame(
        player_dict, df, position1, position2)


#this will also be args in the future or at least config file
team1_tag_col = "blueTeamTag"
team2_tag_col = "redTeamTag"
result_col = "bResult"


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


# create dataframe with player progress and deliver as csv function

# this should go in a test eventually
TSM = [
    player_dict[z]
    for z in ["Bjergsen", "Hauntzer", "Doublelift", "Amazing", "Xpecial"]
]
Cloud9 = [
    player_dict[z] for z in ["Hai", "Sneaky", "Xpecial", "Balls", "Meteos"]
]

print(win_prob(TSM, Cloud9))
#print(win_probability(TSM, Cloud9, env))

#at the end return two dataframes, player ratings and progressionlist (maybe player progression?)

# [x] streamline the win probablity function
# [x] Save player progression information ??
# [/] seperate and define all lol-specific stuff in configurable values
# [] seperate stuff over files and functions
# [] write docstrings for all the functions
# [x] make the code year agnostic
# [] make sure all hardcoded stuff is seperated out
# [] add correct structure
# [] add tests
# [] add coverage % for the tests
# [] add pipenv structure to ensure correct dependencies
# [] seperate function that generates some graphs ?

#end result you want is modular clean code that cals the trueskill rating of teams for a given dataset and can then be used to predict the probabilty
#also useable as input for other models
#have a nice write up for r/leagueoflegends