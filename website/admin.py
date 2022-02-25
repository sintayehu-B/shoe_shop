from flask.helpers import url_for
from flask_admin import Admin
from website import admin, db
from flask import Blueprint
from werkzeug.utils import redirect
from website.models import Order, Product, User
from flask_admin.contrib.sqla import ModelView

admin_blue = Blueprint('admin_blue', __name__)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))
# admin.add_view(ModelView(Ordersbatch, db.session))