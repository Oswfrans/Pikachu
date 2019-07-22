import pandas as pd
import numpy as np

import trueskill
import itertools
from collections import defaultdict

import itertools
import math

from trueskill import Rating
from math import sqrt
from scipy import stats
from scipy.stats import norm

path = "/Users/oswin/Projects/Python/Pikachu/leagueoflegends/"  #"C:\\Users\\o.frans\\Downloads\\leagueoflegends\\"

df = pd.read_csv(path + "matchinfo.csv")

colors = ["red", "blue"]
positions = ["Top", "Jungle", "Middle", "ADC", "Support"]

# seperate by year
df2015 = df[(df.Year == 2015)]
df2016 = df[(df.Year == 2016)]
df2017 = df[(df.Year == 2017)]
df2018 = df[(df.Year == 2018)]

# for each unique player instantiate a rating object


def stackIT(dataframe):
    #stack all unique players in one column
    #add teams to this
    dfList = []
    for pos in positions:
        for col in colors:
            # print(dataframe[col+pos].head)
            dfList.append(dataframe[[col + pos, col + "TeamTag"
                                     ]].rename(index=str,
                                               columns={
                                                   col + pos: "player",
                                                   col + "TeamTag": "team"
                                               }))

    #pd.concat([returnDF, dataframe[col+pos].rename(columns={col+pos, "player"}) ], ignore_index=True, axis=1 )
    return pd.concat(dfList, ignore_index=True).drop_duplicates()
    #return list(set(list(  pd.concat(dfList, ignore_index=True) ) ) )  #.groupby("player")


#this is a a df with all player teams combo
stacked2015 = stackIT(df2015)
#print(stacked2015)

#instantiate a trueskill rating object in a dict for all the players
player2015Dict = {}

for p in list(stacked2015["player"]):
    player2015Dict[p] = trueskill.Rating()


def win_probability(team1, team2, envir):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma**2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (envir.BETA * envir.BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)


def Pwin(rAlist=[Rating()], rBlist=[Rating()]):
    deltaMu = sum([x.mu for x in rAlist]) - sum([x.mu for x in rBlist])
    rsss = sqrt(
        sum([x.sigma**2 for x in rAlist]) + sum([x.sigma**2 for x in rBlist]))
    return norm.cdf(deltaMu / rsss)


env = trueskill.global_env()

# should this be a list?
progressionList = []

# could clean up the conditional assignment here
# def pop_bench(team):
#     enum_col_pos = [row["blue"+y] for y in positions] if team == blueTeam else [row["red"+y] for y in positions]
#     for k in team.keys():
#         if k not in enum_col_pos:
#             team.pop(k, None)
#     return team

#this should iter over all the matches and update the elos
for index, row in df2015.iterrows():
    #construct the teams from the playersdict
    redTeamPositions = [
        "red" + p for p in positions
    ]  #["redTop", "redMiddle", "redJungle", "redADC", "redSupport"]
    blueTeamPostions = [
        "blue" + p for p in positions
    ]  #["blueTop", "blueMiddle", "blueJungle", "blueADC", "blueSupport"]
    blueTeam = [player2015Dict[row[z]] for z in blueTeamPostions]
    redTeam = [player2015Dict[row[z]] for z in redTeamPositions]

    bluePlayers = [row[z] for z in blueTeamPostions]
    redPlayers = [row[z] for z in redTeamPositions]

    #save current elo and win probability in a list or df
    #not sure if this works as well
    #this would then be the two teams, the predicted probability and the actual result
    progressionList.append([
        row['blueTeamTag'], row['redTeamTag'],
        Pwin(blueTeam, redTeam), row['bResult']
    ])

    #who won? based on who won update elo
    if row['bResult'] == 1:
        rated_rating_groups = env.rate([blueTeam, redTeam], ranks=[0, 1])
    else:
        rated_rating_groups = env.rate([blueTeam, redTeam], ranks=[1, 0])

    # save new ratings
    # loop over the players and the raing objects

    #example
    # for player in [p1, p2, p3]:
    #     player.rating = rated_rating_groups[player.team][player]

    i = 0
    for player in bluePlayers + redPlayers:
        if i <= 5:
            player2015Dict[player] = rated_rating_groups[0][i]
        #	#player.rating = rated_rating_groups[player.team][player]
        elif i > 5:
            print(i)
            player2015Dict[player] = rated_rating_groups[1][i - 5]
        i += 1

# create dataframe with player progress and deliver as csv function

# this should go in a test eventually
TSM = [
    player2015Dict[z]
    for z in ["Bjergsen", "Hauntzer", "Doublelift", "Amazing", "Biofrost"]
]
Cloud9 = [
    player2015Dict[z]
    for z in ["Hai", "Sneaky", "Lemonnation", "Balls", "Meteos"]
]

print(win_probability(TSM, Cloud9, env))

#at the end return two dataframes, player ratings and progressionlist (maybe player progression?)

# [] streamline the win probablity function
# [] Save player progression information ??
# [] seperate stuff over files and functions
# [] write docstrings for all the functions
# [] make the code year agnostic
# [] make sure all hardcoded stuff is seperated out
# [] add correct structure
# [] add tests
# [] add pipenv structure to ensure correct dependencies
# [] seperate function that generates some graphs ?

#end result you want is modular clean code that cals the trueskill rating of teams for a given dataset and can then be used to predict the probabilty
#also useable as input for other models
#have a nice write up for r/leagueoflegends