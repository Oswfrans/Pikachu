import pandas as pd
import numpy as np

import trueskill
import itertools
from collections import defaultdict



path = "C:\\Users\\o.frans\\Downloads\\leagueoflegends\\"

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

#print(stackIT(df2015))

stacked2015 = stackIT(df2015)

player2015Dict = {}

for p in list(stacked2015["player"] ) :
	player2015Dict[p] = trueskill.Rating()
 
teams2015Dict = defaultdict(lambda: [])

for index, row in stacked2015.iterrows(): #.itertuples(index=False):
	if row["team"] in teams2015Dict:
		#teams2015Dict[row["team"]] = teams2015Dict[row["team"]].append(player2015Dict[row["player"]])
		teams2015Dict[row["team"]].append(player2015Dict[row["player"]])
		
	else:	
		teams2015Dict[row["team"]] = [ player2015Dict[row["player"]] ]

#create teams for these objects
for z in teams2015Dict.values() :
	print(z)

#update ratings for matches
#iter over the matches
#based on matches you update the ratings

#at the end calc win probs of different teams