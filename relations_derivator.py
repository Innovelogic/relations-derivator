import sklearn
import nltk

from boolean_expression_creator import BooleanExpressionCreator as bEC
from truth_table_creator import TruthTableCreator as tTCreator
from relations_extractor import RelationsExtractorSecond as rES

# Second Phase #

f = open('dummy_input_second.txt')
f = f.read()

sentences = nltk.tokenize.sent_tokenize(f)

# print(sentences[0])

inputs, outputs = rES.sentence_inputs_outputs_cont(sentences[0])

empty_truth_table = tTCreator.truth_table_generator(inputs, outputs)

truth_table = tTCreator.initial_tuple_inputs_insert(inputs, empty_truth_table)

for i in range(len(sentences)):
    inputs_array, outputs_array = rES.relations_extractor(inputs, outputs, sentences[i])
    if i == 0:
        truth_table = tTCreator.header_tuple_adder(inputs, outputs, inputs_array, outputs_array, truth_table)
    truth_table = rES.output_writer(inputs, outputs, inputs_array, outputs_array, truth_table)

print("Truth Table : ", truth_table)

boolean_expression = bEC.boolean_expression_generator(truth_table)
print("Boolean Expression : ", boolean_expression)
