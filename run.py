# -*- coding: utf-8 -*-
import os

from app import create_app
from app import Config

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()
app.run(debug=app.config['IS_DEBUG'], port=5555, host='127.0.0.1')#app.config['HOST'] app.config['PORT']
# app.run(debug=app.config['IS_DEBUG'], port=app.config['PORT'], host=app.config['HOST'], ssl_context=(app.config['CERT'], app.config['KEY']))
