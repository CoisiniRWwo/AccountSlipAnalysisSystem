from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMessageBox
from pyecharts.charts import Bar, Page
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from lib.connectMySQL import everyDayCountPrice


def barPrice(day, priceSum, title):
    x = day
    y1 = priceSum
    # y2 = [1300, 300, 530]

    bar = Bar(init_opts=opts.InitOpts(
        # bg_color='#080b30',  # 设置背景颜色
        # theme='dark'  ,       # 设置主题
        width='670px',  # 设置图的宽度
        height='400px'  # 设置图的高度
    ))
    # 设置x轴
    bar.add_xaxis(x)
    # 设置y轴
    bar.add_yaxis(series_name='金额', y_axis=y1, category_gap="50%")
    # bar.add_yaxis(series_name='B', y_axis=Faker.values(),category_gap="50%")

    bar.set_series_opts(  # 自定义图表样式
        label_opts=opts.LabelOpts(is_show=False),  # 是否显示数据标签
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="最小值"),  # 显示最小值标签
                opts.MarkLineItem(type_="max", name="最大值"),  # 显示最大值标签
                # opts.MarkLineItem(type_="average", name="平均值") # 显示均值标签
            ]
        ),
        itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [ 
                    {offset: 0,color: '#D13ABD'}
                    ,{offset: 1, color: '#EEBD89'}
                    ], false)
                    """
                ),  # 调整柱子颜色渐变
                "barBorderRadius": [70, 70, 0, 0],  # 调整柱子圆角弧度
                "shadowColor": "rgb(0, 160, 221)",  # 调整阴影颜色
            }
        }
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_left='center'),
        legend_opts=opts.LegendOpts(
            pos_left='right',  # 图例显示位置
            # orient='horizontal'  # 图例水平布局
        )
    )

    return bar


def barType(self):
    title = '4月消费金额分析'
    year = str(self.ui.yearlineEdit.text().strip())
    month = str(self.ui.monthlineEdit.text().strip())
    day = list(range(1, 32))
    priceSum = []
    if year == '':
        year = 2023
        title = '2023年消费金额分析'
        day = list(range(1, 13))
        for i in range(1, 13):
            priceSum.append(0.0)
    elif year != '' and month == '':
        day = list(range(1, 13))
        title = year + '年消费金额分析'
        for i in range(1, 13):
            priceSum.append(0.0)
    elif year != '' and month != '':
        day = list(range(1, 32))
        title = year + '年' + month + '月消费金额分析'
        for i in range(1, 32):
            priceSum.append(0.0)

    result = everyDayCountPrice(year, month)
    print('账单信息', result)

    for row in result:
        priceSum[row[0] - 1] = row[1]
    priceSum = [float(x) for x in priceSum]

    bro = QWebEngineView()
    bro.setHtml(barPrice(day, priceSum, title).render_embed())

    self.ui.scrollAreaPrice.setWidget(bro)
