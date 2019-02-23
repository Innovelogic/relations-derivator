import nltk
import spacy
import dialogflow
import re
import en_core_web_sm
import textacy
import time

from nltk.corpus import wordnet
from boolean_expression_creator import BooleanExpressionCreator as bEC
from truth_table_creator import TruthTableCreator as tTCreator
from relations_extractor import RelationsExtractorSecond as rES
from sentence_generator import SentenceGenerator as sG
from input_output_state_finder import InputsOutputsStateFinder as iOSF


start_time = time.time()
# ################################################################# io inserter phase #################################
nlp = en_core_web_sm.load()
print(round((time.time()-start_time)*1000), "ms")

io_states = open('dummy_input_for_io_states_identifier.txt')
io_states = io_states.read()

tag_dictionary = {'SensorA': 'IA', 'SensorB': 'IB', 'SensorC': 'IC', 'A1': 'OZ', 'A2': 'OY', 'A3': 'OX', 'air condition': 'OV'}
reference_dictionary = {'sensors': 'SensorA and SensorB and SensorC', 'alarms': 'A1 and A2 and A3'}

# print(len(tag_dictionary))

new_dictionary = iOSF.input_output_state_matrix_creator(nlp, io_states, tag_dictionary, reference_dictionary)
print(new_dictionary)

# io_sentences = nltk.tokenize.sent_tokenize(io_states)
# print(io_sentences)
# pos_tagged_io_sentences = []
# for v in io_sentences:
#     print(sG.nltk_applier(v))
#     iOSF.verb_identifier(sG.nltk_applier(v))
#     pos_tagged_io_sentences = pos_tagged_io_sentences+sG.nltk_applier(v)
# #
# print(tag_dictionary["IA"])
# print(pos_tagged_io_sentences)

######################################################################################################### First Phase #

# total_inputs_count = 3
# total_outputs_count = 1
#
# ff = open('dummy_input_first.txt')
# ff = ff.read()
#
# sentences_ff = nltk.tokenize.sent_tokenize(ff)
# inputs_names, outputs_names = sG.inputs_outputs_name_extractor(sentences_ff)  # Getting Inputs and outputs name
# # Ex:- ["A", "B", "C"] for inputs and ["Z", "Y"] for outputs  # When inputs count less than total inputs count,
# # sentence generator will fill inputs for the inputs which are haven't values.
#
# # print(inputs_names)
# # print(outputs_names)
#
# #  Checks the inputs outputs conts from sentences regex search for every inputs and outputs
# if total_inputs_count > len(inputs_names):
#     print("Inputs names are not completed")
# elif total_inputs_count < len(inputs_names):
#     print("Inputs count is wrong")
#
# if total_outputs_count > len(outputs_names):
#     print("Outputs names are not completed")
# elif total_outputs_count < len(outputs_names):
#     print("Outputs count is wrong")
#
# for i in sentences_ff:
#     value = sG.inputs_counter_checker(total_inputs_count, i)
#     # print(value)
#     if 0 < len(re.findall("^ONLY", i)):
#         "ToDo - ONLY keyword"
#         pos_tagged_sentence = sG.nltk_applier(i)
#         # print(nla_output)
#         result, sub_result, rule = sG.rules_checker(pos_tagged_sentence)
#         if result.height() > 2:
#             # print(result, sub_result, rule)
#             print("RULE number is = ", rule)
#             rule_number = int(rule[5:7])  # getting integer value of the rule string ex:- RULE 05: => 05
#             new_sentences = sG.sentence_generator(i, pos_tagged_sentence, result, sub_result, total_inputs_count,
#                                                   total_outputs_count, inputs_names, outputs_names, rule_number)
#     if value:
#         "Write on the output without any change"
#         "ToDo"
#         print(i)
#     else:
#         "ToDo - can't write"


####################################################################################################### # Second Phase #

# fs = open('dummy_input_second.txt')
# fs = fs.read()
#
#
# sentences_fs = nltk.tokenize.sent_tokenize(fs)
#
# # print(sentences[0])
#
# inputs, outputs = rES.sentence_inputs_outputs_cont(sentences_fs[0])
#
# empty_truth_table = tTCreator.truth_table_generator(inputs, outputs)
#
# truth_table = tTCreator.initial_tuple_inputs_insert(inputs, empty_truth_table)
#
# for i in range(len(sentences_fs)):
#     inputs_array, outputs_array = rES.relations_extractor(inputs, outputs, sentences_fs[i])
#     if i == 0:
#         truth_table = tTCreator.header_tuple_adder(inputs, outputs, inputs_array, outputs_array, truth_table)
#     truth_table = rES.output_writer(inputs, outputs, inputs_array, outputs_array, truth_table)
#
# print("Truth Table : ", truth_table)
#
# boolean_expression = bEC.boolean_expression_generator(truth_table)
# print("Boolean Expression : ", boolean_expression)

print(round((time.time()-start_time)*1000), "ms")
