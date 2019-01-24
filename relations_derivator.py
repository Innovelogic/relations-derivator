import sklearn
from boolean_expression_creator import BooleanExpressionCreator as bEC
from truth_table_creator import TruthTableCreator as tTCreator

truthtble = a = (("IA", "IB", "IC", "ID", "OZ", "OY"),
                 (0, 0, 0, 0, 1, 1),
                 (0, 0, 0, 1, 1, 0),
                 (0, 0, 1, 0, 0, 0),
                 (0, 0, 1, 1, 1, 0),
                 (0, 1, 0, 0, 0, 0),
                 (0, 1, 0, 1, 0, 1),
                 (0, 1, 1, 0, 1, 1),
                 (0, 1, 1, 1, 1, 1),
                 (1, 0, 0, 0, 0, 0),
                 (1, 0, 0, 1, 1, 0),
                 (1, 0, 1, 0, 0, 0),
                 (1, 0, 1, 1, 1, 0))

#  print(bEC.boolean_expression_generator(a))

inputs = 4
outputs = 1

print(bEC.boolean_expression_generator(truthtble))


truthtble2 = tTCreator.truth_table_generator(inputs, outputs)
print(tTCreator.initial_tuple_insert(inputs, truthtble2))
# print(bin(4))
# print()
#
# print(truth_table)

