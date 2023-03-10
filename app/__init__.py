import cloudinary

from os.path import join, dirname, realpath
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)

# app.config.from_object('config.DevConfig')

app.config['SECRET_KEY'] = '979e67f91832404eba0261aeeaae4a11'

app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

CORS(app)
jwt = JWTManager(app)


cloudinary.config(
  cloud_name = "dpwbqxs1u",
  api_key = "189568311428829",
  api_secret = "yiHPrIheAi0SvDTDes11CVmXSjY"
)

# BluePrints
from app.auth_api.views import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.user_api.views import user_bp
app.register_blueprint(user_bp, url_prefix='/user')

from app.request_api.views import req_bp
app.register_blueprint(req_bp, url_prefix='/request')

from app import views
