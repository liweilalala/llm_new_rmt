from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api, resources=r'/*')

from app.api import AccessController, AIWriteController, TempWriteController
