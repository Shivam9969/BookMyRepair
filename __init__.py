from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'af0d2f8753dbcbd945cdf58b8522ff21'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/Images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from bookmyrepair import routes
from bookmyrepair.products import routes
from bookmyrepair.carts import carts
from bookmyrepair.customers import routes

