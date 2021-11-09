import logging
from warnings import warn
import os
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.WARN)

app = Flask(__name__)
#######################################################
try:
    REVERSE_PROXY_PATH = os.environ['HITO_DATABASE_FRONTEND_REVERSE_PROXY_PATH']
    app.config['REVERSE_PROXY_PATH'] = REVERSE_PROXY_PATH
    ReverseProxyPrefixFix(app)
    print('HITO_DATABASE_FRONTEND_REVERSE_PROXY_PATH='+REVERSE_PROXY_PATH)
except:
    warn('HITO_DATABASE_FRONTEND_REVERSE_PROXY_PATH environment variable not set. This installation may not work when served under a folder.')

#######################################################
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, base_template='base.html')


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
