class TruthTableCreator:
    """It has all method of Truth table creator and other functionality such as filling 0 outputs"""

    @staticmethod
    def truth_table_generator(input_count, output_count):
        truth_table = [[0 for x in range(input_count + output_count)] for y in range(2 ** input_count)]
        #  Creating truth table for given inputs ex:- 3 inputs, 2**3 = 8 then 8*3 matrix for inputs
        return truth_table

    @staticmethod
    def initial_tuple_insert(input_count, truth_table):
        """This method will insert tuple initial inputs each by each as relevant"""
        for i in range(2**input_count):
            boolean_value = bin(i)
            #  getting boolean value of each input combinations
            boolean_value = boolean_value[2:]  # getting only boolean value (as String)
            for j in range(len(boolean_value)):
                #  insert each binary point for relevant places on truth table
                truth_table[i][input_count-1-j] = int(boolean_value[len(boolean_value)-1-j])
        truth_table = [['IA', 'IB', 'IC', 'ID', 'OZ']] + truth_table
        #  truth_table = tuple(truth_table)
        return truth_table

    @staticmethod
    def tuple_finder():
        """ToDo"""

    def zero_value_filler(self):
        """Automatically at array creation"""
