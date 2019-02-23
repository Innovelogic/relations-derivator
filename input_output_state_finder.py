import nltk
import textacy
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


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

    @staticmethod
    def not_value_finder(nlp, verb_of_sentence):
        """
        getting not availability state of each sentence
        :param nlp:
        :param verb_of_sentence:
        :return:
        """
        doc_verb = nlp(verb_of_sentence)
        not_availability = False
        for token in doc_verb:
            if token.text == "not" and token.tag_ == "RB" and token.pos_ == "ADV":
                not_availability = True
        return not_availability

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
    def non_phrasal_verb_finder(nlp, complex_verb):
        """
        Non phrasal verbs (normal verbs) finding from the verb phrases (Verifing from the Wordnet)
        :param nlp:
        :param complex_verb:
        :return:
        """
        non_phrasal_verb = []
        doc_complex_verb = nlp(complex_verb)
        doc_not_stop_word = (' '.join([str(t) for t in doc_complex_verb if not t.is_stop]))
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
    def verb_and_not_word_availability_finder(nlp, sentence):
        """
        Getting verbs and not state availability of the sentences
        :param nlp:
        :param sentence:
        :return:
        """
        verb = []
        not_availability = True
        sentence_all_complex_verbs = []
        # this list will catch all verb element of sentence, the phrasal verb or verb or any other VERB format etc.
        doc_sentence = nlp(sentence)
        pattern = r'<VERB>*<ADV>*<PART>*<VERB>+<PART>*'  # <VB.*>*<RB>*<RP>*<VB.*>+<PP>*
        doc_each_sentence = textacy.Doc(doc_sentence, lang='en_core_web_sm')
        lists_verbs = textacy.extract.pos_regex_matches(doc_each_sentence, pattern)
        for complex_verb in lists_verbs:
            sentence_all_complex_verbs = sentence_all_complex_verbs + [complex_verb.text]

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
                    tem_verb])
                if 1 < len(non_phrasal_verb):
                    print("There is more than one non phrasal verb here in the sentence : ", sentence)
                    verb = []  # in the inputs output statement applier method will check verb length.
                # So, remove verbs because of ignore previous verbs
                    return verb, not_availability
                elif 1 == len(non_phrasal_verb):
                    verb = verb + [non_phrasal_verb]
        return verb, not_availability

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
        io_details_list = [["" for x in range(6)] for y in range(
            len(tag_dictionary))]  # example tuple [[NN], [NNP], [tag_key], [I/O_State], [Verb], [not on the verb]]

        tag_dictionary_key_list = []
        for k, v in tag_dictionary.items():
            tag_dictionary_key_list = tag_dictionary_key_list+[str(k).lower()]

        reference_dictionary_key_list = []
        for k, v in reference_dictionary.items():
            reference_dictionary_key_list = reference_dictionary_key_list+[str(k).lower()]

        written_number_of_table = 0

        io_sentences = nltk.tokenize.sent_tokenize(io_states_sentences)

        for checking_sentence in range(len(io_sentences)):
            if str(io_sentences[checking_sentence][0]).islower():
                print(io_sentences[checking_sentence][0], "letter must be capital in the sentence : ",
                      io_sentences[checking_sentence], " of the I/O_Status.")
                return io_details_list

        for i in range(len(io_sentences)):
            doc_sentence = nlp(io_sentences[i])
            # getting I/O state value for relevant sentence. ex :- value is 1
            io_states_current = InputsOutputsStateFinder.one_zero_finder(nlp, io_sentences[i])

            # getting verb statement. limitations on the phrasal verbs. # "Not" included. "ToDo"
            # should implement not finder within this step
            verb, not_availability = InputsOutputsStateFinder.verb_and_not_word_availability_finder(nlp,
                                                                                                    io_sentences[i])

            if 1 < len(verb):
                print(
                    "There are more than one sentences in the sentence or sentences not in "
                    "the right format in the sentence : ",
                    io_sentences[i], " Hint 1: Sensor works sounds Hint 2: the ........")
                return
            elif 0 == len(verb):
                print("There is no verb in the sentence :", io_sentences[i])
            tag_key_completed = []
            verb = verb[0]  # getting verb sub list from the string list list
            for ref in range(len(reference_dictionary_key_list)):
                if reference_dictionary_key_list[ref] in str(
                        io_sentences[i]).lower():  # if entity on the reference dictionary
                    split_tag_key_temp = str(reference_dictionary[reference_dictionary_key_list[ref]]).split(' and ')
                    for n in range(len(split_tag_key_temp)):
                        io_details_list[written_number_of_table][0] = reference_dictionary_key_list[ref]
                        io_details_list[written_number_of_table][1] = split_tag_key_temp[n]
                        io_details_list[written_number_of_table][2] = tag_dictionary[split_tag_key_temp[n]]
                        io_details_list[written_number_of_table][3] = io_states_current
                        io_details_list[written_number_of_table][4] = verb[0]
                        io_details_list[written_number_of_table][5] = str(not_availability)
                        tag_key_completed = tag_key_completed + [split_tag_key_temp[n]]
                        written_number_of_table = written_number_of_table + 1
                else:
                    if 0 == len(tag_key_completed):
                        for tag in range(len(tag_dictionary_key_list)):
                            if tag_dictionary_key_list[tag] in str(io_sentences[i]).lower():
                                io_details_list[written_number_of_table][0] = "NO_REFERENCE"
                                io_details_list[written_number_of_table][1] = tag_dictionary_key_list[tag]
                                io_details_list[written_number_of_table][2] = tag_dictionary[
                                    tag_dictionary_key_list[tag]]
                                io_details_list[written_number_of_table][3] = io_states_current
                                io_details_list[written_number_of_table][4] = verb[0]
                                io_details_list[written_number_of_table][5] = str(not_availability)
                                tag_key_completed = tag_key_completed + [tag_dictionary_key_list[tag]]
                                written_number_of_table = written_number_of_table + 1
                    else:
                        for competed_tag in range(len(tag_key_completed)):
                            if not tag_key_completed[competed_tag] in str(io_sentences[i]).lower():
                                for tag in range(len(tag_dictionary_key_list)):
                                    if tag_dictionary_key_list[tag] in str(io_sentences[i]).lower():
                                        io_details_list[written_number_of_table][0] = "NO_REFERENCE"
                                        io_details_list[written_number_of_table][1] = tag_dictionary_key_list[tag]
                                        io_details_list[written_number_of_table][2] = tag_dictionary[
                                            tag_dictionary_key_list[tag]]
                                        io_details_list[written_number_of_table][3] = io_states_current
                                        io_details_list[written_number_of_table][4] = verb[0]
                                        io_details_list[written_number_of_table][5] = str(not_availability)
                                        tag_key_completed = tag_key_completed + [tag_dictionary_key_list[tag]]
                                        written_number_of_table = written_number_of_table + 1
        return io_details_list

