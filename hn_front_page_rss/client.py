from datetime import datetime, timedelta, timezone
import time
from functools import lru_cache
import requests
from selectolax.parser import HTMLParser, Node

ONE_DAY = timedelta(days=1)
TIME_ZONE = timezone(timedelta(hours=-5))

def floor_datetime_day(dt: datetime):
	return datetime(
		dt.year,
		dt.month,
		dt.day
	)

def parse_hn_timestamp(timestamp: str) -> datetime:
	return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

def format_hn_front_timestamp(timestamp: str) -> datetime:
	return timestamp.strftime("%Y-%m-%d")

def pause(return_value):
	time.sleep(1)
	return return_value

def extract_post(post: Node) -> dict:
	info = {}

	title_link = post.css_first("a.titlelink")
	footer = post.next
	age = footer.css_first("span.age")


	info["title"] = title_link.text()
	info["author"] = footer.css_first("a.hnuser").text()
	info["link"] = title_link.attrs["href"]
	info["rank"] = int(post.css_first("span.rank").text().split(".")[0])
	info["points"] = int(footer.css_first("span.score").text().split(" ")[0])
	info["datetime"] = parse_hn_timestamp(age.attrs["title"])
	info["id"] = int(age.css_first("a").attrs["href"].split("=")[1])

	site_node = post.css_first("span.sitestr")
	if site_node:
		info["site"] = site_node.text()
	else:
		info["site"] = None

	return info

@lru_cache
def get_front_page(day: datetime, session=requests):
	res = session.get(
		"https://news.ycombinator.com/front",
		params={
			"day": day.strftime("%Y-%m-%d")
		}
	)

	res.raise_for_status()
	text = res.text

	tree = HTMLParser(text)
	posts = tree.css("table.itemlist tr[id]")
	return list(map(extract_post, posts))

def last_week_of_front_pages():
	today = floor_datetime_day(datetime.now(tz=TIME_ZONE))
	week = [today - (ONE_DAY * x) for x in range(1, 8)]
	return {
		day: pause(get_front_page(day))
		for day in week
	}

if __name__ == "__main__":
	print(last_week_of_front_pages())
