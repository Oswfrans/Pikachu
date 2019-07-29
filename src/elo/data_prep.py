import pandas as pd
import trueskill
from Pikachu.elo_config import position1, position2


def stack_it(dataframe):
    """Stacks the dataframe so that all unique players are underneath eachother

    Args:
        dataframe: a dataframe which will be looped over to create a stacked dataframe
    Returns:
        The new stacked dataframe
    """
    #stack all unique players in one column
    df_list = []
    for z in position1 + position2:
        df_list.append(dataframe[[z]].rename(index=str, columns={z: "player"}))

    return pd.concat(dfList, ignore_index=True).drop_duplicates()

    # dfList = []
    # for pos in positions:
    #     for col in colors:
    #         dfList.append(dataframe[[col + pos, col + "TeamTag"
    #                                  ]].rename(index=str,
    #                                            columns={
    #                                                col + pos: "player",
    #                                                col + "TeamTag": "team"
    #                                            }))
    # return pd.concat(dfList, ignore_index=True).drop_duplicates()


#instantiate a trueskill rating object in a dict for all the players
def prep_dict(stckd):
    """Instantiates a trueskill rating object for each player and stores it in a dictionary

    Args:
        stkd : A dataframe containing a player column containing all the unique players to create objects for
    Returns:
        A dictionary consisting of player keys and rating objects
    """
    player_dict = {}

    for p in list(stckd["player"]):
        player_dict[p] = trueskill.Rating()
    return player_dict