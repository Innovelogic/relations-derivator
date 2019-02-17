import nltk
import re
from relations_extractor import RelationsExtractorSecond as rES
from sentence_generator_rules import SentenceGeneratorRules as sGR


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
        grammar_list = ["RULE 03: {<CD><CC><DT><NNP><CC><NNP>}", "RULE 04:{<RB|CC|NNP>+<NNP>+<CC>+<NNP>}",
                        "RULE 05: {<IN>+<JJS>+<CD>}", "RULE 06: {<CD>+<CC>+<JJR>}",
                        "RULE 07: {<DT><NNP><CC><NNP>}", "RULE 08: {<NNP>+<CC>+<NNP>}"]

        # sub_sentence_list = []
        for grammar in grammar_list:
            if not grammar[5:7].isdecimal():
                print(grammar + " is wrong format for rule")
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(nltk_pos)
            if 2 < result.height():
                sub_result = []
                for s in result.subtrees(lambda result: result.height() == 2):
                    sub_result = s[0:]  # convert tree into list
                return result, sub_result, grammar
        return nltk_pos, nltk_pos.productions()[0], grammar_list

    @staticmethod
    def sentence_generator(sentence, pos_tagged_sentence, result, sub_result, total_inputs_count, total_outputs_count, inputs_names, outputs_names, rule_number):
        "todo"
        success_state = False
        if 1 == rule_number:
            "ToDo"
        elif 2 == rule_number:
            "ToDo"
        elif 3 == rule_number:
            "ToDo"
            success_state = sGR.rule_03(pos_tagged_sentence, sub_result, inputs_names, total_inputs_count)
        elif 4 == rule_number:
            "ToDo"
            success_state = sGR.rule_04(pos_tagged_sentence, sub_result, inputs_names, total_inputs_count)
        elif 5 == rule_number:
            "ToDo"
            success_state = sGR.rule_05(sentence, pos_tagged_sentence, sub_result, inputs_names, total_inputs_count)
        elif 6 == rule_number:
            "ToDo"
            success_state = sGR.rule_06(sentence, pos_tagged_sentence, sub_result, inputs_names, total_inputs_count)
        elif 7 == rule_number:
            "ToDo"
            success_state = sGR.rule_07()
        elif 8 == rule_number:
            "ToDo"
            success_state = sGR.rule_08(pos_tagged_sentence, sub_result, inputs_names, total_inputs_count)
        elif 9 == rule_number:
            "ToDo"
        elif 10 == rule_number:
            "ToDo"
        elif 11 == rule_number:
            "ToDo"
        elif 12 == rule_number:
            "ToDo"
            success_state = sGR.rule_01()
        return success_state


