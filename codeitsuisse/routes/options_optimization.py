import logging
import json

from flask import request, jsonify

from codeitsuisse import app
import numpy as np

logger = logging.getLogger(__name__)

from scipy.stats import norm
from math import sqrt

@app.route('/optopt', methods=['POST'])
def optopt():
    input = request.get_json()
    logging.info("Input: {}".format(input))

    option_dicts = input['options']
    view_dicts = input['view']

    expected_returns_list = [0] * len(option_dicts)

    for view_dict in view_dicts:
        mu = view_dict['mean']
        sigma = sqrt(view_dict['var'])
        a = view_dict['min']
        b = view_dict['max']
        aa = np.divide(np.subtract(a, mu), sigma)
        bb = np.divide(np.subtract(b, mu), sigma)
        cdf_aa = norm.cdf(aa)
        cdf_bb = norm.cdf(bb)
        pdf_aa = norm.pdf(aa)
        pdf_bb = norm.pdf(bb)
        diff_cdf_bb_aa = cdf_bb - cdf_aa
    
        for pos in range(len(option_dicts)):
            option_dict = option_dicts[pos]
            strike = option_dict['strike']
            expected_return_of_view = -option_dict['premium']

            if option_dict['type'] == 'call' and strike < b:
                c = max(a, strike)
                cc = np.divide(np.subtract(c, mu), sigma)
                cdf_cc = norm.cdf(cc)
                pdf_cc = norm.pdf(cc)
                increment = np.subtract(np.multiply(np.subtract(cdf_bb, cdf_cc), np.subtract(mu, strike))), (np.multiply(np.subtract(pdf_bb, pdf_cc), sigma))
                increment /= diff_cdf_bb_aa
                expected_return_of_view += increment
            
            if option_dict['type'] == 'put' and strike > a:
                d = min(b, strike)
                dd = np.divide(np.subtract(d, mu), sigma)
                cdf_dd = norm.cdf(dd)
                pdf_dd = norm.pdf(dd)
                increment = np.add(np.multiply(np.subtract(cdf_dd, cdf_aa), np.subtract(strike, mu)), np.multiply(np.subtract(pdf_dd, pdf_aa), sigma))
                increment /= diff_cdf_bb_aa
                expected_return_of_view += increment

            expected_returns_list[pos] += view_dict['weight'] * expected_return_of_view

    
    max_abs_val = 0
    argmax_val = 0
    argmax_pos = 0
    for pos in range(len(option_dicts)):
        val = expected_returns_list[pos]
        abs_val = abs(val)
        if max_abs_val < abs_val:
            max_abs_val = abs_val
            argmax_val = val
            argmax_pos = pos

    output = [0] * len(option_dicts)
    if argmax_val < 0:
        output[argmax_pos] = -100
    else:
        output[argmax_pos] = 100

    logging.info("Output: {}".format(output))
    return json.dumps(output)