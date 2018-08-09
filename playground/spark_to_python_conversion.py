"""
    This is just a playground script to demonstrate how to do a "find and replace" conversion between the serialized
    Spark tree and a python runnable function (i.e. a series of nested if-else).
    It's fairly untested and just here to provide an alternative, brute-force method to the grammar-based one
    explored in the main service.
"""


import os
from datetime import datetime
import time
import ConfigParser
import re


# get file paths to run the program from config
HERE = os.path.dirname(os.path.realpath(__file__))
PROJECT_FOLDER = os.path.abspath(os.path.join(HERE, os.pardir))
MODELS_FOLDER = os.path.join(PROJECT_FOLDER, 'models')
settings_path = os.path.join(PROJECT_FOLDER, 'settings.ini')
Config = ConfigParser.ConfigParser()
Config.read(settings_path)
MODEL_NAME = Config.get('app_data', 'MODEL_NAME')
MODEL_PATH = os.path.join(MODELS_FOLDER, MODEL_NAME)
OUTPUT_FILE_PATH = os.path.join(HERE, 'spark_decision_tree_{}.py'.format(int(time.time())))
DECISION_TREE_FUNCTION_NAME = 'predict_with_decision_tree'
DECISION_TREE_INPUT_NAME = 'feature_vector'  # name of the param containing features as input to the final Python code


def convert_spark_to_python(function_name, input_name, input_file_path, output_file_path):
    with open(input_file_path, 'r') as m_file:
        with open(output_file_path, 'w') as o_file:
            # ATTENTION: the first line contains model description
            model_description = next(m_file).strip()
            model_instructions = [l.rstrip() for l in m_file]
            # setup the main function
            setup_function = '''def {}({}):\n  """{}"""\n\n'''.format(function_name,
                                                                      input_name,
                                                                      model_description)
            o_file.write(setup_function)
            # loop over line in the model and write the converted version
            for i in model_instructions:
                o_file.write('{}\n'.format(spark_instruction_to_python(DECISION_TREE_INPUT_NAME, i)))

            # finally invoke the function with some known params and print out result
            invoke_function = "print {}({})".format(function_name, [-0.3579, 9.496, 6.5779, 2.0])
            o_file.write('{}\n'.format(invoke_function))
    return


def spark_instruction_to_python(feature_param_name, spark_instruction):
    """
        all instructions starts with two spaces, which is compatible with python 2 spaces indentation
        however spark indentation is 1 space for nesting IF, python 2

        example of replacements
        If (feature 0 <= 0.23874) > if (feature[0] <= 0.23874):
        Else (feature 1 > 5.496) > else (feature[1] > 0.23874):
        Predict: 1.0" > return 1.0
    """
    # first, calculate left spacing
    baseline_indentation = 2
    leading_spaces = len(spark_instruction) - len(spark_instruction.lstrip())
    nested_spaces = leading_spaces - baseline_indentation
    final_spaces = baseline_indentation + nested_spaces * 2
    # then make "brute force" replacement
    if spark_instruction.lstrip().startswith("If"):
        # first just swap syntax
        python_line = spark_instruction.replace("If", "if").replace("(", '').replace(")", ":").lstrip()
        # finally extract "feature N" and convert it to a python list syntax
        python_line = re.sub("feature ?(\d+)", '{}[\g<1>]'.format(feature_param_name, '1'), python_line, 1)
    elif spark_instruction.lstrip().startswith("Else"):
        # replicating the condition test in else statement is redundant, so we just replace all the line with ELSE
        python_line = "else:".lstrip()
    elif spark_instruction.lstrip().startswith("Predict"):
        # prediction is the end of the tree navigation - just return whatever leaf we reached
        python_line = spark_instruction.replace("Predict:", "return").lstrip()
    else:
        # should not happen
        raise Exception("Unexpected start of line!")

    return ' ' * final_spaces + python_line


def main():
    convert_spark_to_python(DECISION_TREE_FUNCTION_NAME, DECISION_TREE_INPUT_NAME, MODEL_PATH, OUTPUT_FILE_PATH)
    print "\n==================================\nAll done at {}! See you, space cowboys...".format(datetime.utcnow())
    return


if __name__ == "__main__":
    main()
