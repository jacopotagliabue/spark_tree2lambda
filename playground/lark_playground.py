"""
    This is just a playground script to play around with Lark functions.
    It can be changed/removed at will as it is completely separate from the lambda code: code
    is left here with some simple test methods for users that would like to get familiar with
    lark parsing starting from some minimal examples.
"""
from lark import Lark
from datetime import datetime
import os
from spark_to_python_service import Spark2Python
import ConfigParser


def compile_and_parse(grammar, command):
    lark_grammar = Lark(grammar)
    parse_tree = lark_grammar.parse(command)
    # print it out
    print parse_tree, parse_tree.pretty()
    return parse_tree


def test_hello_world(hello_world_string):
    grammar = '''start: WORD "," WORD "!"
    
                %import common.WORD   // imports from terminal library
                %ignore " "           // Disregard spaces in text
             '''

    return compile_and_parse(grammar, hello_world_string)


def test_logo_parsing(logo_command):
    # http://blog.erezsh.com/how-to-write-a-dsl-in-python-with-lark/
    grammar = '''start: instruction+
 
                instruction: MOVEMENT NUMBER            -> movement
                           | "c" COLOR [COLOR]          -> change_color
                           | "fill" code_block          -> fill
                           | "repeat" NUMBER code_block -> repeat
                 
                code_block: "{" instruction+ "}"
                 
                MOVEMENT: "f"|"b"|"l"|"r"
                COLOR: LETTER+
                 
                %import common.LETTER
                %import common.INT -> NUMBER
                %import common.WS
                %ignore WS

                 '''

    return compile_and_parse(grammar, logo_command)


def test_if_else_parsing(if_command):
    grammar = '''start: if_else_block+

                prediction: PREDICT FLOAT -> predict
                comparison_block: BOOLEAN "(" FEATURE CONDITION SIGN? FLOAT ")" -> compare
                boolean_block: comparison_block RETURN prediction
                if_else_block: boolean_block RETURN boolean_block RETURN?
                
                FEATURE: "feature " NUMBER
                BOOLEAN: "If"|"Else"
                CONDITION: "="|"<="|">="|">"|"<"
                PREDICT: "Predict:"
                SPACE: " "
                RETURN: "\\n"
                SIGN: "-"

                %import common.INT -> NUMBER
                %import common.FLOAT -> FLOAT
                %ignore SPACE
                '''

    return compile_and_parse(grammar, if_command)


def test_recursive_if_else_parsing(rec_if_command):
    # NOTE THAT WHEN GRAMMAR GOES TO A TXT FILE, \n DOES NOT NEED ESCAPING!
    grammar = '''start: full_comparison+
    
                test: FEATURE CONDITION SIGN? FLOAT
                if_comparison:  IF "(" test ")" RETURN -> if_compare
                else_comparison: ELSE "(" test ")" RETURN -> else_compare
                prediction: PREDICT FLOAT RETURN -> predict
                instructions: full_comparison RETURN? | prediction RETURN?
                if_block: if_comparison instructions+
                else_block: else_comparison instructions+
                full_comparison: if_block else_block 

                FEATURE: "feature " NUMBER
                IF: "If"
                ELSE: "Else"
                CONDITION: "="|"<="|">="|">"|"<"
                PREDICT: "Predict:"
                SPACE: " "
                RETURN: "\\n"
                SIGN: "-"

                %import common.INT -> NUMBER
                %import common.FLOAT -> FLOAT
                %ignore SPACE
                '''

    return compile_and_parse(grammar, rec_if_command)


def basic_testing():
    # simple hello world parsing
    hello_command = "Hello, World!"
    test_hello_world(hello_command)
    # logo DSL parsing
    logo_command = """
        c red yellow
        fill { repeat 36 {
            f200 l170
        }}    
        """
    test_logo_parsing(logo_command)
    # if parsing
    if_command = """If (feature 1 <= 5.496)\n Predict: 1.0\nElse (feature 1 > -5.496)\n Predict: 2.0"""
    print if_command
    test_if_else_parsing(if_command)
    # recursive if parsing
    recursive_if_command = """  If (feature 0 <= -3.9172)\n   If (feature 2 <= 0.61663)\n    Predict: 1.0\n   Else (feature 2 > 0.61663)\n    Predict: 2.0\n  Else (feature 0 > -3.9172)\n   Predict: 3.0\n"""
    print recursive_if_command
    test_recursive_if_else_parsing(recursive_if_command)
    return


def service_testing():
    HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    settings_path = os.path.join(HERE, 'settings.ini')
    Config = ConfigParser.ConfigParser()
    Config.read(settings_path)
    # init spark2python "service"
    MODEL_NAME = Config.get('app_data', 'MODEL_NAME')
    GRAMMAR_NAME = Config.get('app_data', 'GRAMMAR_NAME')
    model_file_path = os.path.join(HERE, 'models', MODEL_NAME)
    grammar_file_path = os.path.join(HERE, 'grammars', GRAMMAR_NAME)
    spark2python = Spark2Python(model_file_path, grammar_file_path, verbose=False)
    feature_vector = [-0.46279, 4.496, 6.5779, 2.0]
    prediction = spark2python.interpret_model(spark2python.parse_tree, feature_vector, verbose=True)
    print 'prediction {}'.format(prediction)
    feature_vector = [-0.3579, 9.496, 6.5779, 2.0]
    prediction = spark2python.interpret_model(spark2python.parse_tree, feature_vector, verbose=True)
    print 'prediction {}'.format(prediction)
    feature_vector = [0.21874, 4.2986, 1.123, 2.0]
    prediction = spark2python.interpret_model(spark2python.parse_tree, feature_vector, verbose=True)
    print 'prediction {}'.format(prediction)

    return


def main():
    # basic_testing()
    service_testing()
    print "\n==================================\nAll done at {}! See you, space cowboys...".format(datetime.utcnow())
    return


if __name__ == "__main__":
    main()
