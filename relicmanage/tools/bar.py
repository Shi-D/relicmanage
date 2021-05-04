from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode

type = ['金石陶瓷', '漆木竹骨', '书画碑帖', '丝绸织绣']
num = [4, 2, 2, 3]

c = (
    Bar()
    .add_xaxis(type)
    .add_yaxis("文物数量", num, category_gap="60%")
    .set_series_opts(
        itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(0, 244, 255, 1)'
            }, {
                offset: 1,
                color: 'rgba(0, 77, 167, 1)'
            }], false)"""
                ),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": "rgb(0, 160, 221)",
            }
        }
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="文物类别数量", pos_left='center'),
        legend_opts=opts.LegendOpts(pos_left="right"),
    )
    .render("bar_relic_type.html")
)
