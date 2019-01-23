import sklearn
from boolean_expression_creator import BooleanExpressionCreator as bEC

truthtble = a = (("IA", "IB", "IC", "ID", "OY", "OZ"),
                 # (0, 0, 0, 0, 1, 1),
                 # (0, 0, 0, 1, 1, 0),
                 # (0, 0, 1, 0, 0, 0),
                 # (0, 0, 1, 1, 1, 0),
                 # (0, 1, 0, 0, 0, 0),
                 (0, 1, 0, 1, 0, 1),
                 (0, 1, 1, 0, 1, 1),
                 (0, 1, 1, 1, 1, 1),
                 # (1, 0, 0, 0, 0, 0),
                 # (1, 0, 0, 1, 1, 0),
                 # (1, 0, 1, 0, 0, 0),
                 (1, 0, 1, 1, 1, 0))

print(bEC.boolean_expression_generator(a))









