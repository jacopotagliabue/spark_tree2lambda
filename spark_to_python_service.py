from __future__ import print_function
from lark import Lark, Tree


class Spark2Python:

    def __init__(self, model_file_path, grammar_file_path, verbose=False):
        self.verbose = verbose
        # get the grammar
        grammar = self.load_grammar(grammar_file_path)
        # get the model first
        spark_model = self.load_model(model_file_path)
        # log the model
        if self.verbose:
            print('Model:\n{}'.format(spark_model))
        # store the parse tree as a class variable for later parsing
        self.parse_tree = grammar.parse(spark_model)
        # log tree
        if self.verbose:
            print('Pretty parse tree: {}'.format(self.parse_tree.pretty()))
        return

    def load_grammar(self, grammar_file_path):
        """
        Return a Lark grammar to be used later for parsing

        :param grammar_file_path: path to a txt file containing grammar to parse the serialized Spark model
        :return: Lark grammar
        """
        with open(grammar_file_path, 'r') as g_file:
            data = g_file.read()
        return Lark(data)

    def load_model(self, model_file_path):
        """
        Read serialized model from txt file

        :param model_file_path: path to a txt file containing Spark model
        :return: serialized file as a string
        """
        with open(model_file_path, 'r') as m_file:
            # ATTENTION: make sure to skip the first line
            # which contains model description
            next(m_file)
            serialized_model = ''.join([l for l in m_file])
        return serialized_model

    def predict(self, feature_vector):
        """
        Encapsulate prediction made by intepreting the parse tree. Just here as an "interface" for the
        endpoint in case later prediction comes from a class or other "more stable" methods than
        real time parsing!

        :param feature_vector: list of features values, in the same order as model feature, from 1 to n
        :return: target class from decision tree
        """
        return self.interpret_model(self.parse_tree, feature_vector, verbose=self.verbose)

    def interpret_model(self, parse_tree, feature_vector, verbose=False):
        """
        Take a parse tree from Lark grammar of a Spark model and a feature vector and run through the tree
        checking, feature by feature, which conditions apply and which prediction the model would make.

        :param parse_tree: lark parse tree of a Spark model
        :param feature_vector: list of features values, in the same order as model feature, from 1 to n
        :return: target class from decision tree
        """

        return self.run_instruction(parse_tree.children[0], feature_vector, verbose=verbose)

    def run_instruction(self, sub_tree, feature_vector, verbose=False):
        """

        :param sub_tree: a lark (sub) tree to navigate
        :param feature_vector: list of features values, in the same order as model feature, from 1 to n
        :param verbose: print out messages to the console for verbose logging
        :return: prediction from the model as one of the terminal leaves is reached
        """
        if type(sub_tree) is not Tree:
            print('token: {}'.format(sub_tree))
        else:
            data = sub_tree.data
            children = sub_tree.children
            # we find an equality test:
            if data == 'instructions':
                if children[0].data == 'predict':
                    # parse and return prediction: we are at max depth!
                    return self.parse_predicted_value(children[0].children)
                else:
                    # there is some nested IF, continue the recursion
                    return self.run_instruction(children[0], feature_vector, verbose=verbose)
            if data == 'full_comparison':
                # get two main branch
                if_block = children[0]
                else_block = children[1]
                # test first IF
                tokens = if_block.children[0].children[1].children
                # all children are tokens composing the equality, e.g. feature 0 <= -0.23874
                # get feature index, sign, test type and test value
                parsed_tokens = self.parse_equality_test(tokens)
                test = self.run_test(parsed_tokens, feature_vector, verbose=verbose)
                if test:
                    # if equality is satisfied, go down the IF block
                    return self.run_instruction(if_block.children[1], feature_vector, verbose=verbose)
                else:
                    # else, go down the ELSE block
                    return self.run_instruction(else_block.children[1], feature_vector, verbose=verbose)

    def run_test(self, test_tokens, feature_vector, verbose=False):
        """
        Run the test comparing feature value with test value, e.g. <=(feature 0, -0.23874)

        :param test_tokens: tokens as parsed
        :param feature_vector: list of features values, in the same order as model feature, from 1 to n
        :return: boolean, as the result of the comparison
        """
        # prepare params
        test_val = test_tokens['value']
        condition_function = test_tokens['condition']
        feature_val = feature_vector[test_tokens['index']]
        sign = test_tokens['sign']
        # run comparison
        comparison = condition_function(feature_val, test_val * sign)
        # log stuff
        if verbose:
            print("Running test: {}, feature val {}, result {}".format(test_tokens, feature_val, comparison))

        return comparison

    def parse_predicted_value(self, tokens):
        """

        :param tokens: tokens composing the prediction instruction
        :return: prediction
        """
        return tokens[1]

    def parse_equality_test(self, tokens):
        """
        Parse token into components

        :param tokens: tokens composing the equality test, e.g. [feature 0, <=, -, 0.23874]
        :return: wrapper around the different test components
        """
        feature_index = int(tokens[0].split(' ')[-1])
        condition = tokens[1]
        value = float(tokens[-1])

        # check for both tokens length and exact sign
        if len(tokens) == 4 and tokens[2] == '-':
            sign = -1.0
        else:
            sign = 1.0

        parsed_tokens = {
            'sign': sign,
            'value': value,
            'condition': self.get_condition_function(condition),
            'condition_string': condition,
            'index': feature_index
        }

        return parsed_tokens

    def get_condition_function(self, condition_string):
        """
        Map string for conditions ("="|"<="|">="|">"|"<") to equivalent runnable lambdas

        :param condition_string: condition for the equality test
        :return: lambda representing the condition to be tested
        """
        if condition_string == '=':
            return lambda x, y: x == y
        elif condition_string == '<=':
            return lambda x, y: x <= y
        elif condition_string == '>=':
            return lambda x, y: x >= y
        elif condition_string == '>':
            return lambda x, y: x > y
        elif condition_string == '<':
            return lambda x, y: x < y
        else:
            # this should not happen, since lark grammar would fail otherwise
            raise Exception('Sign not recognized!')