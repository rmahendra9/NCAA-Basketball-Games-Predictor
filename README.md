# NCAA-March-Madness-Bracket-Predictor

This repo contains models aimed at predicting the outcomes of the NCAA Division I Men's Basketball Tournament.

## The Datascraper

The file datascraper.py contains the method for getting information to train the models on. We are primarily interested in scraping individual game logs of all D1 schools. The scraper pulls data from Sports-Reference, so if the scraper is applied to another website, it might not work. Moreover, the URL that the scraper pulls data from must be changed each season, as it will need to scrape data from the newer season of college basketball. The scraper will output a CSV file containing the game logs of all D1 schools. To use the scraper, simply type: 

``` python datascraper.py ```
