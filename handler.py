from __future__ import print_function
import os
import sys
import json
import time
from distutils import util
from datetime import datetime
# this is needed so that the script running on AWS will pick up the pre-compiled dependencies
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "vendored"))
# import non standard dependencies
from spark_to_python_service import Spark2Python
# init spark2python "service"
MODEL_NAME = os.environ['MODEL_NAME']
GRAMMAR_NAME = os.environ['GRAMMAR_NAME']
VERBOSE = bool(util.strtobool(os.environ['VERBOSE']))
model_file_path = os.path.join(HERE, 'models', MODEL_NAME)
grammar_file_path = os.path.join(HERE, 'grammars', GRAMMAR_NAME)
spark2python = Spark2Python(model_file_path, grammar_file_path, verbose=VERBOSE)


def predict(event, context):
    """
    Predict target value with pre-trained decision tree model

    "event" and "context" are the standard AWS lambda parameters - in our case "event" will contain a list
    of query string parameters as they are passed through API Gateway

    TEST GET CALL: https://LAMBDAURL.us-west-2.amazonaws.com/dev/predict?features=-0.46279,4.496,6.5779,2.0
    TEST GET CALL WITH DEBUG FLAG: https://LAMBDAURL.us-west-2.amazonaws.com/dev/predict?debug=1
    """
    # start a timer
    start = time.time()
    # get parameter from query string
    params = event['queryStringParameters']
    # acknowledge the start of the function in AWS console
    print("Request received with params {} at {}".format(json.dumps(params), datetime.utcnow()))
    # if one params is "debug", just use static data for demonstration
    if 'debug' in params:
        feature_vector = [-0.46279, 4.496, 6.5779, 2.0]
    # else parse params
    else:
        feature_vector = [float(f) for f in params['features'].split(',')]
    predicted_class = spark2python.predict(feature_vector)
    response = {
        'prediction': predicted_class,
        'features': feature_vector,
        'debug': 'debug' in params,
        'time': time.time() - start
    }
    # acknowledge the end of the function in AWS console
    print("Response prepared: {}".format(json.dumps(response)))
    return return_lambda_gateway_response(200, response)


def return_lambda_gateway_response(code, body):
    """
    Just a wrapper to return an API Gateway friendly response
    :param code: status code for HTTP response (should be int or castable to int)
    :param body: response body, will be converted to json

    The response to the client will be handle accordingly by API Gateway
    """
    return {"statusCode": int(code), "body": json.dumps(body)}
