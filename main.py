from flask import Flask, make_response, request, render_template, jsonify
import json
import io
import csv

#
# import numpy as np
# from scipy.interpolate import UnivariateSpline

app = Flask(__name__)

class OpgData(object):
    """
    Class to hold data from .opg file
    """

    def __init__(self, opg_reader):
        self.opg_reader = opg_reader
        self.x_cm, self.y_cm, self.pixel_data = self.parse_data()

    def parse_data(self):
        """
        Read in data from .opg file
        """
        # with open(self.opg_reader, "r") as ins:
        raw_data = []
        for row in self.opg_reader:
            raw_data.append(row)

        all_data = []
        while True:
            for line in raw_data:
                if r'<asciibody>' in line:
                    break
            for line in raw_data:
                if '</asciibody>' in line:
                    break
                all_data.append(line)

        x_cm = [float(x) for x in all_data[2].split('\t')[1:-1]]
        y_cm = [float(x.split('\t')[0]) for x in all_data[4:-1]]
        pixel_data = [[float(x) for x in y.split('\t')[1:-1]] for y in all_data[4:]]
        return x_cm, y_cm, pixel_data

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
    reader = csv.reader(stream, delimiter=',')
    return OpgData(reader)


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
    if not f2:
        return "No file 2"

    # opg1 = read_opg_file(f1)
    x_1, y_1 = read_file(f1)
    x_2, y_2 = read_file(f2)

    chart_input = []
    for i in range(len(x_1)):
        chart_input.append([x_1[i],y_1[i],"null"])

    for i in range(len(x_2)):
        chart_input.append([x_2[i],"null",y_2[i]])

    print(chart_input)
    return render_template('chart.html', chart_input = chart_input)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
