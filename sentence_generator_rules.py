import re
from truth_table_creator import TruthTableCreator as tTC


class SentenceGeneratorRules:
    """
    Rules of the sentence
    """

    @staticmethod
    def rule_01():
        """ToDo"""

    @staticmethod
    def rule_02():
        """ToDo"""

    @staticmethod
    def rule_03(pos_tagged_sentence, result, sub_result, inputs_names, outputs_names, total_inputs_count, total_outputs_count):
        """
        One or both
        """
        inputs_array = []
        inputs = [word for word, pos in list(sub_result) if (pos == 'NNP')]
        inputs.sort(key=lambda x: x[1])
        # output_array.sort(key=lambda x: x[1], reverse=True)
        #  Getting two inputs of the one or both sub tree
        for l in range(len(inputs)):
            temp_input = re.findall("(I[A-Z]=\d)", inputs[l], re.IGNORECASE)  # validate whether NNP is a input
            if 0 < len(temp_input):
                inputs_array = inputs_array + temp_input
        inputs_and_outputs = [word for word, pos in pos_tagged_sentence if (pos == 'NNP')]
        # Getting I/O from pos tagged sentece
        outputs_array = []
        for h in range(len(inputs_and_outputs)):
            temp_output = re.findall("(O[A-Z]=\d)", inputs_and_outputs[h], re.IGNORECASE)
            if 0 < len(temp_output):
                outputs_array = outputs_array + temp_output
        if 0 != len(inputs_and_outputs) - len(inputs_array) - len(outputs_array):
            # Checking whether there is another inputs occure or not
            # if there is another inputs than two it may be an error.
            print("Wrongs on inputs count hint: wrong rule sometimes, two rules on the sentence")
            return False
        truth_table_empty = tTC.truth_table_generator(total_inputs_count, 0)
        truth_table_with_initial_inputs = tTC.initial_tuple_inputs_insert(total_inputs_count, truth_table_empty)
        #  "one or both" only consider two inputs
        input_1_type = inputs_array[0][1]
        input_2_type = inputs_array[1][1]
        input_1_value = inputs_array[0][3]
        input_2_value = inputs_array[1][3]
        input_1_place = -1
        input_2_place = -1
        for j in range(len(inputs_names)):  # Getting place of each input vale from the total inputs name list
            if input_1_type == inputs_names[j]:
                input_1_place = j
            elif input_2_type == inputs_names[j]:
                input_2_place = j
        for j in range(len(truth_table_with_initial_inputs)):
            true_count_of_tuple = 0
            #  count of each input when true for each tuple Ex:- 1 1 0 0 (inputs order is A B C D) and
            #  then condition One or both IA=1 and IB=1 ......
            #  we can check relevant value occurance for relevant two values A and B
            if int(input_1_value) == truth_table_with_initial_inputs[j][input_1_place]:
                true_count_of_tuple = true_count_of_tuple+1
            if int(input_2_value) == truth_table_with_initial_inputs[j][input_2_place]:
                true_count_of_tuple = true_count_of_tuple + 1
                # sentence should be generate.
            if 0 < true_count_of_tuple:
                sentence = ''  # expected output IA=1 and IB=1 then OZ=1
                for x in range(len(inputs_names)):
                    sentence = sentence+"I"+inputs_names[x]+"="+str(truth_table_with_initial_inputs[j][x])
                    if x != len(inputs_names)-1:
                        sentence = sentence+" and "
                    else:
                        sentence = sentence+" "
                sentence = sentence+"then "
                for y in range(len(outputs_array)):
                    "Todo"
                    if y != len(outputs_array)-1:
                        sentence = sentence + outputs_array[y]+" and "
                    else:
                        sentence = sentence + outputs_array[y]+"."
                print(sentence)
        return True

    @staticmethod
    def rule_04():
        """ToDo"""

    @staticmethod
    def rule_05():
        """ToDo"""

    @staticmethod
    def rule_06():
        """ToDo"""

    @staticmethod
    def rule_07():
        """ToDo"""

    @staticmethod
    def rule_08():
        """ToDo"""

    @staticmethod
    def rule_09():
        """ToDo"""

    @staticmethod
    def rule_10():
        """ToDo"""

