import logging
import json
import numpy as np
from scipy.stats import norm 

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def expected_return_per_view(option_dict, view_dict):

    strike = option_dict['strike']
    premium = option_dict['premium']

    if option_dict['type'] == 'call':

        if strike >= view_dict['max']:
            return -premium
        else:
            a = view_dict['min']
            b = view_dict['max']
            c = max(a, strike)
            mu = view_dict['mean']
            sigma = (view_dict['var'])
            alpha = (a - mu)/sigma
            beta = (b - mu)/sigma
            gamma = (c - mu)/sigma

            multiplier1 = (norm.cdf(beta) - norm.cdf(gamma))/(norm.cdf(beta) - norm.cdf(alpha))
            multiplier2 = mu - strike - (sigma*(norm.pdf(beta) - norm.pdf(gamma))/(norm.cdf(beta) - norm.cdf(gamma)))
            return (multiplier1 * multiplier2) - premium

    else:

        if strike <= view_dict['min']:
            return -premium
        else:
            a = view_dict['min']
            b = view_dict['max']
            c = min(b, strike)
            mu = view_dict['mean']
            sigma = (view_dict['var'])
            alpha = (a - mu)/sigma
            beta = (b - mu)/sigma
            gamma = (c - mu)/sigma

            multiplier1 = (norm.cdf(gamma) - norm.cdf(alpha))/(norm.cdf(beta) - norm.cdf(alpha))
            multiplier2 = strike - mu + (sigma*(norm.pdf(gamma) - norm.pdf(alpha))/(norm.cdf(gamma) - norm.cdf(alpha)))
            return (multiplier1 * multiplier2) - premium

def expected_return_all_views(option_dict, view_dicts):
    numerator = 0
    denominator = 0

    for view_dict in view_dicts:
        numerator += (view_dict['weight'] * expected_return_per_view(option_dict, view_dict))
        denominator += view_dict['weight']

    return numerator/denominator

@app.route('/optopt', methods=['POST'])
def evaluateOptions():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    
    max_val = 0
    max_abs_val = 0
    max_pos = 0
    for pos in range(len(data['options'])):
        val = expected_return_all_views(data['options'][pos], data['view'])
        abs_val = abs(val)
        if max_abs_val < abs_val:
            max_abs_val = abs_val
            max_val = val
            max_pos = pos

    result = [0] * len(data['options'])
    if max_val < 0:
        result[max_pos] = -100
    else:
        result[max_pos] = 100
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)



