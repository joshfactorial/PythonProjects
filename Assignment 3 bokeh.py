import pandas as pd
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.plotting import figure, show, output_file

output_file("C:/Users/Joshua/Desktop/figure.html")

data = pd.read_csv('C:/Users/Joshua/Downloads/data_tohoku_norm_transpose.csv', header=None)

y = data[5]

for k in range(3500, len(y)):
    del y[k]

for j in range(2000):
    del y[j]

x = []
for i in range(len(y)):
    x.append(i)

color = ["navy"] * len(x)

ind = 0
for p in y:
    ind += (ind + p) /len(y)

print([ind, ind])

s = ColumnDataSource(data=dict(x=x, y=y, color=color))
p = figure(plot_width=400, plot_height=400, tools='lasso_select,save',
           title="Bokeh example", x_axis_label='x-axis', y_axis_label='y-axis')
p.circle('x', 'y', color='color', source=s, alpha=0.4)

s2 = ColumnDataSource(data=dict(x=[0, 1500], ym=[ind, ind]))
p.line(x='x', y='ym', color="orange", line_width=5, alpha=0.6, source=s2)


# https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html
s.callback = CustomJS(args=dict(s2=s2), code="""
        var inds = cb_obj.selected.indices;
        var d = cb_obj.data;
        var ym = 0

        if (inds.length == 0) { return; }

        for (i = 0; i < d['color'].length; i++) {
            d['color'][i] = "navy"
        }
        for (i = 0; i < inds.length; i++) {
            d['color'][inds[i]] = "firebrick"
            ym += d['y'][inds[i]]
        }

        ym /= inds.length
        s2.data['ym'] = [ym, ym]

        cb_obj.change.emit();
        s2.change.emit();
    """)

show(p)
