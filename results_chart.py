import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import layout, widgetbox


df = pd.read_csv('teams.csv', dtype={'Team':str, 'Record':str}, delimiter=':')

df['Record'] = [map(int, df.Record[i].split(',')) for i in range(len(df))]

df['Width']  = 2
df['Colour'] = "blue"
df['Alpha']  = [0.8] * len(df)
df['PC'] = 100 * (df.Record.apply(sum) / df.Record.apply(len)) 


desc = Div(text=open("description.html", 'r').read(), width=800)

search = TextInput(title="Search for a team")

source = ColumnDataSource(data=dict(x=[], y=[], team=[], pc=[], colour=[], width=[], alpha=[]))

p = figure(plot_height=800, plot_width=1000, title="")

p.multi_line(
        xs = 'x',
        ys = 'y',
        line_width = 'width',
        color = 'colour',
        alpha = 'alpha', source=source
)
p.yaxis.axis_label = "Cumulative Matches Won"
p.xaxis.axis_label = "Number of Games Played"


def select_frame():

        sel = df.copy(deep=True)
        if (search.value != ""):
                mask = sel['Team'].str.lower().str.contains(
                        search.value.lower())

                sel.loc[mask, 'Colour']  = 'red'
                sel.loc[mask, 'Alpha']   = 0.8
                sel.loc[mask, 'Width']   = 4
                sel.loc[~mask, 'Colour'] = 'grey'
                sel.loc[~mask, 'Alpha']  = 0.2
                sel.loc[~mask, 'Width']  = 1
        return sel


def update():
        
        df_plot = select_frame()

        selected_team = (df_plot.Team[df_plot.Colour == 'red'].values)
        
        if len(selected_team) != 0:

                p.title.text = "%s have won %.2f%% of their Premier League Matches" %(selected_team[0], df_plot.PC[df_plot.Team == selected_team[0]])


        source.data = dict(
                x = list(df_plot.Record.apply(len).apply(range)),
                y = list(df_plot['Record'].apply(np.cumsum)),
                team = df_plot['Team'],
                pc = df_plot['PC'],
                colour = list(df_plot['Colour']),
                width = list(df_plot['Width']),
                alpha = list(df_plot['Alpha'])
        )


controls = [search]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Premier League Match Results"


