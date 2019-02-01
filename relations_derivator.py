import sklearn
import nltk

from boolean_expression_creator import BooleanExpressionCreator as bEC
from truth_table_creator import TruthTableCreator as tTCreator
from relations_extractor import RelationsExtractorSecond as rES

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

inputs = 5
outputs = 2

sentence = "IA=1, IC=0, IZ=0, IB=1 and ID=0 then OY=1 and OZ=0."  # "IA=0, IB=0, IC=0 and ID=0 then OZ=1."

rES.relations_extractor(inputs, outputs, sentence)


# print(bEC.boolean_expression_generator(truthtble))

#  truthtble2 = tTCreator.truth_table_generator(inputs, outputs)
#  print(tTCreator.initial_tuple_insert(inputs, truthtble2))
# print(bin(4))
# print()
#
# print(truth_table)

# from nltk.corpus import udhr
# languages = ['Chickasaw', 'English', 'German_Deutsch',
#     'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
# cfd = nltk.ConditionalFreqDist(
#            (lang, len(word))
#         for lang in languages
#         for word in udhr.words(lang + '-Latin1'))
# cfd.plot(cumulative=True)

# f = open('dummy_input_second.txt')
# f = f.read()
# print(f)
# sentences = nltk.tokenize.sent_tokenize(f)
# print(sentences)

# porter = nltk.PorterStemmer()
# lancaster = nltk.LancasterStemmer()
#
# [porter.stem(t) for t in f]
#
# print(f)
# [lancaster.stem(t) for t in f]
#
# print(f)
#
# f = nltk.word_tokenize(f)
# f = nltk.pos_tag(f)
#
# print(f)
# print("This is")
# print(nltk.FreqDist(tag for (word, tag) in f).most_common())
#
