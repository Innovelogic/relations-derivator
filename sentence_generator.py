import nltk
import re
from relations_extractor import RelationsExtractorSecond as rES


class SentenceGenerator:
    """
    Generating sentences from Partially english form sentences
    """
    "ToDo"
    @staticmethod
    def inputs_counter_checker(inputs_count, sentence):
        inputs, outputs = rES.sentence_inputs_outputs_cont(sentence)
        if inputs == inputs_count:
            return True
        else:
            return False

    @staticmethod
    def inputs_outputs_name_extractor(sentences_ff):
        inputs_names = set()
        outputs_names = set()
        for i in sentences_ff:
            current_inputs_names = re.findall("(I[A-Z]=\d)", i, re.IGNORECASE)
            for j in current_inputs_names:
                inputs_names.add(j[1])
            current_inputs_names = re.findall("(O[A-Z]=\d)", i, re.IGNORECASE)
            for k in current_inputs_names:
                outputs_names.add(k[1])
        return list(sorted(inputs_names)), list(sorted(outputs_names, reverse=True))

    @staticmethod
    def nltk_applier(sentence):
        """
        ToDo
        """
        output = nltk.word_tokenize(sentence)
        output = nltk.pos_tag(output)
        return output

    @staticmethod
    def rules_checker(nltk_pos):
        grammar_list = ["RULE 03: {<CD>?<CC>*<DT>}", "RULE 04:{<DT| NNP><NNP+><CC><NNP+>}",
                        "RULE 05: {<IN><JJS><CD>}", "RULE 06: {<CD><CC><JJR>}",
                        "RULE 07: {<DT><NNP><CC><NNP>}", "RULE 08: {<NNP><CC><NNP>}"]

        for grammar in grammar_list:
            if not grammar[5:7].isdecimal():
                print(grammar + " is wrong format")
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(nltk_pos)
            if 2 < result.height():
                return result, result.productions()[1], grammar

        return nltk_pos, nltk_pos.productions()[0], grammar_list


