import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

# def winner_guesses():


@app.route('/fixedrace', methods=['POST'])

def evaluateFixedRace():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input")

    return ""



