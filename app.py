#!/usr/bin/env python

import app_config
import datetime
import json
import logging
import oauth
import static

from flask import Flask, make_response, render_template
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from models import models
from render_utils import make_context, smarty_filter, urlencode_filter
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
app.debug = app_config.DEBUG
admin = Admin(app, name=app_config.PROJECT_SLUG)
admin.add_view(ModelView(models.TestModel))

logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)

try:
    file_handler = logging.FileHandler('%s/public_app.log' % app_config.SERVER_LOG_PATH)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
except IOError:
    logger.warn('Could not open %s/public_app.log, skipping file-based logging' % app_config.SERVER_LOG_PATH)

app.logger.setLevel(logging.INFO)

app.register_blueprint(static.static, url_prefix='/%s' % app_config.PROJECT_SLUG)
app.register_blueprint(oauth.oauth, url_prefix='/%s' % app_config.PROJECT_SLUG)

app.add_template_filter(smarty_filter, name='smarty')
app.add_template_filter(urlencode_filter, name='urlencode')

# Example of rendering index.html with public_app
@app.route ('/%s/' % app_config.PROJECT_SLUG, methods=['GET'])
@oauth.oauth_required
def index():
    """
    Example view rendering a simple page.
    """
    context = make_context(asset_depth=1)

    return make_response(render_template('index.html', **context))

# Enable Werkzeug debug pages
if app_config.DEBUG:
    wsgi_app = DebuggedApplication(app, evalex=False)
else:
    wsgi_app = app

# Catch attempts to run the app directly
if __name__ == '__main__':
    logger.error('This command has been removed! Please run "fab public_app" instead!')
