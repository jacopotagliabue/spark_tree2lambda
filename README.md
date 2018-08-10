# spark_tree2lambda
This project is the companion code for my Medium post on serving a decision tree trained with Spark through AWS Lambda (using [Serverless](https://serverless.com/)): 
in a few minutes and a few lines of Python code you can serve predictions from a trained model through a lambda-powered endpoint(from "big-data" to "micro-services", so to speak). 

Please refer to the Medium blog [post](https://medium.com/@jacopotagliabue/serving-tensorflow-predictions-with-python-and-aws-lambda-facb4ab87ddd#.v01eyg8kh) for a full explanation on the code structure, the philosophy behind it and how to properly deploy it.

## TL;DR
We share a pure Pythonic end-to-end workflow that will get you in minutes from a model trained in Spark to a public endpoint serving predictions. The main steps are the following:

* (pre-requisite) train a decision tree model in Spark and export the serialized model to a txt file
* build a [lark](https://github.com/lark-parser/lark) grammar to parse the serialized model as it if was a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language)
* build a prediction service that recursively travels the parse tree at run time and return the prediction based on the model decision nodes
* wrap the service in an AWS lambda function that can be invoked through API Gateway

Obviously, when going from Spark serialized model to runnable Python code, a more "brute-force" approach is available - i.e. producing a python function replacing line after line Spark's syntactic features with Python's. We provide (see section below) a quick "regex+loop replace" version of that idea as well, but since
it's less interesting the endpoint in the project is powered by the parse tree (replacing that with the "brute-force" version will be trivial if one wishes to do so).

## Project structure
The lambda entry point for the endpoint is in `handler.py`, while the model conversion is made through the `spark_to_python_service.py` service. The project comes with several folders with additional materials, in particular:

* data: contains a copy of `data_banknote_authentication.csv` used to train the tree on Spark
* models: contains the serialized Spark model
* grammar: contains the Lark grammar used for parsing and interpreting the tree
* notebooks: contains a Spark notebook to load and train on Spark the banknote dataset
* playground: contains playground files to play around with Lark and different conversions options
* test_data: contains a bunch of artifical serialized models used to write tests for the main service

## Brute-force model translation
The playground folder contains the `spark_to_python_conversion.py` utility tool, that is a quick and dirty script that will take a Spark model in input and, _line after line_ sequentially replace
Spark's syntax with Python's: the result is a runnable python function, whose if/else block are "isomorphic" to the original serialized model file. It's fairly untested and basic, 
but it provides a working alternative to the fancy DSL approach we championed in the blog post.

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
