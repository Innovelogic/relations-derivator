import re


class BooleanExpressionCreator:
    """Generating Boolean expression from truth table"""

    @staticmethod
    def input_output_counter(matrix):
        """ToDo"""
        header_tuple = matrix[0]  # getting input and output name tuple for naming
        count_outputs = 0
        count_inputs = 0
        for x in header_tuple:
            if bool(re.match('I', x, re.IGNORECASE)):
                # inputs are start with "I" and outputs "O"
                # as example inputs IA, IB .... outputs OZ, OY ......,
                # So in this regex check whether it starts with I or not
                count_inputs += 1
            else:
                count_outputs += 1

        return count_inputs, count_outputs, header_tuple

    @staticmethod
    def boolean_expression_generator(matrix):
        """ToDo"""
        inputs_count, outputs_count, tuple_head = BooleanExpressionCreator.input_output_counter(matrix)
        boolean_expression_set = ""
        value_matrix = matrix[1:]
        #  remove header tuple and create new matrix with values
        for i in range(outputs_count):
            #  generating boolean expression for each output separately
            boolean_expression = ""
            for x in range(len(value_matrix)):  # generating boolean expression for each tuple of truth table
                current_tuple = value_matrix[x]
                if 1 == current_tuple[inputs_count + i]:  # only genera boolean expression for outputs when "1"
                    temp_boolean_expresion = BooleanExpressionCreator.bool_expression_of_each_tuple_each_output(
                        inputs_count, current_tuple, tuple_head)
                    if 0 == len(boolean_expression):        # concatenate each boolean expression
                        boolean_expression = boolean_expression + temp_boolean_expresion
                    else:
                        boolean_expression = boolean_expression + " + " + temp_boolean_expresion
                # if 0 < len(temp_boolean_expresion):
            if 0 < len(boolean_expression):
                boolean_expression_set = boolean_expression_set + tuple_head[inputs_count+i][1:] + ' = '\
                                     + boolean_expression + "  "
            # concatenate boolean expression of every outputs'
        return boolean_expression_set

    @staticmethod
    def bool_expression_of_each_tuple_each_output(input_count, tuple_current, tuple_head):
        """ToDo"""
        boolean_expression = ""
        # if 1 == tuple_current[input_count + output_place - 1]:
        for j in range(input_count):
            if 1 == tuple_current[j]:   # check whether input is "1" or not.
                # If it is Getting Input from tuple head value
                boolean_expression = boolean_expression + tuple_head[j][1:]
            else:
                boolean_expression = boolean_expression + tuple_head[j][1:] + "\'"
        return boolean_expression
