from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, session
from flask import render_template, redirect, request
from flask.ext.login import LoginManager, login_required
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.assets import Environment, Bundle
import settings

from utils.readability import make_readable

app = Flask(__name__)
assets = Environment(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.debug = settings.DEBUG
app.secret_key = settings.SECRET

js = Bundle(
    'js/jquery-1.8.3.min.js',
    'assets/jquery-ui/jquery-ui-1.10.1.custom.min.js',
    'js/respond.min.js', 'js/bootstrap.min.js',
    'js/hover-dropdown.js', 'js/jquery.customSelect.min.js',
    'js/jquery.ui.touch-punch.min.js', 'js/sliders.js',
    'js/common-scripts.js', filters='jsmin', output='gen/packed.js'
)

css = Bundle(
    'css/bootstrap.min.css', 'css/bootstrap-reset.css', 'css/style.css',
    'css/style-responsive.css', 'css/custom.css',
    filters='cssmin', output='gen/packed.css'
)

assets.register('js_all', js)
assets.register('css_all', css)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/parsed', methods=["POST"])
def parse():
    url = request.form.get("url")
    json_data = make_readable(url)
    return render_template('parsed.html', data=json_data)


@app.route('/submit', methods=["GET"])
def submit():
    url = request.args.get("url")
    json_data = make_readable(url)
    return render_template('parsed.html', data=json_data)


if __name__ == '__main__':
    app.debug = settings.DEBUG
    app.secret_key = settings.SECRET
    app.run(host="0.0.0.0", port=settings.PORT)
