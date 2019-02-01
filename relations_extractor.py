import re


class RelationsExtractorFirst:
    """Deriving Relationships between Inputs and Outputs"""

    @staticmethod
    def input_preprocessor(self):
        """ToDo"""


class RelationsExtractorSecond:
    """ This is the second"""

    # @staticmethod
    # def inputs_dictionary():
    #     dict_inputs = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    #                    'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17,
    #                    'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}
    #     return dict_inputs
    #
    # @staticmethod
    # def outputs_dictionary():
    #     dict_outputs = {'Z': 1, 'Y': 2, 'X': 3, 'W': 4, 'V': 5, 'U': 6, 'T': 7, 'S': 8, 'R': 9,
    #                     'Q': 10, 'P': 11, 'O': 12, 'N': 13, 'M': 14, 'L': 15, 'K': 16, 'J': 17,
    #                     'I': 18, 'H': 19, 'G': 20, 'F': 21, 'E': 22, 'D': 23, 'C': 24, 'B': 25, 'A': 26}
    #     return dict_outputs

    @staticmethod
    def sentence_inputs_outputs_cont(sentence):
        inputs_count = len(re.findall("(I[A-Z]=\d)", sentence, re.IGNORECASE))
        outputs_count = len(re.findall("(O[A-Z]=\d)", sentence, re.IGNORECASE))
        return inputs_count, outputs_count

    @staticmethod
    def output_writer(inputs_count, outputs_count, inputs_list, outputs_list, truth_tabel):
        input_binary_value = ""
        # state = True
        for i in range(len(inputs_list)):
            input_binary_value = input_binary_value + inputs_list[i][3]
        for j in range(2**inputs_count):
            current_tuple_input = ""
            temp_tuple = truth_tabel[j+1]
            for k in range(inputs_count):
                current_tuple_input = current_tuple_input + str(temp_tuple[k])
            if input_binary_value == current_tuple_input:
                for l in range(outputs_count):
                    truth_tabel[j+1][inputs_count+l] = int(outputs_list[l][3])
        # if True:
        #     state = True
        # else:
        #     state = False
        return truth_tabel

    @staticmethod
    def relations_extractor(input_count, output_count, sentence):
        input_array = re.findall("(I[A-Z]=\d)", sentence, re.IGNORECASE)  # "(I[A-Z]=\d[,and ])" when IA = 1 (No need)
        output_array = re.findall("(O[A-Z]=\d)", sentence, re.IGNORECASE)  # "(O[A-Z]=\d[,and ])" when OZ = 1 (No need)
        if input_count != len(input_array):
            print("inputs count not match as given count")
        if output_count != len(output_array):
            print("output count not match as given count")
        input_array.sort(key=lambda x: x[1])
        output_array.sort(key=lambda x: x[1], reverse=True)
        return input_array, output_array


