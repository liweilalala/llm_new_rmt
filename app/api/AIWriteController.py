from flask import request, jsonify
from . import api
import json


@api.route('/api/AIWrite', methods=['POST'])
def ai_write():

    return jsonify({"Hello world"})