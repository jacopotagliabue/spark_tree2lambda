"""
    Example class providing very simple tests to check the service is doing the proper conversion.
    Obv. would need improvement for PROD use!
"""
from __future__ import print_function
import os
from spark_to_python_service import Spark2Python
import ConfigParser
HERE = os.path.dirname(os.path.realpath(__file__))
# global variables living across requests
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(HERE, 'settings.ini'))
# init spark2python "service"
GRAMMAR_NAME = Config.get('app_data', 'GRAMMAR_NAME')
GRAMMAR_FILE_PATH = os.path.join(HERE, 'grammars', GRAMMAR_NAME)


class TestSpark2Python(object):

    def load_model(self, test_file_path):
        model_file_path = os.path.join(HERE, 'test_data', test_file_path)
        return Spark2Python(model_file_path, GRAMMAR_FILE_PATH)

    def test_simple_if_else(self):
        model_file = 'test_if_else.txt'
        test_model = self.load_model(model_file)
        class_zero_feature_vectors = [[0.957]]
        class_one_feature_vectors = [[0.257]]
        for zero_f, one_f in zip(class_zero_feature_vectors, class_one_feature_vectors):
            assert test_model.predict(zero_f) == '0.0'
            assert test_model.predict(one_f) == '1.0'

        return

    def test_simple_if_else_negative(self):
        model_file = 'test_if_else_negative.txt'
        test_model = self.load_model(model_file)
        class_zero_feature_vectors = [[-9.9080]]
        class_one_feature_vectors = [[-30]]
        for zero_f, one_f in zip(class_zero_feature_vectors, class_one_feature_vectors):
            assert test_model.predict(zero_f) == '0.0'
            assert test_model.predict(one_f) == '1.0'

        return

    def test_simple_if_else_nested(self):
        model_file = 'test_nested_if_else.txt'
        test_model = self.load_model(model_file)
        class_zero_feature_vectors = [[-6.0, 12.986], [2.98, 8.1276]]
        class_one_feature_vectors = [[-20.9090, 1.2133], [-4.8790, 0.789]]
        for zero_f, one_f in zip(class_zero_feature_vectors, class_one_feature_vectors):
            assert test_model.predict(zero_f) == '0.0'
            assert test_model.predict(one_f) == '1.0'

        return


