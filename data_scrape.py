# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:58:19 2020

@author: Jason
"""

import pandas as pd
import numpy as np
import os

#Define working directory
os.chdir('C:\\Users\\User\\Documents\\School\\code\\NBA_Salary_Predictions')

# Scraping in Player Stats for 2018-2019 Season via Basketball Reference
stats = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2019_totals.html')[0]
adv_stats = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2019_advanced.html')[0]
adv_stats.drop(['Unnamed: 19','Unnamed: 24'], axis =1, inplace=True)

# Data Clean
adv_stats.drop(adv_stats[adv_stats['Rk'] == 'Rk'].index, inplace=True)
stats.drop(stats[stats['Rk'] == 'Rk'].index, inplace=True)

stats['Rk'] = stats['Rk'].astype(int)
stats.iloc[:,5:10] = stats.iloc[:,5:10].astype(int)
stats.iloc[:,10:30] = stats.iloc[:,10:30].astype(float)

adv_stats.iloc[:,5:7] = adv_stats.iloc[:,5:7].astype(int)
adv_stats.iloc[:,7:27] = adv_stats.iloc[:,7:27].astype(float)
adv_stats.Age = adv_stats.Age.astype(int)
adv_stats.Rk = adv_stats.Rk.astype(int)

# Scraping in Player Salaries for 2018-2019 Season via URL
list_sal = np.arange(1,14)
player_salary = []
for i in range(len(list_sal)):
    url = 'http://www.espn.com/nba/salaries/_/year/2019/page/{}'.format(list_sal[i])
    player_salary.append(pd.read_html(url)[0])
player_salary_df = pd.concat(player_salary)

# Data Clean

## Player Stats Data
## Renaming Columns
player_stats_df.rename(columns={'Player':'NAME'},inplace=True)
## Player Salary Data
## Renaming Columns
player_salary_df.columns = ['RK','NAME','TEAM','SALARY']

## Deleting rows with irrelevant information
player_salary_df.drop(player_salary_df[player_salary_df['RK']=='RK'].index, inplace=True)

## Parsing Out Player Position
player_salary_df['POSITION'] = player_salary_df['NAME'].apply(lambda x: x.split(', ')[1])
player_salary_df['NAME'] = player_salary_df['NAME'].apply(lambda x: x.split(', ')[0])

## Parsing out Salary
player_salary_df['SALARY'] = player_salary_df['SALARY'].apply(lambda x: x.replace('$',''))
player_salary_df['SALARY'] = player_salary_df['SALARY'].apply(lambda x: x.replace(',',''))
player_salary_df['SALARY'] = player_salary_df['SALARY'].astype(int)

## Team Salary and NBA Total Salary
team_salaries = player_salary_df.groupby('TEAM').sum().reset_index()
team_salaries.columns=['TEAM','TEAM SALARY']
team_salaries['TOTAL NBA SALARY'] = team_salaries['TEAM SALARY'].sum()

# DataFrame merge
df_salaries = pd.merge(player_salary_df, team_salaries, on = 'TEAM', how = 'inner')
df_salaries = df_salaries[['RK','NAME','TEAM','POSITION','SALARY','TEAM SALARY','TOTAL NBA SALARY']]
df_salaries['PLAYER WEIGHT'] = df_salaries['SALARY']/df_salaries['TEAM SALARY']
df_salaries['LEAGUE WEIGHT'] = df_salaries['SALARY']/df_salaries['TOTAL NBA SALARY']

cols_to_use = stats.columns.difference(adv_stats.columns)
cols_to_use
stats_df = pd.merge(stats[cols_to_use], adv_stats, left_index=True, right_index=True, how = 'outer')
stats_df = stats_df[['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'MP',
       'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
       'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
       'BPM', 'VORP','2P', '2P%', '2PA', '3P', '3P%', '3PA', 'AST', 'BLK', 'DRB', 'FG',
       'FG%', 'FGA', 'FT', 'FT%', 'FTA', 'GS', 'ORB', 'PF', 'PTS', 'STL',
       'TOV', 'TRB', 'eFG%']]

stats_df.columns=['Rk', 'NAME', 'Pos', 'Age', 'Tm', 'G', 'MP',
       'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
       'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
       'BPM', 'VORP','2P', '2P%', '2PA', '3P', '3P%', '3PA', 'AST', 'BLK', 'DRB', 'FG',
       'FG%', 'FGA', 'FT', 'FT%', 'FTA', 'GS', 'ORB', 'PF', 'PTS', 'STL',
       'TOV', 'TRB', 'eFG%']

final_df = pd.merge(stats_df, df_salaries, on='NAME', how='inner')
final_df.rename = final_df.rename(columns = {'Tm':'City'})
final_df.drop(['Rk','RK','Pos'],axis=1,inplace=True)
final_df = final_df[[
       'NAME','TEAM','POSITION', 'Tm','Age', 'G', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%',
       'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS',
       'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', '2P', '2P%', '2PA', '3P',
       '3P%', '3PA', 'AST', 'BLK', 'DRB', 'FG', 'FG%', 'FGA', 'FT', 'FT%',
       'FTA', 'GS', 'ORB', 'PF', 'PTS', 'STL', 'TOV', 'TRB', 'eFG%',  'SALARY', 'TEAM SALARY', 'TOTAL NBA SALARY',
       'PLAYER WEIGHT', 'LEAGUE WEIGHT']]

# CSV files
df_salaries.to_csv('nba_salaries1.csv', index = False)
stats_df.to_csv('advanced_stats.csv', index = False)
final_df.to_csv('nba_data.csv', index = False)


