import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])
def evaluateDecoder ():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    output = data["history"][0]["output_received"]
    result = {}
    result['answer'] = random.sample(output, len(output))

    return json.dumps(result)



