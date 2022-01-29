from datetime import datetime
from urllib.parse import quote
from flask import render_template
from rfeed import Guid, Item, Feed
from .client import last_week_of_front_pages, format_hn_front_timestamp
from .extensions import WebfeedsIcon, Webfeeds

def generate_item(day: tuple) -> Item:
	(dt, posts) = day
	info = {}

	pretty_date = dt.strftime("%x")
	info["title"] = f"Hacker News Front Page: {pretty_date}"
	
	url = f"https://news.ycombinator.com/front?day={quote(format_hn_front_timestamp(dt))}"
	info["link"] = url
	info["guid"] = Guid(url)

	info["author"] = "Hacker News submitters"
	info["pubDate"] = dt
	info["description"] = render_template("front_page.html", posts=posts)

	return Item(**info)


def create_feed():
	info = {
		"title": "Hacker News Front Page",
		"language": "en-US",
		"description": "Consume daily the best of Hacker News without constantly checking your phone.",
		"items": map(generate_item, last_week_of_front_pages().items()),
		"extensions": [
			Webfeeds(),
		],
		"lastBuildDate": datetime.now(),
		"link": "https://news.ycombinator.com/front"
	}

	return Feed(**info)
