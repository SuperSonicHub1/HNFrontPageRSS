from hn_front_page_rss import create_app

app = create_app()
app.run("0.0.0.0", 8080, debug=False,)
