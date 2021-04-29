# US Mass Shootings over the last 3 years

## Overview
This website displays US Mass Shootings data scraped from Wikipedia 'List of mass shootings in the United States'.
year : 2018 - 2021 (data for 2021 are the updated ones by the date the database is created)
url: https://en.wikipedia.org/wiki/List_of_mass_shootings_in_the_United_States_in_2021

## Files
This project consists of two python files
1. data scraping and database (scrap data and create databases): run this file first to create databases required for 2. data visualization
2. data visualization (pull scraped data and display graphs)

## Features (data visualization)
- a heatmap that compares the number of US Mass Shootings incidents across states by year user selected
- a line graph that shows the number of victims over the past 3 years by state user selected
- a bar chart that shows the number of victims in cities in state user selected
- a table that lists all the incidents (including description) of US Mass Shoointgs in the year user selected

## Python Packages Used
- bs4
- flask
- requests
- plotly
- pandas
