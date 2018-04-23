import jinja2
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mpld3
from mpld3 import plugins, utils


class HighlightLines(plugins.PluginBase):
    """A plugin to highlight lines on hover"""

    JAVASCRIPT = """
    mpld3.register_plugin("linehighlight", LineHighlightPlugin);
    LineHighlightPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LineHighlightPlugin.prototype.constructor = LineHighlightPlugin;
    LineHighlightPlugin.prototype.requiredProps = ["line_ids"];
    LineHighlightPlugin.prototype.defaultProps = {alpha_bg:0.3, alpha_fg:1.0}
    function LineHighlightPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LineHighlightPlugin.prototype.draw = function(){
      for(var i=0; i<this.props.line_ids.length; i++){
         var obj = mpld3.get_element(this.props.line_ids[i], this.fig),
             alpha_fg = this.props.alpha_fg;
             alpha_bg = this.props.alpha_bg;
         obj.elements()
             .on("mouseover.highlight", function(d, i){
                            d3.select(this).transition().duration(50)
                              .style("stroke-opacity", alpha_fg); })
             .on("mouseout.highlight", function(d, i){
                            d3.select(this).transition().duration(200)
                              .style("stroke-opacity", alpha_bg); });
      }
    };
    """

    def __init__(self, lines):
        self.lines = lines
        self.dict_ = {"type": "linehighlight",
                      "line_ids": [utils.get_id(line) for line in lines],
                      "alpha_bg": lines[0].get_alpha(),
                      "alpha_fg": 1.0}

import pandas as pd
import numpy as np

df = pd.read_csv('teams.csv', dtype={'Team':str, 'Record':str}, delimiter=':')

df['Record'] = [list(map(int, df.Record[i].split(',')))
                for i in range(len(df))]
df['Cumulative'] = df.Record.apply(np.cumsum)

N = df.Cumulative.apply(len).max()

x = np.arange(N)
y = np.empty((len(df), N))
y[:] = np.nan

names = []
for i, row in df.iterrows():
        c = list(row.Cumulative)
        c = c + [np.nan]*(N - len(c))
        y[i, :] = c
        names.append(row.Team)

fig, ax = plt.subplots(figsize=(8, 6),
                        subplot_kw={'xticks': [], 'yticks': []})
colormap = plt.cm.Vega10
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 50)])

lines = ax.plot(x, y.T, '-', lw=1, alpha=0.2)

plugins.connect(fig, HighlightLines(lines))
for i, l in enumerate(lines):
    plugins.connect(fig, plugins.LineLabelTooltip(l, names[i]))
mpld3.save_html(fig, 'premier.html')
