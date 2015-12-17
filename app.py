import numpy as np
import time
import Quandl
import requests
import pandas
from bokeh.charts import Line
from bokeh.embed import file_html, components
from bokeh.plotting import figure,show,output_file
from bokeh.resources import CDN
from flask import Flask, render_template, request, redirect, send_from_directory
from StringIO import StringIO
from werkzeug import secure_filename

Quandl.api_key = "sJN4VTedn6CE_mZ-6LrM"
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.vars = {}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
  if request.method == 'GET': 
    return render_template('index.html')
  else: # request.method == 'POST'
    app.vars['stock'] = request.form['ticker']
    app.vars['choice'] = request.form['features']
    #r = Quandl.get("WIKI/"+app.vars['stock'], returns=pandas)
    j = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + app.vars['stock'] +'.csv?api_key=sJN4VTedn6CE_mZ-6LrM')
    jprime = j.content
    r = pandas.read_csv(StringIO(jprime))
    now = time.time()
    num_points = r.shape[0]
    dt = 24*3600 # days in seconds
    dates = np.linspace(now, now + num_points*dt, num_points) * 1000 # times in ms
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    #output_file("plot.html", title = app.vars['stock']+" prices")
    f = figure(x_axis_label='date', x_axis_type="datetime",tools=TOOLS)
    f.line(dates, r[app.vars['choice']], color='#1F78B4', legend=app.vars['stock'])
    script, div = components(f)
    return render_template('result.html', script=script, div = div, stock = app.vars['stock'])


@app.route('/result', methods=['GET'])
def result():
  return render_template('result.html')

if __name__ == '__main__':
  app.run(port=5000, debug=True)