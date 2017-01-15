from flask import Flask, make_response, request, render_template, jsonify
import json
import io
import csv
# from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('index.html')

def read_file(file_in):
    stream = io.StringIO(file_in.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream, delimiter=',')
    x = []
    y = []
    next(reader, None)
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[1]))
    # x = [i[0] for i in csv_list[1:]]
    # y = [i[1] for i in csv_list[1:]]
    # print(y)
    return x, y

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route('/embed', methods=["POST"])
def transform_view():
    f1 = request.files['datafile_one']
    f2 = request.files['datafile_two']

    if not f1:
        return "No file 1"
    if not f2:
        return "No file 2"

    x_1, y_1 = read_file(f1)
    x_2, y_2 = read_file(f2)

    fig = figure(title="Plot")
    fig.line(x_1, y_1,line_width=2)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(fig)
    html = render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources
    )
    return encode_utf8(html)
    # return render_template('data.html', script=script, div=div)

    # return render_template('output.html',
    # x_1=x_1,
    # data_set_2=data_set_2)

    # stream.seek(0)
    # result = transform(stream.read())
    #
    # response = make_response(result)
    # response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    # return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
