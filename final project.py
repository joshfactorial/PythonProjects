#from bokeh.plotting import *
#from bokeh.models import HoverTool
from bokeh.embed import components
#import pandas as pd
#from ipywidgets import interact
#import bokeh
from bokeh.io import show, output_file, output_notebook
from bokeh.plotting import figure
from bokeh.palettes import Viridis
from bokeh.models import ColumnDataSource, HoverTool,NumeralTickFormatter
import pandas as pd
import ipywidgets
from ipywidgets import interact
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import gaussian_kde

salary = pd.read_csv("data/Salaries.csv")
fielding = pd.read_csv("data/Fielding.csv")

player_position = pd.merge(salary, fielding, on = ["playerID","yearID"])[["yearID", "playerID", "salary", "POS"]]

data = player_position.groupby(["yearID", "POS"]).mean()["salary"].unstack()
output_notebook()
hover = HoverTool(tooltips=[
   ("Position","@pos"),
   ("Salary","@salary{($ 0,0)}")
])


def fi(year=2015):
    x = player_position[player_position["yearID"] == year]
    data = x.groupby("POS").max()["salary"].reset_index()
    pos = []
    for i in data["POS"]:
        pos.append(i)
    sal = []
    for i in data["salary"]:
        sal.append(i)
    source = ColumnDataSource(data=dict(pos=pos, salary=sal, color=Viridis[7]))
    p = figure(x_range=pos, title="Salaries in different positions", tools=[hover], y_range=(0, 35000000),
               plot_height=300)
    p.vbar(x="pos", top="salary", width=0.9, color="color", source=source, legend="pos")
    p.legend.orientation = "horizontal"
    p.xaxis.axis_label = "Position"
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")
    p.yaxis.axis_label = "Salary"
    script, div = components(p)
    script = '\n'.join([line for line in script.split('\n')])

    print('''{script}

    #+BEGIN_HTML
    <a name="figure"></a>
    {div}
    #+END_HTML
    '''.format(script=script, div=div))
interact(fi, year=(1985,2015));