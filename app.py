
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


# https://gitpython.readthedocs.io/en/stable/intro.html
import git

# https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664
@app.route('/update', methods=['GET', 'POST'])
def update():
    # git repo
    repo = git.Repo()
    remote = repo.remotes.gh
    pull = None
    # get notification
    if flask.request.method == 'POST':
        # mark update notification
        key = '%s' % dt.datetime.now()
        val = flask.request.data
        updates['last'] = key
        updates[key] = val
    # git pull
    if not repo.is_dirty():
        try: # master pull
            pull = remote.pull()
        except: # debug fallback
            remote = repo.remotes.bb
            pull = remote.pull()
        # service restart
        WSGI = '/var/www/kbase_pythonanywhere_com_wsgi.py'
        try:
            open(WSGI, 'a').close() # touch reload
        except:
            pass
    else:
        pull = [{'ref': remote, 'flags': 'is', 'note': 'dirty'}]
    # send report
    return flask.render_template('update.html', updates=updates, repo=repo, remote=remote, pull=pull[0])
    # return flask.redirect('/')


if __name__ == '__main__': # local debug mode
    app.run(host='localhost', port=12345, debug=True)
