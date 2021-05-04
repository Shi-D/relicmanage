import pyecharts.options as opts
from pyecharts.charts import Line, Grid
from datetime import datetime, timedelta, timezone
import csv
import pandas as pd

# 日期列表
date = datetime(2021, 4, 23)
print(date)
date_list = []

for i in range(335):
    dd = str(date)
    dd = dd[:10]
    date_list.append(dd)
    date -= timedelta(days=1)

date_list.reverse()
print('date_list', date_list)


# 人流量列表
def data_load(data_path):
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = pd.DataFrame(reader)
        return data
    return None

data_path = 'museum.csv'
data = data_load(data_path)
y_train = data[[2]]
y_train = y_train.values
y_train = y_train[1:]
y = []
for i in y_train:
    y.append(int(i[0]))
print('y', y)

predict = []
with open('predict.txt', 'r') as f:
    for i in range(5):
        predict.append(int(f.readline()))
print('predict', predict)

y.extend(predict)

l1 = (
    Line()
    .add_xaxis(xaxis_data=date_list)
    .add_yaxis(
        series_name="人流量",
        y_axis=y,
        symbol_size=8,
        is_hover_animation=False,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=1.5),
        is_smooth=False,
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="浙江省博物馆人流量", subtitle="数据来自shiyd", pos_left="center"
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=False,
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
        ],

        yaxis_opts=opts.AxisOpts(max_=8000, name="人流量(人/天)"),
        legend_opts=opts.LegendOpts(pos_left="left"),
    )
    .render("museum_visitors_flowrate.html")

)

