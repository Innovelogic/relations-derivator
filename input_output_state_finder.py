import nltk
import textacy
from nltk.corpus import wordnet
import re
from nltk.stem import WordNetLemmatizer

from nltk import word_tokenize,pos_tag,sent_tokenize,RegexpParser


class InputsOutputsStateFinder:
    """
    Input Output Status Finding and deriving from the Wordnet corpus from the nltk, spaCy tools
    """

    @staticmethod
    def one_zero_finder(nlp, sentence):
        """
        getting 1 or 0 state of each sentence
        :param nlp:
        :param sentence:
        :return: io_state: Str
        """
        doc_sentence = nlp(sentence)
        io_states_current = ''
        for token in doc_sentence:
            if (token.tag_ == "CD" and token.text == "1") or (
                    (token.tag_ == "NFP" or token.tag_ == "CD") and token.text == "0"):
                io_states_current = token.text
        return io_states_current

    # @staticmethod
    # def not_value_finder(nlp, verb_of_sentence):
    #     """
    #     getting not availability state of each sentence
    #     :param nlp:
    #     :param verb_of_sentence:
    #     :return:
    #     """
    #     doc_verb = nlp(verb_of_sentence)
    #     not_availability = False
    #     for token in doc_verb:
    #         if token.text == "not" and token.tag_ == "RB" and token.pos_ == "ADV":
    #             not_availability = True
    #     return not_availability

    @staticmethod
    def phrasal_verb_finder(nlp, complex_verb):
        """
        pharasal verbs finder from the verb phrases (Verifing from the Wordnet)
        :param nlp:
        :param complex_verb:
        :return:
        """
        phrasal_verb = []
        doc_complex_verb = nlp(complex_verb)
        pattern_for_phrasal_verb = r'<VERB><PART>'
        doc_complex_verb = textacy.Doc(doc_complex_verb, lang='en_core_web_sm')
        list_of_phrasal_verb = textacy.extract.pos_regex_matches(doc_complex_verb, pattern_for_phrasal_verb)
        phrasal_verb_temp = []
        for element_of_phrasal_verb in list_of_phrasal_verb:
            phrasal_verb_temp = phrasal_verb_temp + [element_of_phrasal_verb.text]
        for single_phrasal_verb in range(len(phrasal_verb_temp)):
            str_of_phrasal_verb = str(phrasal_verb_temp[single_phrasal_verb])
            sub_verb_list_of_phrasal_verb = str_of_phrasal_verb.split(" ")
            sub_verb_before_lemmatize = str(sub_verb_list_of_phrasal_verb[0])
            sub_verb_aftr_lemmatize = WordNetLemmatizer().lemmatize(sub_verb_before_lemmatize, 'v')
            phrasal_verb_lemmatized = sub_verb_aftr_lemmatize+"_"+sub_verb_list_of_phrasal_verb[1]
            for syn in wordnet.synsets(phrasal_verb_lemmatized, pos=wordnet.VERB):
                if 0 < len(syn.lemmas()):
                    phrasal_verb = phrasal_verb + [phrasal_verb_lemmatized]
                    break
        return phrasal_verb

    @staticmethod
    def non_phrasal_verb_finder(nlp, complex_verb, stop_word_applier):
        """
        Non phrasal verbs (normal verbs) finding from the verb phrases (Verifing from the Wordnet)
        :param nlp:
        :param complex_verb:
        :return:
        """
        non_phrasal_verb = []
        doc_complex_verb = nlp(complex_verb)
        if stop_word_applier:
            doc_not_stop_word = (' '.join([str(t) for t in doc_complex_verb if not t.is_stop]))
        else:
            doc_not_stop_word = doc_complex_verb

        pattern_for_non_phrasal_verb = r'<VERB>'
        doc_complex_verb = textacy.Doc(doc_not_stop_word, lang='en_core_web_sm')
        list_of_non_phrasal_verb = textacy.extract.pos_regex_matches(doc_complex_verb, pattern_for_non_phrasal_verb)
        non_phrasal_verb_temp = []
        for element_of_non_phrasal_verb in list_of_non_phrasal_verb:
            non_phrasal_verb_temp = non_phrasal_verb_temp + [element_of_non_phrasal_verb.text]
        for single_non_phrasal_verb in range(len(non_phrasal_verb_temp)):
            for syn in wordnet.synsets(
                    WordNetLemmatizer().lemmatize(str(non_phrasal_verb_temp[single_non_phrasal_verb]), 'v'),
                    pos=wordnet.VERB):
                if 0 < len(syn.lemmas()):
                    non_phrasal_verb = non_phrasal_verb + [
                        WordNetLemmatizer().lemmatize(str(non_phrasal_verb_temp[single_non_phrasal_verb]), 'v')]
                    break
        return non_phrasal_verb

    @staticmethod
    def complex_verb_finder(nlp, sentence):
        """ToDo"""
        all_complex_verb_list = []
        # this list will catch all verb element of sentence, the phrasal verb or verb or any other VERB format etc.
        doc_sentence = nlp(sentence)
        pattern = r'<VERB>*<ADV>*<PART>*<VERB>+<PART>*'  # <VB.*>*<RB>*<RP>*<VB.*>+<PP>*
        doc_each_sentence = textacy.Doc(doc_sentence, lang='en_core_web_sm')
        lists_verbs = textacy.extract.pos_regex_matches(doc_each_sentence, pattern)
        for complex_verb in lists_verbs:
            all_complex_verb_list = all_complex_verb_list + [complex_verb.text]
        return all_complex_verb_list

    @staticmethod
    def verb_and_not_word_availability_finder(nlp, sentence):
        """
        Getting verbs and not state availability of the sentences
        :param nlp:
        :param sentence:
        :return:
        """
        verb = []
        stop_word_applier = True
        not_availability = True
        sentence_all_complex_verbs = InputsOutputsStateFinder.complex_verb_finder(nlp, sentence)
        for tem_verb in range(len(sentence_all_complex_verbs)):
            not_availability = InputsOutputsStateFinder.not_value_finder(nlp, sentence_all_complex_verbs[tem_verb])
            phrasal_verb = InputsOutputsStateFinder.phrasal_verb_finder(nlp, sentence_all_complex_verbs[tem_verb])

            if 1 < len(phrasal_verb):
                print("There is more than one phrasal verb here in the sentence : ", sentence)
                verb = []  # in the inputs output statement applier method will check verb length.
                # So, remove verbs because of ignore previous verbs
                return verb, not_availability
            elif 1 == len(phrasal_verb):
                verb = verb + [phrasal_verb]
            else:
                non_phrasal_verb = InputsOutputsStateFinder.non_phrasal_verb_finder(nlp, sentence_all_complex_verbs[
                    tem_verb], stop_word_applier)
                if 1 < len(non_phrasal_verb):
                    print("There is more than one non phrasal verb here in the sentence : ", sentence)
                    verb = []  # in the inputs output statement applier method will check verb length.
                # So, remove verbs because of ignore previous verbs
                    return verb, not_availability
                elif 1 == len(non_phrasal_verb):
                    verb = verb + [non_phrasal_verb]
        return verb, not_availability

#  ##############################################################################################################
    @staticmethod
    def not_value_finder(negation_word):
        """
        :param negation_word:
        :return:
        """
        """ToDo : if not have space on the begin it should remove"""
        if negation_word.lower() == "not":
            return True
        elif negation_word == "":
            return False
        else:
            assert True, "In the I/O statements have wrong type negation"

    @staticmethod
    def phrasal_verb_verifier_or_verb_part_extractor(nlp, verb):
        verified_verb_lemma = []

        splited_verb = str(verb.strip()).split(" ")
        if 2 == len(splited_verb):  # must be a phrasal verb
            lemma_of_first_verb = WordNetLemmatizer().lemmatize(splited_verb[0], 'v')
            lemma_phrasal_verb = lemma_of_first_verb + "_" + splited_verb[1]
            for syn in wordnet.synsets(lemma_phrasal_verb, pos=wordnet.VERB):
                if 0 < len(syn.lemmas()):
                    return verb
            return splited_verb[0]
        elif 2 < len(splited_verb):
            print(" Wrong format of the verb part : ", verb, ". This is the verb after splited by space : ",
                  splited_verb)
            assert True, "Please change it on given scenario and re run the process"
        elif 1 == len(splited_verb):
            return splited_verb[0]
        else:
            print(" There is no verb in ", verb, "Hint: Accidentally send a " " or likewise string as verb.")
            assert True, "Please change it on given scenario and re run the process"

    @staticmethod
    def identify_io_verbs(nlp, sentences):
        """
        :param nlp:
        :param sentences:
        :return:
        """
        sentences = sent_tokenize(sentences)
        grammar = r"""
                  GR : {<RB>*<VB|VBN|JJ|VBG|VBZ|VBP|VBD>+<IN|RP>*} 
                  """
        # GR : {<RB>*<VB|VBN|JJ|VBG|VBZ|VBP>+<IN|RP>*}
        io_sent_verbs = []
        for sent in sentences:
            sample = sent.split('=')
            if 2 != len(sample):
                print("Wrong I/O format in the io sentence : ", sent)
                return
            sent_verified = sample[0]

            words = word_tokenize(sent_verified)
            tagged = pos_tag(words)
            cp = RegexpParser(grammar)
            t = cp.parse(tagged)
            # t.draw()
            negate = ''
            verb = ''
            verbs = []
            for s in t.subtrees():
                is_phrasal = False
                if s.label() == "GR":
                    for token in s.leaves():
                        if token[0] == 'is' or token[0] == 'are' or token[0] == 'does' or token[0] == 'do':
                            continue
                        elif token[1] == 'RB':
                            negate = token[0]
                        elif token[0] != "=":
                            verb = verb + " " + token[0]

            verb = InputsOutputsStateFinder.phrasal_verb_verifier_or_verb_part_extractor(nlp, verb)
            verbs.append([negate, verb])
            io_sent_verbs.append(verbs)
        return io_sent_verbs

    @staticmethod
    def matrix_writer(io_details_list, written_number_of_table, nn, nnp, tag_key, io_value, verb, negation):
        io_details_list[written_number_of_table][0] = nn
        io_details_list[written_number_of_table][1] = nnp
        io_details_list[written_number_of_table][2] = tag_key
        io_details_list[written_number_of_table][3] = io_value
        io_details_list[written_number_of_table][4] = verb
        io_details_list[written_number_of_table][5] = negation
        return io_details_list

    @staticmethod
    def initial_lists_and_dictionaries_of_io_state_matrix_creator(nlp, tag_dictionary, reference_dictionary):
        tag_key_not_completed = []
        tag_value_not_completed = []
        tag_dictionary_key_list = []
        value_dictionary_of_tag_dictionary = {}
        for k, v in tag_dictionary.items():
            tag_dictionary_key_list = tag_dictionary_key_list + [str(k).lower()]
            value_dictionary_of_tag_dictionary[str(v).lower()] = k
            tag_key_not_completed.append(str(k).lower())
            tag_value_not_completed.append(str(v).lower())

        reference_dictionary_key_list = []
        for k, v in reference_dictionary.items():
            reference_dictionary_key_list = reference_dictionary_key_list + [str(k).lower()]

        list_of_all = []
        list_of_all = list_of_all + [tag_key_not_completed]
        list_of_all = list_of_all + [tag_value_not_completed]
        list_of_all = list_of_all + [tag_dictionary_key_list]
        list_of_all = list_of_all + [reference_dictionary_key_list]
        return list_of_all, value_dictionary_of_tag_dictionary

    @staticmethod
    def input_output_state_matrix_creator(nlp, io_states_sentences, tag_dictionary, reference_dictionary):
        """
        Creates Inputs Outputs matrix from Input Output states.
        :param nlp:
        :param io_states_sentences:
        :param tag_dictionary:
        :param reference_dictionary:
        :return:
        """
        io_details_list = [["" for x in range(6)] for y in range(len(tag_dictionary))]
        # example tuple [[NN], [NNP], [tag_key], [I/O_State], [Verb], [not on the verb]]

        list_of_initial_lists, value_dictionary_of_tag_dictionary = \
            InputsOutputsStateFinder.initial_lists_and_dictionaries_of_io_state_matrix_creator(nlp, tag_dictionary,
                                                                                               reference_dictionary)

        tag_key_not_completed = list_of_initial_lists[0]
        tag_value_not_completed = list_of_initial_lists[1]
        tag_dictionary_key_list = list_of_initial_lists[2]
        reference_dictionary_key_list = list_of_initial_lists[3]

        written_number_of_table = 0

        io_sentences = nltk.tokenize.sent_tokenize(io_states_sentences)

        tag_key_completed = []

        for checking_sentence in range(len(io_sentences)):
            if str(io_sentences[checking_sentence][0]).islower():
                print(io_sentences[checking_sentence][0], "letter must be capital in the sentence : ",
                      io_sentences[checking_sentence], " of the I/O_Status.")
                assert True, "Correct the previous error on the scenario and run. "

        for i in range(len(io_sentences)):
            # print()
            doc_sentence = nlp(io_sentences[i])
            # getting I/O state value for relevant sentence. ex :- value is 1
            io_states_current = InputsOutputsStateFinder.one_zero_finder(nlp, io_sentences[i])

            # getting verb statement. limitations on the phrasal verbs. # "Not" included. "ToDo"
            # should implement not finder within this step
            verb_and_not_list = InputsOutputsStateFinder.identify_io_verbs(nlp, io_sentences[i])

            not_availability = InputsOutputsStateFinder.not_value_finder(verb_and_not_list[0][0][0])

            verb = [verb_and_not_list[0][0][1]]
            if 1 < len(verb):
                print("There are more than one sentences in the sentence or sentences not in the "
                      "right format in the sentence : ", io_sentences[i],
                      " Hint 1: Sensor works sounds Hint 2: Sometimes sentence starts with lower "
                      "case letter Hint 3: ................ please change it", verb)
                assert True, "Please correct the above limitation"
            elif 0 == len(verb):
                print("There is no verb in the sentence :", io_sentences[i])
                assert True, "Please correct the above limitation"

            if written_number_of_table > len(tag_dictionary) - 1:
                print("There is more sentence in the I/O_Status")
                assert True, "Please correct the above limitation"
            if 0 != len(reference_dictionary):
                if 0 == len(reference_dictionary_key_list):
                    if 0 == len(tag_key_completed):
                        for tag in range(len(tag_dictionary_key_list)):

                            temp_entity = \
                                re.findall(tag_dictionary[str(tag_dictionary_key_list[tag]).upper()], io_sentences[i],
                                           re.IGNORECASE)

                            if 0 != len(temp_entity):

                                io_details_list = \
                                    InputsOutputsStateFinder.matrix_writer(io_details_list,
                                                                           written_number_of_table,
                                                                           "NO_REFERENCE",
                                                                           tag_dictionary[
                                                                               tag_dictionary_key_list[tag].upper()],
                                                                           tag_dictionary_key_list[tag].upper(),
                                                                           io_states_current, verb[0],
                                                                           str(not_availability))

                                tag_key_completed = tag_key_completed + [tag_dictionary_key_list[tag]]

                                tag_value_not_completed.remove(
                                    str(tag_dictionary[str(tag_dictionary_key_list[tag]).upper()]).lower())
                                written_number_of_table = written_number_of_table + 1
                    else:
                        for competed_tag in range(len(tag_key_completed)):
                            if not tag_key_completed[competed_tag] in str(io_sentences[i]).lower():
                                for tag in range(len(tag_dictionary_key_list)):
                                    if tag_dictionary_key_list[tag] in str(io_sentences[i]).lower():

                                        io_details_list = \
                                            InputsOutputsStateFinder.matrix_writer(io_details_list,
                                                                                   written_number_of_table,
                                                                                   "NO_REFERENCE",
                                                                                   tag_dictionary[
                                                                                       tag_dictionary_key_list[
                                                                                           tag].upper()],
                                                                                   tag_dictionary_key_list[
                                                                                       tag].upper(),
                                                                                   io_states_current, verb[0],
                                                                                   str(not_availability))

                                        tag_key_completed = tag_key_completed + [tag_dictionary_key_list[tag]]
                                        tag_value_not_completed.remove(tag_dictionary_key_list[tag])
                                        written_number_of_table = written_number_of_table + 1
                else:
                    for ref in range(len(reference_dictionary_key_list)):
                        if reference_dictionary_key_list[ref] in str(
                                io_sentences[i]).lower():  # if entity on the reference dictionary
                            split_tag_key_temp = str(reference_dictionary[reference_dictionary_key_list[ref]]).split(
                                ' and ')
                            for n in range(len(split_tag_key_temp)):
                                if split_tag_key_temp[n].lower() in tag_value_not_completed:

                                    io_details_list = \
                                        InputsOutputsStateFinder.matrix_writer(io_details_list,
                                                                               written_number_of_table,
                                                                               reference_dictionary_key_list[ref],
                                                                               split_tag_key_temp[n],
                                                                               value_dictionary_of_tag_dictionary[
                                                                                   split_tag_key_temp[n].lower()],
                                                                               io_states_current, verb[0],
                                                                               str(not_availability))

                                    tag_key_completed = tag_key_completed + [split_tag_key_temp[n]]

                                    tag_value_not_completed.remove(split_tag_key_temp[n].lower())
                                    written_number_of_table = written_number_of_table + 1
                        else:
                            if 0 == len(tag_key_completed):
                                for tag in range(len(tag_dictionary_key_list)):
                                    if tag_dictionary_key_list[tag] in str(io_sentences[i]).lower():

                                        io_details_list = \
                                            InputsOutputsStateFinder.matrix_writer(io_details_list,
                                                                                   written_number_of_table,
                                                                                   "NO_REFERENCE",
                                                                                   tag_dictionary[
                                                                                       tag_dictionary_key_list[
                                                                                           tag].upper()],
                                                                                   tag_dictionary_key_list[
                                                                                       tag].upper(),
                                                                                   io_states_current, verb[0],
                                                                                   str(not_availability))

                                        tag_key_completed = tag_key_completed + [tag_dictionary_key_list[tag]]

                                        tag_value_not_completed.remove(
                                            str(tag_dictionary[tag_dictionary_key_list[tag].upper()]).lower())
                                        written_number_of_table = written_number_of_table + 1
                            else:
                                for competed_tag in range(len(tag_key_completed)):
                                    if not tag_key_completed[competed_tag] in str(io_sentences[i]).lower():
                                        for tag in range(len(tag_dictionary_key_list)):

                                            if str(tag_dictionary[tag_dictionary_key_list[tag].upper()]).lower() \
                                                    in tag_value_not_completed:

                                                if tag_dictionary_key_list[tag] in str(io_sentences[i]).lower():

                                                    io_details_list = \
                                                        InputsOutputsStateFinder.matrix_writer(
                                                            io_details_list, written_number_of_table,
                                                            "NO_REFERENCE",
                                                            tag_dictionary[tag_dictionary_key_list[tag].upper()],
                                                            tag_dictionary_key_list[tag].upper(),
                                                            io_states_current, verb[0],
                                                            str(not_availability))

                                                    tag_key_completed = tag_key_completed + \
                                                                        [tag_dictionary_key_list[tag]]

                                                    tag_value_not_completed.remove(tag_dictionary_key_list[tag].upper())
                                                    written_number_of_table = written_number_of_table + 1

                if 0 < len(tag_value_not_completed):
                    tag_value_not_completed_will_be_remove = []
                    for value in range(len(tag_value_not_completed)):

                        if tag_value_not_completed[value] in str(io_sentences[i]).lower():
                            io_details_list = \
                                InputsOutputsStateFinder.matrix_writer(io_details_list,
                                                                       written_number_of_table,
                                                                       "NO_REFERENCE",
                                                                       tag_dictionary[str(tag_dictionary_key_list[
                                                                                              tag]).upper()],
                                                                       str(tag_dictionary_key_list[
                                                                               tag]).upper(),
                                                                       io_states_current, verb[0],
                                                                       str(not_availability))

                            tag_key_completed = tag_key_completed + [tag_dictionary_key_list[tag]]

                            tag_value_not_completed_will_be_remove.append(
                                str(tag_dictionary[str(tag_dictionary_key_list[tag]).upper()]).lower())

                            written_number_of_table = written_number_of_table + 1
                    if 0 < len(tag_value_not_completed_will_be_remove):
                        for l in range(len(tag_value_not_completed_will_be_remove)):
                            tag_value_not_completed.remove(tag_value_not_completed_will_be_remove[l])
            else:
                if 0 < len(tag_value_not_completed):
                    tag_value_not_completed_will_be_remove = []
                    for value in range(len(tag_value_not_completed)):

                        if tag_value_not_completed[value] in str(io_sentences[i]).lower():
                            io_details_list = \
                                InputsOutputsStateFinder.matrix_writer(io_details_list,
                                                                       written_number_of_table,
                                                                       "NO_REFERENCE",
                                                                       tag_dictionary[
                                                                           value_dictionary_of_tag_dictionary[
                                                                               tag_value_not_completed[value]]],
                                                                       value_dictionary_of_tag_dictionary[
                                                                           tag_value_not_completed[value]],
                                                                       io_states_current, verb[0],
                                                                       str(not_availability))

                            tag_key_completed = \
                                tag_key_completed + \
                                [value_dictionary_of_tag_dictionary[tag_value_not_completed[value]]]

                            tag_value_not_completed_will_be_remove.append(str(tag_dictionary[
                                                                                  value_dictionary_of_tag_dictionary[
                                                                                      tag_value_not_completed[
                                                                                          value]]]).lower())
                            written_number_of_table = written_number_of_table + 1

                    if 0 < len(tag_value_not_completed_will_be_remove):
                        for l in range(len(tag_value_not_completed_will_be_remove)):
                            tag_value_not_completed.remove(tag_value_not_completed_will_be_remove[l])

        return io_details_list

#  ################################################################################################################

    # @staticmethod
    # def chunk_by_verb_and_relevant(text):
    #     chunks = []
    #     sentences = sent_tokenize(text)
    #     grammar = r"""
    #              NBAR  : {<NN.*>*<NN.*>}
    #              CCAR  : {<CC><NBAR>}     # [and X]
    #              NCAR  : {<NBAR><CCAR>*}  # Pressure sensor [and X][and Y][and Z]
    #              FUTPAS: {<MD><RB>*<VB>}
    #              NOV   : {<VBZ|VBP><RB>}
    #              PHR   : {<VBN><IN|RP>}
    #              PAS   : {<VBZ|VBP|FUTPAS|NOV><RB>*<VBN|JJ|VBG|PHR>}
    #              FUT   : {<MD><RB>*<VB>}
    #              NOT   : {<VBZ|VBP><RB><VB>}
    #              ACT   : {<VBZ|VBP|FUT|NOT>}
    #              GR    : {<NBAR|NCAR><ACT|PAS>}
    #              """
    #
    #     for sent in sentences:
    #         words = word_tokenize(sent)
    #         tagged = pos_tag(words)
    #         cp = RegexpParser(grammar)
    #         t = cp.parse(tagged)
    #         t.draw()
    #         for s in t.subtrees():
    #             if s.label() == "GR":
    #                 current_str = ""
    #                 for token in s.leaves():
    #                     current_str = current_str + " " + token[0]
    #                 chunks.append(current_str)
    #     return chunks

    @staticmethod
    def matching_verb_and_not_value_from_io_matrix(entity, i_o_status_matrix):
        verb = ''
        not_value = ''
        io_value = ''
        for i in range(len(i_o_status_matrix)):
            if i_o_status_matrix[i][2] == entity:
                verb = i_o_status_matrix[i][4]
                not_value = i_o_status_matrix[i][5]
                io_value = i_o_status_matrix[i][3]
                return verb, not_value, io_value
        return verb, not_value, io_value

    @staticmethod
    def synonyms_antonyms_of_verb(verb):
        synonyms = []
        antonyms = []
        for syn in wordnet.synsets(verb, pos=wordnet.VERB):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
        synonyms_list = list(set(synonyms))
        antonyms_list = list(set(antonyms))
        return synonyms_list, antonyms_list

    @staticmethod
    def io_status_revers(io_state):
        if str(io_state) == "1":
            return "0"
        elif str(io_state) == "0":
            return "1"
        elif str(io_state) == "True":
            return "0"
        elif str(io_state) == "False":
            return "1"

    @staticmethod
    def io_value_replacer_of_map(entity, io_value, sentence):
        old_entity = str(entity+"=1/0")
        new_entity = str(entity+"="+io_value)
        temp_noun_verb = str(sentence).replace(old_entity, new_entity)
        return temp_noun_verb

    @staticmethod
    def value_replacer_of_mapper(nlp, verb_noun_map_part, verb_noun_mapped_chunks_list_with_verb, i_o_status_matrix):
        value_replaced_map = []

        for i in range(len(verb_noun_map_part)):
            temp_noun_verb = ''
            inputs_list = re.findall("(I[A-Z]=1/0)", verb_noun_map_part[i], re.IGNORECASE)
            output_list = re.findall("(O[A-Z]=1/0)", verb_noun_map_part[i], re.IGNORECASE)
            if 0 == len(inputs_list):
                inputs_list = output_list
            temp_noun_verb = verb_noun_map_part[i]
            for j in range(len(inputs_list)):
                input_temp = str(inputs_list[j][0:2])
                # print(input_temp)
                verb, not_availability, io_value = InputsOutputsStateFinder.matching_verb_and_not_value_from_io_matrix(input_temp,i_o_status_matrix)
                sentence_lemma_verb = verb_noun_mapped_chunks_list_with_verb[i][1]
                sentence_not_availability = verb_noun_mapped_chunks_list_with_verb[i][2]
                if verb == sentence_lemma_verb:
                    if str(not_availability) == str(sentence_not_availability):
                        print("same state")
                        final_io_state = io_value
                        temp_noun_verb = InputsOutputsStateFinder.io_value_replacer_of_map(input_temp,final_io_state,temp_noun_verb)

                    else:
                        print("inverse input")
                        final_io_state = InputsOutputsStateFinder.io_status_revers(io_value)
                        temp_noun_verb = InputsOutputsStateFinder.io_value_replacer_of_map(input_temp, final_io_state,
                                                                                           temp_noun_verb)
                else:
                    synonyms, antonyms = InputsOutputsStateFinder.synonyms_antonyms_of_verb(verb)
                    for i in range(len(synonyms)):
                        if synonyms[i] == sentence_lemma_verb:
                            if str(not_availability) == str(sentence_not_availability):
                                print("same state")
                                final_io_state = io_value
                                temp_noun_verb = InputsOutputsStateFinder.io_value_replacer_of_map(input_temp,
                                                                                                   final_io_state,
                                                                                                   temp_noun_verb)
                                break
                            else:
                                print("inverse statement")
                                final_io_state = InputsOutputsStateFinder.io_status_revers(io_value)
                                temp_noun_verb = InputsOutputsStateFinder.io_value_replacer_of_map(input_temp,
                                                                                                   final_io_state,
                                                                                                   temp_noun_verb)
                                break
                    for i in range(len(antonyms)):
                        if antonyms[i] == sentence_lemma_verb:
                            if str(not_availability) != str(sentence_not_availability):
                                print("same statement")
                                final_io_state = io_value
                                temp_noun_verb = InputsOutputsStateFinder.io_value_replacer_of_map(input_temp,
                                                                                                   final_io_state,
                                                                                                   temp_noun_verb)
                                break
                            else:
                                print("inverse statement")
                                final_io_state = InputsOutputsStateFinder.io_status_revers(io_value)
                                temp_noun_verb = InputsOutputsStateFinder.io_value_replacer_of_map(input_temp,
                                                                                                   final_io_state,
                                                                                                   temp_noun_verb)
                                break

            value_replaced_map = value_replaced_map + [temp_noun_verb]
        return value_replaced_map

    @staticmethod
    def verbs_finder_of_mapper(nlp, verb_noun_mapped_chunks_list):
        """ToDo : remove stop word filter when non phrasal verb and using new regex to identify non phrasal verbs.
        Advantege, there is no phrasal verbs. phrasal verbs filtered at the about stage
        """
        verb_list_of_input_or_output = []
        actual_complex_verb_list = []
        for j in range(len(verb_noun_mapped_chunks_list)):
            # print(verb_noun_mapped_chunks_list[j])
            complex_verbs_of_input_or_output = InputsOutputsStateFinder.complex_verb_finder(nlp, verb_noun_mapped_chunks_list[j])
            for i in range(len(complex_verbs_of_input_or_output)):
                # print(complex_verbs_of_input_or_output[i], "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                not_availability = InputsOutputsStateFinder.not_value_finder(nlp, complex_verbs_of_input_or_output[i])
                # print(not_availability, "Nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooonnn")
                phrasal_verbs_of_input_or_output_sentence = InputsOutputsStateFinder.phrasal_verb_finder(nlp, complex_verbs_of_input_or_output[i])
                # print(phrasal_verbs_of_input_or_output_sentence, "this is outputs 12345")
                if 0 == len(phrasal_verbs_of_input_or_output_sentence):
                    # print(phrasal_verbs_of_input_or_output_sentence, "123456789012333")
                    doc_complex_verb = nlp(complex_verbs_of_input_or_output[i])
                    doc_not_stop_word = (' '.join([str(t) for t in doc_complex_verb if not t.is_stop]))
                    # print(doc_not_stop_word)
                    spliced_verb_stop_word_removed = doc_not_stop_word.split(" ")
                    if 1 < len(spliced_verb_stop_word_removed):
                        print("There is more than one verbs in the chuncker : ", complex_verbs_of_input_or_output[i])
                        return
                    elif 1 == len(spliced_verb_stop_word_removed):
                        non_phrasal_verb_for_lemma = spliced_verb_stop_word_removed[0]
                        # print(non_phrasal_verb_for_lemma)
                        non_phrasal_verb_lemma = WordNetLemmatizer().lemmatize(non_phrasal_verb_for_lemma, 'v')
                        # print(non_phrasal_verb_lemma)
                        verb_list_of_input_or_output = verb_list_of_input_or_output + [non_phrasal_verb_lemma] + [not_availability]
                        # print(verb_list_of_input_or_output, "9999999999999999999999999999999")
                        actual_complex_verb_list = actual_complex_verb_list + [
                            [complex_verbs_of_input_or_output[i]] + [non_phrasal_verb_lemma]+[not_availability]]
                        # print(actual_complex_verb_list, " 88888888888888888888888888888888888888888888")
                else:
                    if 1 < len(phrasal_verbs_of_input_or_output_sentence):
                        print("There is ambiguity on phrasal verbs please correct it on sentence : ", verb_noun_mapped_chunks_list)
                        return
                    else:
                        verb_list_of_input_or_output = verb_list_of_input_or_output + [phrasal_verbs_of_input_or_output_sentence]+[not_availability]
                        actual_complex_verb_list = actual_complex_verb_list + [
                            [complex_verbs_of_input_or_output[j]] + [phrasal_verbs_of_input_or_output_sentence[0]]+[not_availability]]
        # print(actual_complex_verb_list, "GGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRR")
        return actual_complex_verb_list

    @staticmethod
    def i_0_applier_for_input_or_output_part(nlp, sentence, sentence_input_or_output_part, i_o_status_matrix):
        input_or_output_sentence_part = sentence_input_or_output_part
        verb_list_of_input_or_output = []
        actual_complex_verb_list = []
        # print("There is no any tagged output in the sentence : ", tokenize_sentences[i])
        complex_verbs_of_input_or_output = InputsOutputsStateFinder.complex_verb_finder(nlp, sentence_input_or_output_part)
        for i in range(len(complex_verbs_of_input_or_output)):
            phrasal_verbs_of_input_or_output_sentence = InputsOutputsStateFinder.phrasal_verb_finder(nlp, sentence_input_or_output_part)
            if 0 == len(phrasal_verbs_of_input_or_output_sentence):
                doc_complex_verb = nlp(complex_verbs_of_input_or_output[i])
                doc_not_stop_word = (' '.join([str(t) for t in doc_complex_verb if not t.is_stop]))
                spliced_verb_stop_word_removed = doc_not_stop_word.split(" ")
                if 1 < len(spliced_verb_stop_word_removed):
                    print("There is more verbs in the sentence : ", sentence, " sub sentence : ",
                          sentence_input_or_output_part, " in the verb :", complex_verbs_of_input_or_output[i])
                    return
                elif 1 == len(spliced_verb_stop_word_removed):
                    non_phrasal_verb_for_lemma = spliced_verb_stop_word_removed[0]
                    non_phrasal_verb_lemma = WordNetLemmatizer().lemmatize(non_phrasal_verb_for_lemma)
                    verb_list_of_input_or_output = verb_list_of_input_or_output + [non_phrasal_verb_lemma]
                    actual_complex_verb_list = actual_complex_verb_list + [[complex_verbs_of_input_or_output[i]]+[non_phrasal_verb_lemma]]
            else:
                if 1 < len(phrasal_verbs_of_input_or_output_sentence):
                    print("There is ambiguity on phrasal verbs please correct it on sentence : ", sentence)
                    return
                else:
                    verb_list_of_input_or_output = verb_list_of_input_or_output + [phrasal_verbs_of_input_or_output_sentence]
                    actual_complex_verb_list = actual_complex_verb_list + [[complex_verbs_of_input_or_output[i]]+[phrasal_verbs_of_input_or_output_sentence[0]]]
        input_or_output_sentence_part = InputsOutputsStateFinder.value_replacer(nlp, actual_complex_verb_list, input_or_output_sentence_part, i_o_status_matrix)
        return input_or_output_sentence_part

#  ####################################################################################################################
    @staticmethod
    def verb_or_phrasal_verb_lemmatizer(verb):
        lemma_verb_verified = ''
        verb = verb.strip()
        splited_verb = str(verb).split(" ")
        lemma_verb = WordNetLemmatizer().lemmatize(splited_verb[0], 'v')
        if 0 == len(lemma_verb):  # addressing limitation of the verb lemmatizer of wordnet.
            print(" There is a limitation when finding lemmatized verb from : ", splited_verb[0])
            assert True, "Correct the above limitation"
        if 1 == len(splited_verb):
            lemma_verb_verified = lemma_verb
        elif 2 == len(splited_verb):
            lemma_verb_verified = lemma_verb + "_" + splited_verb[1]
        return lemma_verb_verified

    @staticmethod
    def entity_values_generator_sent_part(nlp, sentence_part, verb_noun_map_part, verb_and_negation_list,
                                          i_o_status_matrix):
        value_replaced_map = []

        tags_list = []
        inputs_list = re.findall("(I[A-Z]=1/0)", verb_noun_map_part, re.IGNORECASE)
        outputs_list = re.findall("(O[A-Z]=1/0)", verb_noun_map_part, re.IGNORECASE)
        if 0 == len(inputs_list):
            tags_list = outputs_list
        elif 0 == len(outputs_list):
            tags_list = inputs_list

        negation_map_part = ''
        if '' == verb_and_negation_list[0]:
            negation_map_part = 'False'
        elif 'not' == verb_and_negation_list[0].lower():
            negation_map_part = 'True'
        verb_map_part = verb_and_negation_list[1]
        io_generated_map_part = verb_noun_map_part
        for j in range(len(tags_list)):
            entity_tag_temp = str(tags_list[j][0:2])

            verb_io, not_availability_io, value_io = \
                InputsOutputsStateFinder.matching_verb_and_not_value_from_io_matrix(entity_tag_temp, i_o_status_matrix)

            lemma_verb_map_part = InputsOutputsStateFinder.verb_or_phrasal_verb_lemmatizer(verb_map_part)
            lemma_verb_io = InputsOutputsStateFinder.verb_or_phrasal_verb_lemmatizer(verb_io)
            map_part_not_availability = negation_map_part
            if lemma_verb_io == lemma_verb_map_part:
                if str(not_availability_io) == str(map_part_not_availability):
                    print("same state")
                    final_io_state = value_io

                    io_generated_map_part = \
                        InputsOutputsStateFinder.io_value_replacer_of_map(entity_tag_temp,
                                                                          final_io_state,
                                                                          io_generated_map_part)

                else:
                    print("inverse input")
                    final_io_state = InputsOutputsStateFinder.io_status_revers(value_io)

                    io_generated_map_part = \
                        InputsOutputsStateFinder.io_value_replacer_of_map(entity_tag_temp,
                                                                          final_io_state,
                                                                          io_generated_map_part)
            else:
                synonyms, antonyms = InputsOutputsStateFinder.synonyms_antonyms_of_verb(lemma_verb_io)
                for i in range(len(synonyms)):
                    if synonyms[i] == lemma_verb_map_part:
                        if str(not_availability_io) == str(map_part_not_availability):
                            print("same state")
                            final_io_state = value_io

                            io_generated_map_part = \
                                InputsOutputsStateFinder.io_value_replacer_of_map(entity_tag_temp,
                                                                                  final_io_state,
                                                                                  io_generated_map_part)
                            break
                        else:
                            print("inverse statement")
                            final_io_state = InputsOutputsStateFinder.io_status_revers(value_io)

                            io_generated_map_part = \
                                InputsOutputsStateFinder.io_value_replacer_of_map(entity_tag_temp,
                                                                                  final_io_state,
                                                                                  io_generated_map_part)
                            break
                for i in range(len(antonyms)):
                    if antonyms[i] == lemma_verb_map_part:
                        if str(not_availability_io) != str(map_part_not_availability):
                            print("same statement")
                            final_io_state = value_io

                            io_generated_map_part = \
                                InputsOutputsStateFinder.io_value_replacer_of_map(entity_tag_temp,
                                                                                  final_io_state,
                                                                                  io_generated_map_part)
                            break
                        else:
                            print("inverse statement")
                            final_io_state = InputsOutputsStateFinder.io_status_revers(value_io)

                            io_generated_map_part = \
                                InputsOutputsStateFinder.io_value_replacer_of_map(entity_tag_temp,
                                                                                  final_io_state,
                                                                                  io_generated_map_part)
                            break
        sentence_part = str(sentence_part).replace(verb_noun_map_part, io_generated_map_part)
        return sentence_part

    @staticmethod
    def identify_map_verbs_with_negation(nlp, sentences):
        """Errors are happens when sentences are list type, hint: extracts string from the list"""
        sentences = sent_tokenize(sentences)
        grammar = r"""
                  GR : {<RB>*<VB|VBN|JJ|VBG|VBZ|VBP|VBD>+<IN|RP>*} 
                  """
        # GR : {<RB>*<VB|VBN|JJ|VBG|VBZ|VBP>+<IN|RP>*}
        map_part_verb_and_negation = []
        for sent in sentences:
            # sample = sent.split('=')
            words = word_tokenize(sent)
            tagged = pos_tag(words)
            cp = RegexpParser(grammar)
            t = cp.parse(tagged)
            # t.draw()
            negate = ''
            verb = ''
            verbs = []
            for s in t.subtrees():
                is_phrasal = False
                if s.label() == "GR":
                    for token in s.leaves():
                        if token[0] == 'is' or token[0] == 'are' or token[0] == 'does' or token[0] == 'do':
                            continue
                        elif token[1] == 'RB':
                            negate = token[0]
                        elif token[0] != "=":
                            verb = verb + " " + token[0]
            verb = InputsOutputsStateFinder.phrasal_verb_verifier_or_verb_part_extractor(nlp, verb)
            verbs.append([negate, verb])
            map_part_verb_and_negation.append(verbs)
        return map_part_verb_and_negation.pop()

    @staticmethod
    def one_or_zero_applier_for_logic_sentence(nlp, logic_sentences, i_o_status_matrix, noun_verb_map_set):
        completed_logic_sentences = ''
        tokenize_sentences = nltk.tokenize.sent_tokenize(logic_sentences)
        if len(tokenize_sentences) != len(noun_verb_map_set):
            print("noun_verb_map_set length not match with sentences count")
            return
        for i in range(len(tokenize_sentences)):
            completed_logic_sentence = ''
            splited_sentence = tokenize_sentences[i].split(",")
            noun_verb_map_set_of_each_sentence = noun_verb_map_set[i]
            if 2 < len(splited_sentence):
                print(" Two or more ',' not allow in the logical sentence : ", tokenize_sentences[i])
                return
            elif 2 > len(splited_sentence):
                print(" There is no any ',' in the logical sentence : ", tokenize_sentences[i])
                return
            else:
                input_count_of_first_part = len(re.findall("(I[A-Z]=1/0)", splited_sentence[0], re.IGNORECASE))
                input_count_of_second_part = len(re.findall("(I[A-Z]=1/0)", splited_sentence[1], re.IGNORECASE))
                output_count_of_first_part = len(re.findall("(O[A-Z]=1/0)", splited_sentence[0], re.IGNORECASE))
                output_count_of_second_part = len(re.findall("(O[A-Z]=1/0)", splited_sentence[1], re.IGNORECASE))
                if (0 < input_count_of_first_part and 0 < output_count_of_first_part) or (
                        0 < input_count_of_second_part and 0 < output_count_of_second_part):
                    print("Inputs and outputs in the same side in the logic sentence : ", tokenize_sentences[i])
                    return

                for part_of_logic_sentence in range(len(splited_sentence)):
                    completed_logic_sentence_part = ''
                    inputs_list = re.findall("(I[A-Z]=1/0)", splited_sentence[part_of_logic_sentence],
                                             re.IGNORECASE)
                    # "(I[A-Z]=\d[,and ])" when IA = 1 (No need)
                    outputs_list = re.findall("(O[A-Z]=1/0)", splited_sentence[part_of_logic_sentence],
                                              re.IGNORECASE)
                    # "(O[A-Z]=\d[,and ])" when OZ = 1 (No need)
                    if 0 == len(inputs_list) and 0 == len(outputs_list):
                        print("There is no any tagged input or output in the sentence : ", tokenize_sentences[i])
                        return
                    if 0 < len(inputs_list) and 0 < len(outputs_list):
                        print("There are inputs and outputs in the same side : ", " of the conditional sentence : ", )
                        return
                    for r in range(len(noun_verb_map_set_of_each_sentence[part_of_logic_sentence])):

                        verb_and_negation_map_part = \
                            InputsOutputsStateFinder.identify_map_verbs_with_negation(
                                nlp, noun_verb_map_set_of_each_sentence[part_of_logic_sentence][r])

                        if 1 != len(verb_and_negation_map_part):
                            print(" There is no any verb or two or more verbs in the map part : ",
                                  noun_verb_map_set_of_each_sentence[part_of_logic_sentence][r])
                            assert True, " Please correct the above limitation on the scenario."
                        if 0 == len(completed_logic_sentence_part):

                            completed_sent_part = \
                                InputsOutputsStateFinder.entity_values_generator_sent_part(
                                    nlp, splited_sentence[part_of_logic_sentence],
                                    noun_verb_map_set_of_each_sentence[part_of_logic_sentence][r],
                                    verb_and_negation_map_part[0], i_o_status_matrix)

                            completed_logic_sentence_part = completed_sent_part
                        else:

                            completed_sent_part = \
                                InputsOutputsStateFinder.entity_values_generator_sent_part(
                                    nlp, completed_logic_sentence_part,
                                    noun_verb_map_set_of_each_sentence[part_of_logic_sentence][r],
                                    verb_and_negation_map_part[0], i_o_status_matrix)

                            completed_logic_sentence_part = completed_sent_part

                    if 0 == part_of_logic_sentence:
                        completed_logic_sentence_part = str(completed_logic_sentence_part).strip() + ", "
                        completed_logic_sentence = completed_logic_sentence + completed_logic_sentence_part
                    else:
                        completed_logic_sentence_part = str(completed_logic_sentence_part).strip() + " "
                        completed_logic_sentence = completed_logic_sentence + completed_logic_sentence_part
            completed_logic_sentences = completed_logic_sentences + completed_logic_sentence
        return completed_logic_sentences

#  #############################################################################################################
