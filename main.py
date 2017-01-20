from flask import Flask, make_response, request, render_template, jsonify
import json
import io
import csv
from bs4 import BeautifulSoup
import pprint
#
# import numpy as np
# from scipy.interpolate import UnivariateSpline

app = Flask(__name__)

pp = pprint.PrettyPrinter(indent=4)

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
    return x, y


def read_opg_file(opg_file_in):
    stream = io.StringIO(opg_file_in.stream.read().decode("UTF8"), newline=None)
    soup = BeautifulSoup(stream)
    raw_data = soup.find('asciibody').getText()
    raw_data = raw_data.split('\n')
    x_cm = [float(x) for x in raw_data[3].split('\t')[1:-1]]
    y_cm = [float(x.split('\t')[0]) for x in raw_data[5:-1]]
    pixel_data = [[float(x) for x in y.split('\t')[1:-1]] for y in raw_data[5:]]
    # pp.pprint(x_cm)


    # reader = csv.reader(stream, delimiter=',')
    # class_to_return = OpgData(reader)
    # console.log(class_to_return.x_cm)
    return x_cm, y_cm, pixel_data


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route('/chart', methods=["POST"])
def transform_view():
    f1 = request.files['datafile_one']
    f2 = request.files['datafile_two']

    if not f1:
        return "No file 1"
    # if not f2:
    #     return "No file 2"

    x_vals_1, y_vals_1, pixel_data_1 = read_opg_file(f1)


    # stream = io.StringIO(f1.stream.read().decode("UTF8"), newline=None)
    # reader = csv.reader(stream)
    # raw_data = []
    # for row in reader:
    #     raw_data.append(row)
    # all_data = []
    # while True:
    #     for line in raw_data:
    #         if r'<asciibody>' in line:
    #             break
    #     for line in raw_data:
    #         if '</asciibody>' in line:
    #             break
    #         all_data.append(line)
    # x_cm = [float(x) for x in all_data[2].split('\t')[1:-1]]
    # y_cm = [float(x.split('\t')[0]) for x in all_data[4:-1]]
    # pixel_data = [[float(x) for x in y.split('\t')[1:-1]] for y in all_data[4:]]
    # for x in x_cm:
    #     print(x)
    # x_1, y_1 = read_file(f1)
    # x_2, y_2 = read_file(f2)

    x_1 = x_vals_1
    y_1 = pixel_data_1[round(len(pixel_data_1) / 2)]

    chart_input = []
    for i in range(len(x_1)):
        chart_input.append([x_1[i],y_1[i],"null"])

    pp.pprint(chart_input)
    # for i in range(len(x_2)):
    #     chart_input.append([x_2[i],"null",y_2[i]])

    return render_template('chart.html', chart_input = chart_input)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
