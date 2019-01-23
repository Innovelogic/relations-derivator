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

        return count_inputs, count_outputs, header_tuple

    @staticmethod
    def boolean_expression_generator(matrix):
        """ToDo"""
        inputs_count, outputs_count, tuple_head = BooleanExpressionCreator.input_output_counter(matrix)
        boolean_expression_array = ""
        value_matrix = matrix[1:]
        for i in range(outputs_count):
            boolean_expression = ""
            for x in range(len(value_matrix)):
                current_tuple = value_matrix[x]
                if 1 == current_tuple[inputs_count + i]:
                    temp_boolean_expresion = BooleanExpressionCreator.bool_expression_of_each_tuple_each_output(inputs_count, outputs_count, inputs_count + i, current_tuple, tuple_head)
                    if 0 == len(boolean_expression):
                        boolean_expression = boolean_expression + temp_boolean_expresion
                    else:
                        boolean_expression = boolean_expression + " + " + temp_boolean_expresion
                # if 0 < len(temp_boolean_expresion):
            if 0 < len(boolean_expression_array):
                boolean_expression_array+tuple_head[i][1:]+'='+boolean_expression+"  "
            print("this is final expression " + boolean_expression)
        print("this is final final expression" + boolean_expression_array)
        return boolean_expression_array

    @staticmethod
    def bool_expression_of_each_tuple_each_output(input_count, output_count, output_place, tuple_current, tuple_head):
        """ToDo"""
        boolean_expression = ""
        # if 1 == tuple_current[input_count + output_place - 1]:
        for j in range(input_count):
            # print(tuple_current[j])
            if 1 == tuple_current[j]:
                boolean_expression = boolean_expression + tuple_head[j][1:]
            else:
                boolean_expression = boolean_expression + tuple_head[j][1:] + "\'"
        # boolean_expression + "+"
        print("this is temporal expression", boolean_expression)
        return boolean_expression
