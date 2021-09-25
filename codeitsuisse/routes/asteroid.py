import logging
import json

from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)


# step 1: preprocess
# step 2: prepare the function (destroyed_asteroid_score)
# step 3: call the function

def calculate_multiplier(asteroid_destroyed):
    multiplier = 0
    if asteroid_destroyed <= 6:
        multiplier = 1
    elif asteroid_destroyed >= 7 and asteroid_destroyed < 10:
        multiplier = 1.5
    else:
        multiplier = 2
    
    return multiplier

def score_update(score, new_score):
    if score < new_score:
        return new_score
    return score

def score_and_origin_update(score, new_score, origin, asteroid_type_and_value, letter_origin):
    if score < new_score:
        score = new_score
        origin = 0
        for i in range(0, letter_origin - 1):
            origin += asteroid_type_and_value[i][1]
        origin += (asteroid_type_and_value[letter_origin][1])//2
        return score, origin
    return score, origin


def destroyed_asteroid_score(input_string, asteroid_type_and_value):

    letter_origin = 0
    score = 0
    origin = 0
    asteroid_destroyed = 0
    total_non_consecutive_letter = len(asteroid_type_and_value) - 1

    for i in asteroid_type_and_value:

        if letter_origin == 0:
            asteroid_destroyed = asteroid_type_and_value[letter_origin][1]
            multiplier = calculate_multiplier(asteroid_destroyed)
            score1 = asteroid_destroyed * multiplier
            score = score_update(score, score1)
            score, origin = score_and_origin_update(score, score2, origin, asteroid_type_and_value, letter_origin)
        elif letter_origin == total_non_consecutive_letter:
            asteroid_destroyed = asteroid_type_and_value[letter_origin][1]
            multiplier = calculate_multiplier(asteroid_destroyed)
            score2 = asteroid_destroyed * multiplier
            score = score_update(score, score2)
            score, origin = score_and_origin_update(score, score2, origin, asteroid_type_and_value, letter_origin)
        else: 
            asteroid_destroyed = asteroid_type_and_value[letter_origin][1]
            prev_origin = letter_origin - 1
            next_origin = letter_origin + 1
            multiplier = calculate_multiplier(asteroid_destroyed)
            score3 = asteroid_destroyed * multiplier
            while prev_origin >= 0 and next_origin <= total_non_consecutive_letter:
                if asteroid_type_and_value[prev_origin][0] != asteroid_type_and_value[next_origin][0]:
                    break

                asteroid_destroyed = asteroid_type_and_value[prev_origin][1] + asteroid_type_and_value[next_origin][1]
                prev_origin -= 1
                next_origin += 1

                multiplier = calculate_multiplier(asteroid_destroyed)
                score3 += asteroid_destroyed * multiplier
                score = score_update(score, score3)
                score, origin = score_and_origin_update(score, score2, origin, asteroid_type_and_value, letter_origin)
        letter_origin += 1

    return score, origin

@app.route('/asteroid', methods=['POST']) # change the /square to whatever the requirements are

def evaluateAsteroidScore():
    input = request.get_json()
    logging.info("Input {}".format(input))

    output = []

    for inputString in input['test_cases']:
        '''
        preprocess: create a list of tuple that hold an integer value to the number of times same asteroid has appeared consecutively
        example: 
        input_string: "CCCAAABBBAAACCCx" -> added x to check the validity
        asteroid_type_and_value = [(C, 3), (A, 3), (B, 3), (A, 3), (C, 3)]
        '''
        case_output = {}
        case_output['input'] = inputString

        input_string = inputString + 'x'
        asteroid_type_and_value = []
        asteroid_type = input_string[0]
        asteroid_value = 0

        for input_char in input_string:
            if input_char == asteroid_type:
                asteroid_value += 1
            else:
                asteroid_type_and_value.append((asteroid_type, asteroid_value))
                asteroid_type = input_char
                asteroid_value = 1        

        score, origin = destroyed_asteroid_score(input_string, asteroid_type_and_value)
        case_output['score'] = score
        case_output['origin'] = origin
        output.append(case_output)


    logging.info("Output :{}".format(output))
    return json.dumps(output)



