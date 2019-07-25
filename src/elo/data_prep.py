import pandas as pd
import trueskill
from Pikachu.elo_config import position1, position2

#fix these functions
#make it dependent on the confiq
#add docstring

def stack_it(dataframe):
    """
    Stack all unique players in one column
    dataframe :     Dataframe of which all unique players are taken and put underneath eachother
    returns a dataframe
    """
    #stack all unique players in one column

    df_list = []
    for z in position1+position2:
        df_list.append(dataframe[[z]].rename(index=str, columns={z : "player"}))

    #need to test if new versions works as intended
    # for pos in positions:
    #     for col in colors:
    #         df_list.append(dataframe[[col + pos, col + "TeamTag"
    #                                  ]].rename(index=str,
    #                                            columns={
    #                                                col + pos: "player",
    #                                                col + "TeamTag": "team"
    #                                            }))

    return pd.concat(df_list, ignore_index=True).drop_duplicates()


#instantiate a trueskill rating object in a dict for all the players
def prep_dict(stckd):
    """
    Function that prepares a dictionary of keys of all the players and values
    of all their rating objects
    stckd : Dataframe of all the players stacked underneath eachother
    returns a dictionary of all the players and their rating objects
    """
    player_dict = {}

    for p in list(stckd["player"]):
        player_dict[p] = trueskill.Rating()
    return player_dict