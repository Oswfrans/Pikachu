from src.elo.data_prep import stack_it, prep_dict
from src.elo.rating_util import iter_frame, win_prob
from elo_config import path, positions1, positions2


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


if __name__ == "__main__":
    main()

#below here will need to go later

#at the end return two dataframes, player ratings and progressionlist (maybe player progression?)

# [x] streamline the win probablity function
# [x] Save player progression information ??
# [/] seperate and define all lol-specific stuff in configurable values
# [] seperate stuff over files and functions
# [] write docstrings for all the functions
# [x] make the code year agnostic
# [/] make sure all hardcoded stuff is seperated out
# [] add correct structure
# [] add tests
# [] add coverage % for the tests
# [] add pipenv structure to ensure correct dependencies
# [] seperate function that generates some graphs ?

#end result you want is modular clean code that cals the trueskill rating of teams for a given dataset and can then be used to predict the probabilty
#also useable as input for other models
#have a nice write up for r/leagueoflegends