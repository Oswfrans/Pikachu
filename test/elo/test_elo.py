#first everything in 1 file and tests for each function
#then multiple tests for each function
#then multiple files
import pytest
import pandas as pd
from Pikachu.data_prep import stack_it, prep_dict
from Pikachu.rating_util import win_prob,iter_frame, save_ratings,update_elo
from trueskill import Rating
#double check if necessary
import math
from math import sqrt
from scipy import stats
from scipy.stats import norm

def smoke_test():
    #placeholder value
    from_file =  0.69
    TSM = [
        player_dict[z]
        for z in ["Bjergsen", "Hauntzer", "Doublelift", "Amazing", "Xpecial"]
    ]
    Cloud9 = [
        player_dict[z]
        for z in ["Hai", "Sneaky", "Xpecial", "Balls", "Meteos"]
    ]

    print(win_prob(TSM, Cloud9))
    assert (win_prob(TSM, Cloud9) == from_file)


#data prep

#test for stackit function
def test_stack_it():
    sample = pd.DataFrame([["Doublelift","Hauntzer","Bjergsen", "Reginald","Xpecial",
	"Perkz", "Amazing","Lodnen","Miky","Farza"]], columns=["blueTop", "blueMiddle", "blueJungle", "blueADC", "blueSupport", "redTop", "redMiddle", "redJungle", "redADC", "redSupport"])
    results = pd.DataFrame([["Doublelift"],["Hauntzer"],["Bjergsen"], ["Reginald"],["Xpecial"],
	["Perkz"], ["Amazing"],["Lodnen"],["Miky"],["Farza"]], columns=["player"])
    #results = pd.read_csv(from_file)
    #sample = pd.read_csv(sample)
    assert(stack_it(sample)==results)

#test for playerdict function
def test_prep_dict():
    stacked = pd.DataFrame([["Doublelift"],["Hauntzer"],["Bjergsen"], ["Reginald"],["Xpecial"],
	["Perkz"], ["Amazing"],["Lodnen"],["Miky"],["Farza"]], columns=["player"]) 

    dict1 = {"Doublelift": Rating(),"Hauntzer": Rating(),"Bjergsen": Rating(),
    "Reginald": Rating(),"Xpecial": Rating(),
    "Perkz": Rating(), "Amazing":Rating(),"Lodnen": Rating(),"Miky":Rating(),"Farza": Rating()}

    assert(prep_dict(stacked)==dict1)

#rating util function

def test_win_prob():
    probability= 0.997227166342378
    assert(win_prob([Rating(30, 3)], [Rating(20, 2)])== probability)

#test for iter_frame function
#def test_iter_frame():

#test for update_elo function
def test_update_elo():
    envir = trueskill.global_env()

    team1 = [Rating(30,2), Rating(20,2)]
    team2 = [Rating(11, 1), Rating(40,4)]

    #these numbers are all wrong will need to fix
    #!!!!!!!!!!
    expected_rating_groups = [Rating(11,11), Rating(11,11) ]
    assert(update_elo(1, envir ,team1, team2)== expected_rating_groups)

#Do we need this?
#test for save_rating function


#example
# def test_scrape_website():
#     with open('%s/scrape_website_output.txt' % output_path, 'r') as scrape_website_output:
#         content = scrape_website_output.read()
#     assert scrape_website(website) == content