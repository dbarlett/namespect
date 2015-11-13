import os
from flask import Flask

app = Flask(
    __name__.split(".")[0],
    static_folder=os.path.join(os.getcwd(), "public"),
    static_url_path="/"
)
app.config.from_object("config")

from core import models
from core import views
