# Pikachu
This is a simple project to calculate Trueskill ratings for a competive endeavor on the basis of a result csv file using the Trueskill library.
This library can be found here [https://github.com/sublee/trueskill] and you can read more regarding this rating system itself here [http://www.moserware.com/2010/03/computing-your-skill.html].
Currently it is configured to work with the Kaggle dataset of League of Legends, but in principal with minor tweaking it can work on any sport which has clear winners and losers. The file structure should be structured in a way in which each row is a match and there is a column for match results and seperate columns for each player (if individual rating is desired) and two columns that indicate the teams playing.

This project could be extended to use the Trueskill rating as input of a machine learning model to be able to say even more regarding the probability of a victory.

I also used this small project to try out the pipenv project setup, please let me know if there is anything I can do to increase the quality.