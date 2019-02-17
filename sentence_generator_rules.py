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
    def rule_03(pos_tagged_sentence, sub_result, inputs_names, total_inputs_count):
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
        inputs_and_outputs = [word for word, pos in pos_tagged_sentence if (pos == 'NNP') & (word != "Either") & (word != "Neither")]
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
            #  we can check relevant value occurrence for relevant two values A and B
            if int(input_1_value) == truth_table_with_initial_inputs[j][input_1_place]:
                true_count_of_tuple = true_count_of_tuple+1
            if int(input_2_value) == truth_table_with_initial_inputs[j][input_2_place]:
                true_count_of_tuple = true_count_of_tuple + 1
                # sentence should be generate.
            if 0 < true_count_of_tuple:
                sentence = ''  # expected output IA=1 and IB=1 then OZ=1
                if len(inputs_names) > total_inputs_count:
                    print("Inputs counts not matching. Hint: Anciently puts irrelevant more inputs")
                    return False
                elif len(inputs_names) < total_inputs_count:
                    print("Inputs counts not matching. Hint: Anciently missed input/inputs in all sentences")
                    return False
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
    def rule_04(pos_tagged_sentence, sub_result, inputs_names, total_inputs_count):
        """
        Either or / Neither nor
        :param pos_tagged_sentence:
        :param sub_result:
        :param inputs_names:
        :param total_inputs_count:
        :return:boolean
        """
        success_state = False
        for i in range(len(sub_result)):
            if "either" == str(sub_result[i][0]).lower():
                sub_result_without_either = sub_result[1:]
                # in the rule method Inputs collect by NNP tag, sometimes Either also can be NNP
                # tag therefore it should remove before send it
                success_state = SentenceGeneratorRules.rule_03(pos_tagged_sentence, sub_result_without_either,
                                                               inputs_names, total_inputs_count)
                return success_state
            elif "neither" == str(sub_result[i][0]).lower():
                "Neither"
                sub_result_without_neither = sub_result[1:]
                # in the rule method Inputs collect by NNP tag, sometimes Neither also can be NNP
                # tag therefore it should remove before send it
                inputs_array = []
                inputs = [word for word, pos in list(sub_result_without_neither) if (pos == 'NNP')]
                inputs.sort(key=lambda x: x[1])
                # output_array.sort(key=lambda x: x[1], reverse=True)
                #  Getting two inputs of the one or both sub tree
                for l in range(len(inputs)):
                    temp_input = re.findall("(I[A-Z]=\d)", inputs[l], re.IGNORECASE)  # validate whether NNP is a input
                    if 0 < len(temp_input):
                        inputs_array = inputs_array + temp_input
                inputs_and_outputs = [word for word, pos in pos_tagged_sentence if (pos == 'NNP') & (word != "Either") & (word != "Neither")]
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
                        true_count_of_tuple = true_count_of_tuple + 1
                    if int(input_2_value) == truth_table_with_initial_inputs[j][input_2_place]:
                        true_count_of_tuple = true_count_of_tuple + 1
                        # sentence should be generate.
                    if 0 == true_count_of_tuple:
                        sentence = ''  # expected output IA=1 and IB=1 then OZ=1
                        if len(inputs_names) > total_inputs_count:
                            print("Inputs counts not matching. Hint: Anciently puts irrelevant more inputs")
                            return False
                        elif len(inputs_names) < total_inputs_count:
                            print("Inputs counts not matching. Hint: Anciently missed input/inputs in all sentences")
                            return False
                        for x in range(len(inputs_names)):
                            sentence = sentence + "I" + inputs_names[x] + "=" + str(
                                truth_table_with_initial_inputs[j][x])
                            if x != len(inputs_names) - 1:
                                sentence = sentence + " and "
                            else:
                                sentence = sentence + " "
                        sentence = sentence + "then "
                        for y in range(len(outputs_array)):
                            "Todo"
                            if y != len(outputs_array) - 1:
                                sentence = sentence + outputs_array[y] + " and "
                            else:
                                sentence = sentence + outputs_array[y] + "."
                        print(sentence)
                success_state = True
                return success_state
        return success_state

    @staticmethod
    def rule_05(sentence, pos_tagged_sentence, sub_result, inputs_names, total_inputs_count):
        """
        At (least | most) (one | two | three .....)
        :param sentence:
        :param pos_tagged_sentence:
        :param sub_result:
        :param inputs_names:
        :param total_inputs_count:
        :return: boolean
        """
        sentence_keyword = [word for word, pos in list(sub_result) if (pos == 'JJS')]
        if 1 != len(sentence_keyword):
            print("There is more than one words which are having 'JJS' tag. "
                  "Hint: Both 'most' and lest‘ tags in same sentence or another JJS word like 'biggest ’")
        else:
            count_keyword = [word for word, pos in list(sub_result) if (pos == 'CD')]
            if 1 != len(count_keyword):  # check whether there is only one cd or multiple
                print("There is more than one words having 'CD' tag. "
                      "Hint: there can be more than one word like, 'one', 'two', 'three' ........")
            else:
                str(count_keyword[0]).lower()
                dictionary_cd = {'one': 1,
                                 'two': 2,
                                 'three': 3,
                                 'four': 4,
                                 'five': 5,
                                 'six': 6,
                                 'seven': 7,
                                 'eight': 8,
                                 'nine': 9,
                                 'ten': 10}
                numerical_value_of_cd = dictionary_cd[str(count_keyword[0]).lower()]
                if numerical_value_of_cd >= total_inputs_count:
                    print("Wrong on At least " + count_keyword[0] + " . Hint: It should be less value for " +
                          count_keyword[0])
                else:
                    outputs_array_of_sentence = re.findall("(O[A-Z]=\d)", sentence, re.IGNORECASE)
                    if "least" == str(sentence_keyword[0]).lower():
                        truth_table_empty = tTC.truth_table_generator(total_inputs_count, 0)
                        truth_table_with_initial_inputs = tTC.initial_tuple_inputs_insert(total_inputs_count,
                                                                                          truth_table_empty)
                        for i in range(len(truth_table_with_initial_inputs)):
                            true_count_of_tuple = 0
                            #  count of each input when true for each tuple
                            #  Ex:- 1 1 0 0 (inputs order is A B C D) and
                            #  then condition One or both IA=1 and IB=1 ......
                            #  we can check relevant value occurrence for relevant two values A and B
                            for j in range(len(truth_table_with_initial_inputs[i])):
                                if int(truth_table_with_initial_inputs[i][j]) == 1:
                                    true_count_of_tuple = true_count_of_tuple + 1
                                    # sentence should be generate.
                            if true_count_of_tuple >= numerical_value_of_cd:
                                new_sentence = ''
                                for k in range(len(inputs_names)):
                                    if 1 == len(inputs_names):
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " then "
                                    elif 0 == k:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " , "
                                    elif k == len(inputs_names)-1:
                                        new_sentence = new_sentence + "and I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " then "
                                    else:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " , "
                                for l in range(len(outputs_array_of_sentence)):
                                    if 1 == len(outputs_array_of_sentence):
                                        new_sentence = new_sentence + outputs_array_of_sentence[l]+"."
                                    elif 0 == l:
                                        new_sentence = new_sentence + outputs_array_of_sentence[l]+" , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and " + outputs_array_of_sentence[k] + "."
                                    else:
                                        new_sentence = new_sentence + " , " + outputs_array_of_sentence[k] + " , "
                                print(new_sentence)
                        return True
                    elif "most" == str(sentence_keyword[0]).lower():
                        truth_table_empty = tTC.truth_table_generator(total_inputs_count, 0)
                        truth_table_with_initial_inputs = tTC.initial_tuple_inputs_insert(total_inputs_count,
                                                                                          truth_table_empty)
                        for i in range(len(truth_table_with_initial_inputs)):
                            true_count_of_tuple = 0
                            #  count of each input when true for each tuple
                            #  Ex:- 1 1 0 0 (inputs order is A B C D) and
                            #  then condition One or both IA=1 and IB=1 ......
                            #  we can check relevant value occurrence for relevant two values A and B
                            for j in range(len(truth_table_with_initial_inputs[i])):
                                if int(truth_table_with_initial_inputs[i][j]) == 1:
                                    true_count_of_tuple = true_count_of_tuple + 1
                                    # sentence should be generate.
                            if true_count_of_tuple <= numerical_value_of_cd:
                                new_sentence = ''
                                for k in range(len(inputs_names)):
                                    if 1 == len(inputs_names):
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k])+ " then "
                                    elif 0 == k:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " then "
                                    else:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " , "
                                for l in range(len(outputs_array_of_sentence)):
                                    if 1 == len(outputs_array_of_sentence):
                                        new_sentence = new_sentence + outputs_array_of_sentence[l] + "."
                                    elif 0 == l:
                                        new_sentence = new_sentence + outputs_array_of_sentence[l] + " , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and " + outputs_array_of_sentence[k] + "."
                                    else:
                                        new_sentence = new_sentence + " , " + outputs_array_of_sentence[k] + " , "
                                print(new_sentence)
                        return True
        return False

    @staticmethod
    def rule_06(sentence, pos_tagged_sentence, sub_result, inputs_names, total_inputs_count):
        """
        (one | two | three .......) or (more | less)
        :param sentence:
        :param pos_tagged_sentence:
        :param sub_result:
        :param inputs_names:
        :param total_inputs_count:
        :return:
        """
        sentence_keyword = [word for word, pos in list(sub_result) if (pos == 'JJR')]
        if 1 != len(sentence_keyword):
            print("There is more than one words which are having 'JJR' tag. "
                  "Hint: Both 'more' and less‘ tags in same sentence or another JJR word like 'bigger’")
        else:
            count_keyword = [word for word, pos in list(sub_result) if (pos == 'CD')]
            if 1 != len(count_keyword):  # check whether there is only one cd or multiple
                print("There is more than one words having 'CD' tag. "
                      "Hint: there can be more than one word like, 'one', 'two', 'three' ........")
            else:
                str(count_keyword[0]).lower()
                dictionary_cd = {'one': 1,
                                 'two': 2,
                                 'three': 3,
                                 'four': 4,
                                 'five': 5,
                                 'six': 6,
                                 'seven': 7,
                                 'eight': 8,
                                 'nine': 9,
                                 'ten': 10}
                numerical_value_of_cd = dictionary_cd[str(count_keyword[0]).lower()]
                if numerical_value_of_cd >= total_inputs_count:
                    print("Wrong on " + count_keyword[0] + " or " + sentence_keyword[
                        0] + ". Hint: It should be less value for " + count_keyword[0])
                else:
                    outputs_array_of_sentence = re.findall("(O[A-Z]=\d)", sentence, re.IGNORECASE)
                    if "more" == str(sentence_keyword[0]).lower():
                        truth_table_empty = tTC.truth_table_generator(total_inputs_count, 0)
                        truth_table_with_initial_inputs = tTC.initial_tuple_inputs_insert(total_inputs_count,
                                                                                          truth_table_empty)
                        for i in range(len(truth_table_with_initial_inputs)):
                            true_count_of_tuple = 0
                            #  count of each input when true for each tuple
                            #  Ex:- 1 1 0 0 (inputs order is A B C D) and
                            #  then condition One or both IA=1 and IB=1 ......
                            #  we can check relevant value occurrence for relevant two values A and B
                            for j in range(len(truth_table_with_initial_inputs[i])):
                                if int(truth_table_with_initial_inputs[i][j]) == 1:
                                    true_count_of_tuple = true_count_of_tuple + 1
                                    # sentence should be generate.
                            if true_count_of_tuple >= numerical_value_of_cd:
                                new_sentence = ''
                                for k in range(len(inputs_names)):
                                    if 1 == len(inputs_names):
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " then "
                                    elif 0 == k:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " then "
                                    else:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + str(
                                            truth_table_with_initial_inputs[i][k]) + " , "
                                for l in range(len(outputs_array_of_sentence)):
                                    if 1 == len(outputs_array_of_sentence):
                                        new_sentence = new_sentence + outputs_array_of_sentence[l] + "."
                                    elif 0 == l:
                                        new_sentence = new_sentence + outputs_array_of_sentence[l] + " , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and " + outputs_array_of_sentence[k] + "."
                                    else:
                                        new_sentence = new_sentence + " , " + outputs_array_of_sentence[k] + " , "
                                print(new_sentence)
                        return True
                    elif "less" == str(sentence_keyword[0]).lower():
                        truth_table_empty = tTC.truth_table_generator(total_inputs_count, 0)
                        truth_table_with_initial_inputs = tTC.initial_tuple_inputs_insert(total_inputs_count,
                                                                                          truth_table_empty)
                        for i in range(len(truth_table_with_initial_inputs)):
                            true_count_of_tuple = 0
                            #  count of each input when true for each tuple
                            #  Ex:- 1 1 0 0 (inputs order is A B C D) and
                            #  then condition One or both IA=1 and IB=1 ......
                            #  we can check relevant value occurrence for relevant two values A and B
                            for j in range(len(truth_table_with_initial_inputs[i])):
                                if int(truth_table_with_initial_inputs[i][j]) == 1:
                                    true_count_of_tuple = true_count_of_tuple + 1
                                    # sentence should be generate.
                            if true_count_of_tuple <= numerical_value_of_cd:
                                new_sentence = ''
                                for k in range(len(inputs_names)):
                                    if 1 == len(inputs_names):
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " then "
                                    elif 0 == k:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " then "
                                    else:
                                        new_sentence = new_sentence + "I" + inputs_names[k] + "=" + \
                                                       str(truth_table_with_initial_inputs[i][k]) + " , "
                                for l in range(len(outputs_array_of_sentence)):
                                    if 1 == len(outputs_array_of_sentence):
                                        new_sentence = new_sentence + outputs_array_of_sentence[l] + "."
                                    elif 0 == l:
                                        new_sentence = new_sentence + outputs_array_of_sentence[l] + " , "
                                    elif k == len(inputs_names) - 1:
                                        new_sentence = new_sentence + "and " + outputs_array_of_sentence[k] + "."
                                    else:
                                        new_sentence = new_sentence + " , " + outputs_array_of_sentence[k] + " , "
                                print(new_sentence)
                        return True
        return False

    @staticmethod
    def rule_07():
        """ToDo"""

    @staticmethod
    def rule_08(pos_tagged_sentence, sub_result, inputs_names, total_inputs_count):
        """ToDo"""
        # print(sub_result)
        # print("hi")
        # print(pos_tagged_sentence)

    @staticmethod
    def rule_09():
        """ToDo"""

    @staticmethod
    def rule_10():
        """ToDo"""

