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

io_states = "Sensors indicate cold = 1. Heaters are activated = 1."

tag_dictionary = {'IA': 'T4', 'IB': 'T1', 'IC': 'T3', 'ID': 'T2', 'OZ': 'H2', 'OY': 'H3'}
reference_dictionary = {'heaters': 'H1 and H2 and H3', 'sensors': 'T1 and T2 and T3 and T4'}

# print(len(tag_dictionary))

i_o_status_matrix = iOSF.input_output_state_matrix_creator(nlp, io_states, tag_dictionary, reference_dictionary)
print("I O Status Matrix : ", i_o_status_matrix)


logic_sentences = "When at least two IB=1/0 and ID=1/0 and IC=1/0 and IA=1/0 are indicated cold, then OZ=1/0 and OY=1/0 are activated. If neither IB=1/0 and ID=1/0 and IC=1/0 and IA=1/0 are indicated cold, then OZ=1/0 is activated. If ID=1/0 is indicated cold, then OY=1/0 is inactivated."

noun_verb_mapper_set = [[[' IB=1/0 and ID=1/0 and IC=1/0 and IA=1/0 are indicated'], [' OZ=1/0 and OY=1/0 are activated']], [[' IB=1/0 and ID=1/0 and IC=1/0 and IA=1/0 are indicated'], [' OZ=1/0 is activated']], [[' ID=1/0 is indicated'], [' OY=1/0 is inactivated']]]

inputs = 4
outputs = 2

input_output_status_added_sentences = \
    iOSF.one_or_zero_applier_for_logic_sentence(nlp, logic_sentences, i_o_status_matrix, noun_verb_mapper_set)
print(input_output_status_added_sentences)


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
