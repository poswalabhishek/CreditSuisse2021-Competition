import logging
import json
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def winner_guesses(string_array):

    return random.shuffle(string_array)


@app.route('/fixedrace', methods=['POST'])

def evaluateFixedRace():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input")
    string_array = data.split(',')

    result_string = winner_guesses(string_array)
    
    return (',').join(result_string)



