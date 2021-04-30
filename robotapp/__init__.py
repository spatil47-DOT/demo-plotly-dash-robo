from flask import Flask

app = Flask(__name__)

from robotapp import routes
