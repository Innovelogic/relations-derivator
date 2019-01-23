import re


class BooleanExpressionCreator:
    """Generating Boolean expression from truth table"""

    @staticmethod
    def input_output_counter(matrix):
        """ToDo"""
        header_tuple = matrix[0]
        count_outputs = 0
        count_inputs = 0
        for x in header_tuple:
            if bool(re.match('I', x, re.IGNORECASE)):
                count_inputs += 1
            else:
                count_outputs += 1

        return count_inputs, count_outputs

    @staticmethod
    def boolean_expression_generator(matrix):
        """ToDo"""
        input_types_count, output_types_count = BooleanExpressionCreator.input_output_counter(matrix)


    def boolean_expression_generator_of_each_tuple(self, matrix):
        """ToDo"""
        return
