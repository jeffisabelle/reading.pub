# -*- coding: utf-8 -*-
import settings
import json

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, session
from flask import render_template, redirect, request
from flask.ext.login import LoginManager, login_required
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.assets import Environment, Bundle
from datetime import datetime

from utils import userutils
from utils.readability import make_readable
from utils.pyscrape.soup import LinkScrapper
from models.models import User, Post


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
    'js/common-scripts.js', 'js/jquery.timeago.js',
    filters='jsmin', output='gen/packed.js'
)

css = Bundle(
    'css/bootstrap.min.css', 'css/bootstrap-reset.css', 'css/style.css',
    'css/style-responsive.css', 'css/custom.css',
    filters='cssmin', output='gen/packed.css'
)

assets.register('js_all', js)
assets.register('css_all', css)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return User.objects(username=username).first()


def get_user():
    if current_user.is_authenticated():
        user = User.objects(username=current_user.username).first()
        return user
    else:
        return None


@app.route('/')
def index():
    user = get_user()
    recent = Post.objects(author=user).order_by("-saved_date")
    return render_template("index.html", user=user, recent=recent)


@app.route('/parsed', methods=["POST"])
def parse():
    url = request.form.get("url")
    json_data = make_readable(url)
    user = get_user()
    return render_template('parsed.html', data=json_data, user=user)


@app.route('/submit', methods=["GET"])
def submit():
    url = request.args.get("url")
    json_data = make_readable(url)
    user = get_user()
    return render_template('parsed.html', data=json_data, user=user)


@app.route("/login", methods=["GET", "POST"])
def login_function():
    post_data = json.loads(request.data)
    username = post_data["username"]
    password = post_data["password"]
    remember_me = post_data["remember_me"]

    user = User.objects(username=username).first()
    if not user:
        return json.dumps(
            {
                "status": "error",
                "result": "we couldn't find that user, sorry!'"
            }
        )

    pwd_hash = user["password"]
    if userutils.check_password(password, pwd_hash):
        if remember_me:
            login_user(user, remember=True)
        else:
            login_user(user)

        return json.dumps(
            {
                "status": "success",
                "result": "user logged in"
            }
        )
    else:
        return json.dumps(
            {
                "status": "error",
                "result": "password seems to be incorrect, sorry!"
            }
        )


@app.route("/register", methods=["POST"])
def register_function():
    post_data = json.loads(request.data)
    username = post_data["username"]
    email = post_data["email"]
    password = post_data["password"]

    if not userutils.check_mail(email):
        return json.dumps(
            {
                "status": "error",
                "result": "please check your email"
            }
        )

    if len(str(password)) < 4:
        return json.dumps(
            {
                "status": "error",
                "result": "please get some serious password"
            }
        )

    user = User.objects(username=username).first()
    if user:
        return json.dumps(
            {
                "status": "error",
                "result": "this username already taken, sorry"
            }
        )

    if not username:
        return json.dumps(
            {
                "status": "error",
                "result": "please provide a username, it's required'"
            }
        )

    user = User.objects(email=email).first()
    if user:
        return json.dumps(
            {
                "status": "error",
                "result": "this email address already registered, sorry"
            }
        )

    user = User(username=username, email=email)
    user.password = userutils.encrypt(password)
    user.slug = userutils.make_slug(username)
    user.register_date = datetime.now()
    user.save()
    login_user(user)
    return json.dumps(
        {
            "status": "success",
            "result": "registeration successful"
        }
    )


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route("/user/profile/")
def profile():
    user = get_user()
    posts = Post.objects(author=user).order_by("-saved_date")
    return render_template('profile.html', user=user, posts=posts)


@app.route("/<string:seq>/<string:slug>/")
def single_post(seq, slug):
    seq = int(seq)
    user = get_user()
    post = Post.objects(seq=seq).first()
    return render_template('single.html', user=user, post=post)


@app.route("/post/scrape", methods=["POST"])
@login_required
def scrape_link():
    post_data = json.loads(request.data)
    ls = LinkScrapper(post_data["url"])
    data = ls.scrape()
    data["now"] = unicode(datetime.now())

    return json.dumps(data)


@app.route("/post/save", methods=["POST"])
@login_required
def save_post():
    post_data = json.loads(request.data)
    url = post_data["url"]
    json_data = make_readable(url)

    title = post_data["title"]
    slug = userutils.make_slug(title)
    author = User.objects(username=current_user.username).first()

    p = Post(title=title, slug=slug)
    p.saved_date = datetime.now()
    p.thumbnail = post_data["thumbnail"]
    p.url = url
    p.author = author
    p.content = json_data["content"]
    p.excerpt = json_data["excerpt"]
    p.domain = post_data["domain"]
    p.save()
    return "ok"


if __name__ == '__main__':
    app.debug = settings.DEBUG
    app.secret_key = settings.SECRET
    app.run(host="0.0.0.0", port=settings.PORT)
