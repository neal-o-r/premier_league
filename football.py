import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, TapTool, Line, Div
from collections import defaultdict
import numpy as np


df = pd.read_csv('pl_games.csv', parse_dates=[2])

df.sort_values(['Date'], inplace=True)


team_wins = defaultdict(list)
for row in df.iterrows():
        row = row[1]
        
        if row.FTHG > row.FTAG:

                team_wins[row.HomeTeam].append(1)
       
        if row.FTAG >= row.FTAG:
       
                team_wins[row.AwayTeam].append(0)
                   



#output_file("premier_league.html", title="Premier League Matches")
p = figure(plot_width=1000, plot_height=600, tools=[TapTool()], title="")
 


for team in team_wins:

        source = ColumnDataSource({'x': range(len(team_wins[team])),
                                'y': np.cumsum(team_wins[team])})

        render = p.line(x='x', y='y', source=source, 
                nonselection_line_color='blue', 
                nonselection_line_alpha=0.5,
                selection_color='firebrick',
                selection_line_alpha=1.,
                line_width=2.
        )

show(p)
