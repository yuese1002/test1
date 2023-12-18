from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Line
from pyecharts.globals import ThemeType

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        generate_word_frequency(url)
        return render_template('index.html', show_chart=True)
    else:
        return render_template('index.html', show_chart=False)

def generate_word_frequency(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    filter_words = ['\n', ' ', '，', '。', '！', '？', '的', '是', '在', '了', '和', '同', '为', '也', '这', '有',
                    '就', '又', '或', '但', '如果', '由于', '因此', '所以', '之', '与',
                    '及', '或者', '一些', '一样', '例如', '这些', '那些', '不', '也不',
                    '之一', '之二', '之三', '之四', '之五', '之六', '之七', '之八', '之九', '之十',
                    '……', '。', '，', '、', '：', '；', '！', '？', '“', '”',
                    '（', '）', '【', '】', '《', '》', '［', '］', '｛', '｝'
                    ,'我', '他', '她', '你']
    for word in filter_words:
        text = text.replace(word, '')

    words = jieba.cut(text)

    word_count = Counter(words)

    top_10_words = dict(word_count.most_common(10))

    x = list(top_10_words.keys())
    y = list(top_10_words.values())

    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("", [list(z) for z in zip(x, y)])
        .set_global_opts(title_opts=opts.TitleOpts(title="饼状图"),
                         legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render("static/bing.html")
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x)
        .add_yaxis("word Count", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="柱状图 "),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                         legend_opts=opts.LegendOpts(is_show=False))
    )
    bar.render("static/zhu.html")

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x)
        .add_yaxis("word Count", y)
        .set_global_opts(title_opts=opts.TitleOpts(title=" 折线图"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                         legend_opts=opts.LegendOpts(is_show=False))
    )
    line.render("static/zhexian.html")

if __name__ == "__main__":
    app.run(debug=True)