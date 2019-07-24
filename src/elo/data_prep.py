import pandas as pd
import trueskill


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