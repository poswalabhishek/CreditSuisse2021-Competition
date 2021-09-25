import logging
import json
import numpy
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def winner_guesses(string_array):

    shuffled_set = random.sample(string_array, len(string_array))

    arr = ["Francisco Finchum", "Joseph Jarosz", "Shelli Scheuerman", "Lyman Laseter", "Spring Sawin", "Monroe Middlebrook"]

    for i in arr:
        if i in shuffled_set:
            shuffled_set[0], shuffled_set[shuffled_set.index(i)] = shuffled_set[shuffled_set.index(i)], shuffled_set[0]
    
    return shuffled_set


@app.route('/fixedrace', methods=['POST'])

def evaluateFixedRace():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input")
    string_array = data.split(',')

    result_string = winner_guesses(string_array)
    
    return (',').join(result_string)



