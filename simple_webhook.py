from github_webhook import Webhook
from flask import Flask
import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)   # Standard Flask app
webhook = Webhook(app)  # Defines '/postreceive' endpoint


@app.route("/")        # Standard Flask endpoint
def hello_world():
    logging.debug('Hello World!')
    return "Hello, World!"


# Define a handler for the 'push' event
@webhook.hook()
def on_push(data):
    logging.debug("Got push event with: {0}".format(data))


# Define a handler for the "issues" event
@webhook.hook(event_type='issues')
def on_issues(data):
    logging.debug("Got issues event with: {0}".format(data))


# Define a handler for the "issue_comment" event
@webhook.hook(event_type='issue_comment')
def on_issue_comment(data):
    logging.debug("Got issue_comment event with: {0}".format(data))


if __name__ == "__main__":
    app.run()
