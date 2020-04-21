
import datetime as dt

updates = {}

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html', updates=updates)

@app.route('/<path:path>.css')
def css(path):
    return app.send_static_file('%s.css' % path)

@app.route('/<path:path>.js')
def js(path):
    return app.send_static_file('%s.js' % path)

@app.route('/logo.png')
def logo():
    return app.send_static_file('logo.png')

# https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664
@app.route('/update', methods=['GET', 'POST'])
def update():
    key = '%s' % dt.datetime.now()
    val = flask.request.data
    updates['last'] = key
    updates[key] = val
    return flask.redirect('/')


if __name__ == '__main__': # local debug mode
    app.run(host='localhost', port=12345, debug=True)
