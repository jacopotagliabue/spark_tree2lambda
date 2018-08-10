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

    def test_equality_parsing(self):
        # load any model here, no difference
        model_file = 'test_if_else.txt'
        test_model = self.load_model(model_file)
        # positive sign
        tokens = ['feature 100', '>=', 12.8774]
        parsed_tokens = test_model.parse_equality_test(tokens)
        assert parsed_tokens['sign'] == 1.0
        assert parsed_tokens['value'] == 12.8774
        assert parsed_tokens['index'] == 100
        # negative sign
        tokens = ['feature 0', '<=', '-', 0.23874]
        parsed_tokens = test_model.parse_equality_test(tokens)
        assert parsed_tokens['sign'] == -1.0
        assert parsed_tokens['value'] == 0.23874
        assert parsed_tokens['index'] == 0

        return

    def test_run_test_function(self):
        # load any model here, no difference
        model_file = 'test_if_else.txt'
        test_model = self.load_model(model_file)
        # first, fail equality
        tokens = ['feature 80', '>=', 12.8774]
        feature_vector = [2.6513] * 81
        parsed_tokens = test_model.parse_equality_test(tokens)
        test = test_model.run_test(parsed_tokens, feature_vector)
        assert test is False
        # then, correct equality
        tokens = ['feature 2', '<=', 12.8774]
        feature_vector = [2.6513, 232.8774, 1.8774]
        parsed_tokens = test_model.parse_equality_test(tokens)
        test = test_model.run_test(parsed_tokens, feature_vector)
        assert test is True

        return