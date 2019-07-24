#these all should go in the config file
path = "/Users/oswin/Projects/Python/Pikachu/data/matchinfo.csv"  #"C:\\Users\\o.frans\\Downloads\\data\\"

colors = ["red", "blue"]
positions = ["Top", "Jungle", "Middle", "ADC", "Support"]

positions1 = [
    "blue" + p for p in positions
]  #["blueTop", "blueMiddle", "blueJungle", "blueADC", "blueSupport"]

positions2 = ["red" + p for p in positions
              ]  #["redTop", "redMiddle", "redJungle", "redADC", "redSupport"]

#this will also be args in the future or at least config file
team1_tag_col = "blueTeamTag"
team2_tag_col = "redTeamTag"
result_col = "bResult"