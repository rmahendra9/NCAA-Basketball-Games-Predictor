# NCAA-Basketball-Games-Predictor

This repo contains models aimed at predicting the outcomes of NCAA Men's Division I Basketball Tournament.

## Acknowledgements

I want to acknowledge Bart Torvik (https://barttorvik.com/#) as the data for NCAA Basketball teams was pulled from there.

## The Motivation

The idea for this project is inspired by this paper on using a kNN methodology to predict the winners of the NCAA March Madness Tournament (https://engineering.purdue.edu/KongLab/publications/NCAABracketSelection_Kong.pdf). In this paper, the author used Pythagorean Expectation to find similarity scores between teams and used this data to predict games in March Madness. 

## The Idea

For this project, instead of Pythagorean Expectation, Adjusted Offensive (AdjOE) and Defensive Efficieny (AdjDE) were used. The reason for this choice is that Pythagorean Expectation is an estimate of a team's winning chance against an average D1 team while AdjOE and AdjDE are more concrete stats we can use to examine similarities between teams. Thus, the idea for the model is simple; to predict a matchup between team A and B:

1. Get the 25 most similar teams that A played in the regular season to team B based on AdjOE and AdjDE
2. If team A won against them, add the similarity score between that team and B to W<sub>A,B</sub>, else add it to L<sub>A,B</sub>
3. Repeat for team B to get W<sub>B,A</sub> and L<sub>B,A</sub>
4. The probability that team A beats team B is P<sub>A,B</sub> = (W<sub>A,B</sub> + L<sub>B,A</sub>) / (W<sub>A,B</sub> + L<sub>A,B</sub> + W<sub>B,A</sub> + L<sub>B,A</sub>)

## Preliminaries

All the libraries needed for this project are in the requirements.txt file so just install them with:

``` pip install -r requirements.txt ```

## The Datascraper

The file game_log_datascraper.py contains the method for getting information on game logs for every D1 college basketball team. This produces a file called NCAA_Game_Log.csv

``` python src/game_log_datascraper.py ```

The file school_stats_datascaper.py contains the method for getting tempo free stats for each college basketball team. This produces a file called NCAA_School_Stats_Tempo_Free.csv

``` python src/school_stats_datascraper.py ```

## The Model

Once the datascrapers have been run and the csv files have been produced, you can run the model like this:

``` python src/knn_model_regular_season.py  <Team A> <Team B>```

This will give you the chance that Team A beats Team B.

