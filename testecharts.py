from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QFileSystemModel, QTreeView, QPushButton, \
    QLabel, QDialog
from PySide6.QtCore import QFile, QObject, Qt, QDir, QUrl, QSize
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore

from PySide6.QtWebEngineWidgets import QWebEngineView
from pyecharts.charts import Bar, Page
from pyecharts import options as opts

x = ['a1', 'b1', 'c1']
y1 = [1240, 524, 270]
y2 = [1300, 300, 530]

bar = Bar(init_opts=opts.InitOpts(
            # bg_color='#080b30',  # 设置背景颜色
            # theme='dark'  ,       # 设置主题
            width='380px',     # 设置图的宽度
            height='300px'     # 设置图的高度
        ))
# 设置x轴
bar.add_xaxis(xaxis_data=x)
# 设置y轴
bar.add_yaxis(series_name='A', y_axis=y1)
# bar.add_yaxis(series_name='B', y_axis=y2)
bar.set_global_opts(title_opts=opts.TitleOpts(title='示例'))


class Stats:

    def __init__(self):
        qfile_daqi = QFile('ui/test.ui')  # 加载自己的ui文件
        qfile_daqi.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(qfile_daqi)
        qfile_daqi.close()
        bro = QWebEngineView()
        # bar.set_global_opts(
        #     title_opts=opts.TitleOpts(title='示例'),
        #     init_opts=opts.InitOpts(width='600px', height='400px')
        # )
        bro.setHtml(bar.render_embed())
        self.ui.scrollArea.setWidget(bro)


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec()

# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QFileSystemModel, QTreeView, QPushButton, QLabel, QDialog
# from PySide6.QtCore import QFile, QObject, Qt, QDir, QUrl, QSize
# from PySide6.QtUiTools import QUiLoader
# from PySide6.QtWebEngineWidgets import QWebEngineView
# from pyecharts.charts import Bar, Page
# from pyecharts import options as opts
#
# x = ['a1', 'b1', 'c1']
# y1 = [1240, 524, 270]
# y2 = [1300, 300, 530]
#
# bar = Bar()
# # 设置x轴
# bar.add_xaxis(xaxis_data=x)
# # 设置y轴
# bar.add_yaxis(series_name='A', y_axis=y1)
# bar.add_yaxis(series_name='B', y_axis=y2)
# bar.set_global_opts(title_opts=opts.TitleOpts(title='示例'))
#                     # ,init_opts=opts.InitOpts(width='600px', height='400px'))
#
# class Stats:
#     def __init__(self):
#         qfile_daqi = QFile('ui/test.ui')  # 加载自己的ui文件
#         qfile_daqi.open(QFile.ReadOnly)
#         self.ui = QUiLoader().load(qfile_daqi)
#         qfile_daqi.close()
#
#         # 创建 QWebEngineView 控件
#         self.webEngineView = QWebEngineView()
#         self.ui.scrollArea.setWidget(self.webEngineView)
#
#         # 将图表渲染为 HTML 文件
#         page = Page()
#         page.add(bar)
#         page.render('bar.html')
#
#         # 在 QWebEngineView 中显示图表
#         self.webEngineView.load(QUrl.fromLocalFile('bar.html'))
#
# if __name__ == '__main__':
#     app = QApplication([])
#     stats = Stats()
#     stats.ui.show()
#     app.exec()