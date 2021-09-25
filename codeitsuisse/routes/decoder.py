import logging
import json
import random
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])

def right_and_wrong_symbols_position_result(result):
    right_symbol_right_position = result % 10
    right_symbol_wrong_position = (result // 10) % 10

    return right_symbol_right_position, right_symbol_wrong_position

def evaluateDecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = data["history"]["output_received"]

    result = random.sample(result, len(result))

    logging.info("My result :{}".format(result))
    return json.dumps(result)



