from flask import Blueprint, render_template, Response
from .generator import create_feed

views = Blueprint("views", __name__, url_prefix="/")

@views.route('/')
def index():
	return render_template("index.html")

@views.route('/feed')
def feed():
	feed = create_feed()
	return Response(feed.rss(), mimetype='application/rss+xml')
