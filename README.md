# flask-omnipro-plot

Synopsis
--------
A simple Flask website to read in two .opg beam data files from the [OmniPro Matrixx](http://www.iba-dosimetry.com/complete-solutions/radiotherapy/imrt-igrt-rotational-qa/matrixxes) and plot them against each other, including a helpful point-to-point percentage difference plot.


Install
--------
```
pip install -r requirements
```

Run
--------
```
python main.py
```
which will run the server on `http:\\localhost:5001`.

Usage
--------
Choose one or two .opg files and click Submit. Hover over points on the graphs for point measurements. The percentage difference between the plots is shown in yellow.

Built with
------------
[Flask](http://flask.pocoo.org/)

[Jinja2](http://jinja.pocoo.org/docs/2.9/)

[Google Charts](https://developers.google.com/chart/)

