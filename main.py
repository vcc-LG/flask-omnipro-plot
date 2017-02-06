"""
    flask-omnipro-plot
    ~~~~~~
    A simple website to plot out and compare beam profiles
     from the OmniPro Matrixx using Flask.
"""

from flask import Flask,request, render_template
import io
from bs4 import BeautifulSoup
import numpy as np
from scipy.interpolate import UnivariateSpline

# create application
app = Flask(__name__)

@app.route('/')
def index():
    """Render index."""
    return render_template('index.html')


def find_middle(input_list):
    """Return closest centre value of array"""
    middle = float(len(input_list)) / 2
    if middle % 2 != 0:
        return input_list[int(middle - .5)]
    else:
        return (input_list[int(middle)] + input_list[int(middle - 1)]) / 2


def normalise_data(input_data):
    """Normalise to central axis"""
    return [100 * (float(i) / find_middle(input_data)) for i in input_data]


def read_opg_file(opg_file_in):
    """Parse data from opg file"""
    stream = io.StringIO(
        opg_file_in.stream.read().decode("UTF8"), newline=None)
    soup = BeautifulSoup(stream)
    raw_data = soup.find('asciibody').getText()
    raw_data = raw_data.split('\n')
    x_cm = [float(x) for x in raw_data[3].split('\t')[1:-1]]
    y_cm = [float(x.split('\t')[0]) for x in raw_data[5:-1]]
    pixel_data = [[float(x) for x in y.split('\t')[1:-1]]
                  for y in raw_data[5:]]

    return x_cm, y_cm, pixel_data


@app.route('/chart', methods=["POST"])
def transform_view():
    """Convert opg data into a usable format and pass to template"""
    f1 = request.files['datafile_one']
    f2 = request.files['datafile_two']
    chart_input = []
    file_names = []
    if f1:
        try:
            file_names.append(f1.filename)
            x_vals_1, y_vals_1, pixel_data_1 = read_opg_file(f1)
            x_1 = x_vals_1
            y_1 = normalise_data(pixel_data_1[round(len(pixel_data_1[0]) / 2)])
            for i in range(len(x_1)):
                chart_input.append([x_1[i], y_1[i]])
        except AttributeError:
            return render_template('error.html')
    if f2:
        try:
            [i.append("null") for i in chart_input]
            file_names.append(f2.filename)
            x_vals_2, y_vals_2, pixel_data_2 = read_opg_file(f2)
            x_2 = x_vals_2
            # y_2 = pixel_data_2[round(len(pixel_data_2) / 2)]
            y_2 = normalise_data(pixel_data_2[round(len(pixel_data_2[0]) / 2)])
            for i in range(len(x_2)):
                chart_input.append([x_2[i], "null", y_2[i]])
        except AttributeError:
            return render_template('error.html')

    if not f1 and not f2: #if user hasn't selected any files
        return render_template('error.html')

    if f1 and f2:
        measurement_horz = x_2
        measurement_norm = y_2
        baseline_norm = y_1
        baseline_horz = x_1
        spline_interpolation = UnivariateSpline(measurement_horz,
                                                np.array(measurement_norm) - 20)  # Interpolate to 20 % field width
        roots_out = spline_interpolation.roots()
        r1, r2 = roots_out[::len(roots_out) - 1]
        percentage_diff = [100 * ((x / y) - 1) for x, y in zip(baseline_norm, measurement_norm)]
        [i.append("null") for i in chart_input]
        for i in range(len(x_1)):
            chart_input.append([x_1[i], "null", "null", percentage_diff[i]])
        file_names.append('Percentage difference')

    return render_template('chart.html',
                           file_names=file_names,
                           chart_input=chart_input)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
