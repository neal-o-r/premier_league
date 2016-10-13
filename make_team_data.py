import pandas as pd
from collections import defaultdict
import numpy as np

df = pd.read_csv('pl_games.csv', parse_dates=[2])

df.sort_values(['Date'], inplace=True)

team_wins = defaultdict(list)
for row in df.iterrows():
        row = row[1]
        
        if row.FTHG > row.FTAG:

                team_wins[row.HomeTeam].append(1)
       		team_wins[row.AwayTeam].append(-1)

        if row.FTAG > row.FTHG:
       
                team_wins[row.AwayTeam].append(-1)
		team_wins[row.HomeTeam].append(1)

	if row.FTHG == row.FTAG:

		team_wins[row.AwayTeam].append(0)
		team_wins[row.HomeTeam].append(0)

with open('teams.csv', 'w') as f:                   
	for team in team_wins:
		f.write('"'+team+'"'+':' +'"'+str(team_wins[team]) + '"\n')	

