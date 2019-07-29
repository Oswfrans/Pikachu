#first everything in 1 file and tests for each function
#then multiple tests for each function
#then multiple files


def smoke_test():
    #placeholder value
    from_file = 0, 69
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

#test for playerdict function

#rating util function

#test for win_prob function

#test for iter_frame function

#test for update_elo function

#test for save_rating function

#example
# def test_scrape_website():
#     with open('%s/scrape_website_output.txt' % output_path, 'r') as scrape_website_output:
#         content = scrape_website_output.read()
#     assert scrape_website(website) == content