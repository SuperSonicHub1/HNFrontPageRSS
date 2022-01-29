# Hacker News Front Page RSS

Consume daily the best of Hacker News without constantly
checking your phone.

This works through scraping multiple days of
[the front page archive][front] off the site. If anyone
knows how to do this with either of the APIs so I can
avoid rate limiting the site, feel free to write an issue!

## Install
```bash
poetry install
# For the lazy...
python3 main.py
# For the more upstanding
gunicorn 'hn_front_page_rss:create_app()'
```

[front]: https://news.ycombinator.com/front
