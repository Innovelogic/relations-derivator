import sklearn
from boolean_expression_creator import BooleanExpressionCreator as bEC

truthtble = a = (("IA", "IB", "IC", "OD", "OZ"),
                 (0, 0, 0, 0, 1),
                 (0, 0, 0, 0, 1),
                 (0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 1),
                 (0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 1),
                 (0, 0, 0, 0, 1),
                 (0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 1),
                 (0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 1))
print(a[2])
print(len(a))

print(bEC.boolean_expression_generator(a))









