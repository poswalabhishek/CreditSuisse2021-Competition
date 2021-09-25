# import logging
# import json
# import hashlib
# from flask import request, jsonify
# import math

# from codeitsuisse import app

# logger = logging.getLogger(__name__)

# @app.route('/cipher-cracking', methods=['POST'])
# def evaluateCipher():
#     input_list = request.get_json()
#     logging.info("data sent for evaluation {}".format(input_list))

#     results = []
#     for input in input_list:
#         D = input['D']
#         X = input['X']
#         y = input['Y']

#         function_x = (X+1)/X * (0.57721566 + math.log(X) + 0.5/X) - 1
#         logging.info("f(x) :{}".format(function_x))
#         result = -1
#         # y = SHA256(K::f(x))
#         for K in range(0, pow(10, D)):
#             if y == hashlib.sha256(str(K) + "::" + str(function_x)):
#                 result = K
#                 break
#         results.append(result)

#     logging.info("My result :{}".format(results))
#     return json.dumps(results)



import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

import hashlib
from math import log

@app.route('/cipher-cracking', methods=['POST'])
def cipher_cracking():
    input = request.get_json()
    logging.info("Input: {}".format(input))

    output = []
    for test_case in input:
        X = int(test_case['X'])
        fx = (X+1)/X * (0.57721566 + log(X) + 0.5/X) - 1
        FX = '::{:.3f}'.format(fx)
        for K in range(1, 10**test_case['D']):
            if hashlib.sha256((str(K)+FX).encode('utf-8')).hexdigest() == test_case['Y']:                    
                break
        output.append(K)

    logging.info("Output: {}".format(output))
    return json.dumps(output)