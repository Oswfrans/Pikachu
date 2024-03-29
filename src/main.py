from Pikachu.src.elo.data_prep import stack_it, prep_dict
from Pikachu.src.elo.rating_util import iter_frame, win_prob
from Pikachu.elo_config import path, positions1, positions2
import pandas as pd
import trueskill


def main():
    #!!!!
    #figure out how to pass args and

    env = trueskill.global_env()

    df = pd.read_csv(path)
    stacked = stack_it(df)
    player_dict = prep_dict(stacked)

    player_dict, match_result, player_progression = iter_frame(
        player_dict, df, positions1, positions2)


if __name__ == "__main__":
    main()

#below here will need to go later

#at the end return two dataframes, player ratings and progressionlist (maybe player progression?)


# [] add coverage % for the tests
# [] ?makefile
# [] seperate function that generates some graphs ?

#end result you want is modular clean code that cals the trueskill rating of teams for a given dataset and can then be used to predict the probabilty
#also useable as input for other models
#have a nice write up for r/leagueoflegends
