import pandas as pd
import numpy as np

import trueskill
import itertools
from collections import defaultdict


path = "/Users/oswin/Projects/Python/Pikachu/leagueoflegends/" #"C:\\Users\\o.frans\\Downloads\\leagueoflegends\\"

df = pd.read_csv(path+"matchinfo.csv")

colors = ["red", "blue"]
positions = ["Top", "Jungle", "Middle", "ADC", "Support"]

#seperate by year
df2015 = df[(df.Year==2015)]
df2016 = df[(df.Year==2016)]
df2017 = df[(df.Year==2017)]
df2018 = df[(df.Year==2018)]

#for each unique player instantiate a rating object

def stackIT(dataframe) :
	#stack all unique players in one column
	#add teams to this
	dfList = []
	for pos in positions:
		for col in colors:
			#print(dataframe[col+pos].head)
			dfList.append(dataframe[[col+pos, col+"TeamTag"]].rename(index= str,columns={col+pos: "player", col+"TeamTag": "team"}) )

	#pd.concat([returnDF, dataframe[col+pos].rename(columns={col+pos, "player"}) ], ignore_index=True, axis=1 )
	return pd.concat(dfList, ignore_index=True).drop_duplicates()
	#return list(set(list(  pd.concat(dfList, ignore_index=True) ) ) )  #.groupby("player")

#this is a a df with all player teams combo
stacked2015 = stackIT(df2015)
#print(stacked2015)

#instantiate a trueskill rating object in a dict for all the players
player2015Dict = {}

for p in list(stacked2015["player"] ) :
	player2015Dict[p] = trueskill.Rating()


#here we have a dict of dicts
#create teams for these objects
teams2015Dict = defaultdict(lambda: [])

for index, row in stacked2015.iterrows(): #.itertuples(index=False):
	if row["team"] in teams2015Dict:
		#teams2015Dict[row["team"]] = teams2015Dict[row["team"]].append(player2015Dict[row["player"]])
		#teams2015Dict[row["team"]].append({ row["player"] : player2015Dict[row["player"]]})
		teams2015Dict[row["team"]][row["player"]] = player2015Dict[row["player"]]
#		if row["player"] in teams2015Dict[row["team"]]:
	#		pass
		#else:
			#teams2015Dict[row["team"]][row["player"]] = player2015Dict[row["player"]]
	else:	
		teams2015Dict[row["team"]] = { row["player"] : player2015Dict[row["player"]]} 

import itertools
import math

def win_probability(team1, team2, envir):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (envir.BETA * envir.BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)

from trueskill import Rating
from math import sqrt
from scipy import stats
from scipy.stats import norm


def Pwin(rAlist=[Rating()],  rBlist=[Rating()] ):
    deltaMu = sum( [x.mu for x in rAlist])  - sum( [x.mu for x in  rBlist])
    rsss = sqrt(sum( [x.sigma**2 for x in  rAlist]) + sum( [x.sigma**2 for x in rBlist]) )
    return norm.cdf(deltaMu/rsss)

"""
# calculate new ratings
rating_groups = [{p1: p1.rating, p2: p2.rating}, {p3: p3.rating}]
rated_rating_groups = env.rate(rating_groups, ranks=[0, 1])
# save new ratings
for player in [p1, p2, p3]:
    player.rating = rated_rating_groups[player.team][player]
"""

env = trueskill.global_env()

#should this be a list?
progressionList =[]

#could clean up the conditional assignment here
def pop_bench(team):
	enum_col_pos=  [row["red"+y] for y in positions] if team==blueTeam else [row["red"+y] for y in positions]
	for k in team.keys():
		if k not in enum_col_pos:
			team.pop(k, None)
	return team

#this should iter over all the matches and update the elos
for index, row in df2015.iterrows():
	#construct the teams from the playersdict
	redTeamPositions = ["red"+p for p in positions] #["redTop", "redMiddle", "redJungle", "redADC", "redSupport"]
	blueTeamPostions = ["blue"+p for p in positions] #["blueTop", "blueMiddle", "blueJungle", "blueADC", "blueSupport"]
	blueTeam = [player2015Dict[row[z]] for z in blueTeamPostions]
 	redTeam = [player2015Dict[row[z]] for z in redTeamPositions]
	
	bluePlayers= [row[z] for z in blueTeamPostions]
	redPlayers = [row[z] for z in redTeamPositions]
	
	#blueTeam = teams2015Dict[row['blueTeamTag']]
	#redTeam = teams2015Dict[row['redTeamTag']]

	#need to filter out players that are not playing
	#blueTeam = pop_bench(blueTeam)
	#redTeam = pop_bench(redTeam)

	#save current elo and win probability in a list or df
	#not sure if this works as well
	#this would then be the two teams, the predicted probability and the actual result
	progressionList.append( [ row['blueTeamTag'], row['redTeamTag'], Pwin(blueTeam, redTeam), row['bResult']  ] ) 

	#who won? based on who won update elo
	if row['bResult']==1:
		rated_rating_groups= env.rate( [blueTeam, redTeam] , ranks= [0,1] )
	else:
		rated_rating_groups= env.rate( [blueTeam, redTeam] , ranks=[1,0] )
	
	#!!!!!!!!!!!!!!
	# save new ratings
	#loop over the players and the raing objects
	for player in rated_rating_groups:
		
		player2015Dict[]

	#need to figure out how to properly assign credit
	print(rated_rating_groups)
	
	#what the code below here needs to do is update the player ratings in the teamsdict
	#we will update the player ratings at the end in the players dict
	#we cannot do that because of conflicting values of different players at the end
	#hence we need to update the player dict now

	#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#wait is it not better to basically only update the players?
	#then we have a single source of truth
	#if we only do team construction at inference
	#also prevents  hanging stuff

	#ok so in the teams2015dict we update the players that just played
	#teams2015Dict[row["blueTeamTag"]]

	#example
	for player in [p1, p2, p3]:
    	player.rating = rated_rating_groups[player.team][player]



	#doing this in an ugly way for now
	i=0
	for player in blueTeam + redTeam:
		print(len(blueTeam+redTeam))
		print(rated_rating_groups[1][1])
		#print(row['blueTeamTag'])
		if i <= 5:
			player.rating = rated_rating_groups[0][i]
		#	#player.rating = rated_rating_groups[player.team][player]
		elif i >5:
			print(i)
			player.rating = rated_rating_groups[1][i-5]
		i+=1

#here goes a function that updates the player ratings

print(win_probability("TSM","Cloud9", env))

#progressionList should be changed to dataframe?

#how do you deal with changing rosters ??
	#we need to update the individual player ratings in the dict
	#we need to check if all players are still the same 5 and if not chenge the dict and team dict
		#so for each match we check the rosters, then if mismatch, we get the rating object from the playerdict and we construct the new teamdict to use?
	
	
	# !!!!!problem right now is that we basically shove everything in a list instead of a dict!!!!

#I accept the limitation that we can only do one year for now

#at the end return three dataframes, team ratings, player ratings and progressionlist

#update ratings for matches
#iter over the matches
#based on matches you update the ratings

#at the end calc win probs of different teams

#how do we make it so that we can easily adept it to other type of files and other sports?
#some type of clojure-like description?
#we have functions that do the important things, then we describe what the specifics of our use case either in a seperate file or at the start of the file

#end result you want is modular clean code that cals the trueskill rating of teams for a given dataset and can then be used to predict the probabilty
#also useable as input for other models
#have a nice write up for r/leagueoflegends





