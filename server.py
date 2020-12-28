import os
from bottle import Bottle, response
import sentry_sdk
from sentry_sdk.integrations.bottle import BottleIntegration
from config import key_project

sentry_sdk.init(
    dsn=key_project,
    integrations=[BottleIntegration()]
)

app = Bottle()


@app.route("/")
def index():
	html = """
		<!doctype html>
		<html lang="en">
		<head>
			<title>Сервер</title>
		</head>
		<body>
			<div class="container">
			<h1>Добрый день!</h1>
			<h3>Тест работы сервера...</h3>
			</div>
		</body>
		</html>
	"""
	return html

@app.route("/success")
def success():
	html = """
		<!doctype html>
		<html lang="en">
		<head>
			<title>Сервер</title>
		</head>
		<body>
			<div class="container">
				<h2>HTTP статус: {}</h2>
				<hr>
				<h3>Тест работы сервера...</h3>
			</div>
		</body>
		</html>
	""".format(response.status)
	return html

@app.route("/fail")
def fail():
	raise RuntimeError("There is an error!")    

if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)
