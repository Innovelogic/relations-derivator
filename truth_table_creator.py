class TruthTableCreator:
    """It has all method of Truth table creator and other functionality such as filling 0 outputs"""

    @staticmethod
    def truth_table_generator(input_count, output_count):
        truth_table = [[0 for x in range(input_count + output_count)] for y in range(2 ** input_count)]
        #  Creating truth table for given inputs ex:- 3 inputs, 2**3 = 8 then 8*3 matrix for inputs
        return truth_table

    @staticmethod
    def initial_tuple_inputs_insert(input_count, truth_table):
        """This method will insert tuple initial inputs each by each as relevant"""
        for i in range(2**input_count):
            boolean_value = bin(i)
            #  getting boolean value of each input combinations
            boolean_value = boolean_value[2:]  # getting only boolean value from String format of boolean
            # representation of the Integer (as String)
            for j in range(len(boolean_value)):
                #  insert each binary point for relevant places on truth table
                truth_table[i][input_count-1-j] = int(boolean_value[len(boolean_value)-1-j])
        # truth_table = [['IA', 'IB', 'IC', 'ID', 'OZ']] + truth_table  # this is not dynamic
        """ToDo"""
        #  truth_table = tuple(truth_table)
        return truth_table

    @staticmethod
    def header_tuple_adder(inputs_count, outputs_count, inputs_array, outputs_array, truth_table):
        """
        input and outputs arrays must be sorted arrays
        """
        header_tuple = [" " for i in range(inputs_count+outputs_count)]
        for i in range(inputs_count):
            header_tuple[i] = inputs_array[i][:2]
        for j in range(outputs_count):
            header_tuple[inputs_count+j] = outputs_array[j][:2]
        truth_table = [header_tuple] + truth_table
        return truth_table

    @staticmethod
    def tuple_finder():
        """ToDo"""

    def zero_value_filler(self):
        """Automatically at array creation"""
