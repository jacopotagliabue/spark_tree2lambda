# spark_tree2lambda
This project is the companion code for my Medium post on serving a decision tree trained with Spark through AWS Lambda (using [Serverless](https://serverless.com/)): in a few minutes and a few lines of Python code you can serve predictions from a trained model through a lambda-powered endpoint. 

Please refer to the Medium blog [post](https://medium.com/@jacopotagliabue/serving-tensorflow-predictions-with-python-and-aws-lambda-facb4ab87ddd#.v01eyg8kh) for a full explanation on the code structure, the philosophy behind it and how to properly deploy it.

## TL;DR
We share a pure Pythonic end-to-end workflow that will get you in minutes from a model trained in Spark to a public endpoint serving predictions. The steps

## Project structure
The lambda entry point for the endpoint is in `handler.py`, while the model conversion is made through the `spark_to_python_service.py` service. The project comes with several folders with additional materials, in particular:

* data: contains a copy of `data_banknote_authentication.csv` used to train the tree on Spark
* models: contains the serialized Spark model
* grammar: contains the Lark grammar used for parsing and interpreting the tree
* notebooks: contains a Spark notebook to load and train on Spark the banknote dataset
* playground: contains playground files to play around with Lark and different conversions options
* test_data: contains a bunch of artifical serialized models used to write tests for the main service

## Brute-force model translation

## Deployment
Make sure to have Serverless installed and configured with AWS credentials; then, install with pip the dependencies in a project folder (e.g. `vendored`):

``` 
pip install -t vendored/ -r requirements.txt
```

and finally deploy to AWS with:

```serverless deploy```

## Tests
Tests built with [pytest](https://docs.pytest.org/). Use

```pytest test_spark2python.py```

to run some basic tests.
