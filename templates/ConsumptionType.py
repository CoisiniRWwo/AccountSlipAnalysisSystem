from pyecharts.charts import Pie
from pyecharts import options as opts
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMessageBox
from pyecharts.charts import Bar, Page
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from lib.connectMySQL import everyDayCountPrice, everyDayCountType


def piePrice(title, data):
    # data = list(zip(day, priceSum))
    # data = [831.87, 374.12, 1276.37, 80.75, 831.87]
    labels = ['交通', '娱乐', '日用', '购物', '餐饮']
    data = [(i, j) for i, j in zip(labels, data)]
    pie = Pie(init_opts=opts.InitOpts(
        width='640px',  # 设置图的宽度
        height='400px'  # 设置图的高度
    ))
    pie.add("", data)
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_left='center'),
        legend_opts=opts.LegendOpts(
            pos_left='right',  # 图例显示位置
            orient='vertical'  # 图例竖向显示
        )
    )
    return pie


def showPieChart(self):
    title = '4月消费金额分析'
    year = str(self.ui.yearlineEdit_2.text().strip())
    month = str(self.ui.monthlineEdit_2.text().strip())
    if year == '':
        year = 2023
        title = '2023年消费类型分析'
    elif year != '' and month == '':
        title = year + '年消费类型分析'
    elif year != '' and month != '':
        title = year + '年' + month + '月消费类型分析'

    data = []
    result = everyDayCountType(year, month)
    print('类型信息：', result)
    for row in result:
        data.append(row[1])
    data = [float(x) for x in data]

    pie = piePrice(title, data)
    bro = QWebEngineView()
    bro.setHtml(pie.render_embed())
    self.ui.scrollAreaType.setWidget(bro)
