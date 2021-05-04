import pyecharts.options as opts
from pyecharts.charts import WordCloud

data = [["玉三叉形器", 3],["的", 0],["分裆鼎", 0],["ddd", 0],["f d sa", 0]]

(
    WordCloud()
    .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="文物热度词云图", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        legend_opts=opts.LegendOpts(pos_left="left"),
    )
    .render("basic_wordcloud.html")
)