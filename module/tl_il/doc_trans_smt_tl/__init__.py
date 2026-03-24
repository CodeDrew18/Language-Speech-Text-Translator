from module.tl_il.rule_based_tl import dict_tl, tokenized, pos
from module.il_tl.rule_based_il import dict_il
from module.functions.global_funcs import combine_tokens, remove_punct
from module.smt import encapsulate, ngram_var
import pandas as pd

def get_sum_tl(sen_poss_list, dict_src, not_in_sw, not_in_vb, not_in_nn, not_in_jj, not_in_rb, not_in_cc, not_in_pr, not_in_dt, not_tagged, sum_tf_idf_tl_list, vb_tl_tf_idf_list, nn_tl_tf_idf_list, jj_tl_tf_idf_list, rb_tl_tf_idf_list, cc_tl_tf_idf_list, pr_tl_tf_idf_list, dt_tl_tf_idf_list):
    """
    This function computes for the lexial probabilities of a sentence
    
    Parameters:
        sen_poss_list (list): A list of parts of speech (POS) for each word in the sentence.
        dict_src (dict): An object that contains information about words and their corresponding POS in both the source language (Tagalog) and the target language (Ilokano).
        not_in_'' (list): Lists of words in the sentence that are not found in the corresponding lists of words in the target language (Ilokano).
        not_tagged: A list of words in the sentence that are not tagged with a POS.
        sum_tf_idf_tl_list, ''_tl_tf_idf_list (list): Lists of values that represent the lexical probabilities of the corresponding word lists in the target language (Ilokano).
    
    Returns:
        (list): Returns the sum_tf_idf_tl_list which represents the lexical probabilities for the sentence.
    """

    sp_index = 0
    
    for pos_src in sen_poss_list:
        """
        pos_srcs is a list of POS of a sentence
        eg. ['VB', 'DT', 'NN', 'DT', 'NN']
        """
        
        sum_tf_idf_tl = 0
        wp_index = 0
        
        for word_pos in pos_src:
            word = dict_src['Tokenized'][sp_index][wp_index]
            
            # 1. SW
            if word_pos == 'SW':
                """
                if the POS of the word is 'SW'
                """
                if word in dict_tl.sw_tl_list:
                    """
                    if the word is in the Tagalog list of single words
                    """
                    temp_index = dict_tl.sw_tl_list.index(word)
                    
                else:
                    not_in_sw.append(word)
                                
            # 2. SW
            elif word_pos == 'VB':
                """
                if the POS of the word is 'VB'
                """
                if word in dict_tl.vb_tl_list:
                    """
                    if the word is in the Tagalog list of verbs
                    """
                    temp_index = dict_tl.vb_tl_list.index(word)
                    sum_tf_idf_tl += vb_tl_tf_idf_list[temp_index]
                else:
                    not_in_vb.append(word)
            
            # 3. NN
            elif word_pos == 'NN':
                """
                if the POS of the word is 'NN'
                """
                if word in dict_tl.nn_tl_list:
                    """
                    if the word is in the Tagalog list of nouns
                    """
                    temp_index = dict_tl.nn_tl_list.index(word)
                    sum_tf_idf_tl += nn_tl_tf_idf_list[temp_index]
                else:
                    not_in_nn.append(word)
            
            # 4. JJ
            elif word_pos == 'JJ':
                """
                if the POS of the word is 'JJ'
                """
                if word in dict_tl.jj_tl_list:
                    """
                    if the word is in the Tagalog list of nouns
                    """
                    temp_index = dict_tl.jj_tl_list.index(word)
                    sum_tf_idf_tl += jj_tl_tf_idf_list[temp_index]
                else:
                    not_in_jj.append(word)
            
            # 5. RB
            elif word_pos == 'RB':
                """
                if the POS of the word is 'RB'
                """
                if word in dict_tl.rb_tl_list:
                    """
                    if the word is in the Tagalog list of nouns
                    """
                    temp_index = dict_tl.rb_tl_list.index(word)
                    sum_tf_idf_tl += rb_tl_tf_idf_list[temp_index]
                else:
                    not_in_rb.append(word)
                    
            # 6. CC
            elif word_pos == 'CC':
                """
                if the POS of the word is 'CC'
                """
                if word in dict_tl.cc_tl_list:
                    """
                    if the word is in the Tagalog list of nouns
                    """
                    temp_index = dict_tl.cc_tl_list.index(word)
                    sum_tf_idf_tl += cc_tl_tf_idf_list[temp_index]
                else:
                    not_in_cc.append(word)
                    
            # 7. PR
            elif word_pos == 'PR':
                """
                if the POS of the word is 'CC'
                """
                if word in dict_tl.pr_tl_list:
                    """
                    if the word is in the Tagalog list of nouns
                    """
                    temp_index = dict_tl.pr_tl_list.index(word)
                    sum_tf_idf_tl += pr_tl_tf_idf_list[temp_index]
                else:
                    not_in_pr.append(word)
            
             # 8. DT
            elif word_pos == 'DT':
                """
                if the POS of the word is 'DT'
                """
                if word in dict_tl.dt_tl_list:
                    """
                    if the word is in the Tagalog list of nouns
                    """
                    temp_index = dict_tl.dt_tl_list.index(word)
                    sum_tf_idf_tl += dt_tl_tf_idf_list[temp_index]
                else:
                    not_in_dt.append(word)
            
            else:
                not_tagged.append(word)
                
            wp_index += 1
        
        sum_tf_idf_tl_list.append(round(sum_tf_idf_tl, 5))
        sp_index += 1
        
    return sum_tf_idf_tl_list
# end of get_sum_tl

def tl_trans_lm(ngram_data, tl_struct, il_struct, il_struct_count):
    """
    This function performs language model based translation of the input sentences.
    
    Parameters:
        ngram_data (list): List of sentences, where each sentence is a list of n-grams
        tl_struct (list): List of source language (TL) n-grams
        il_struct (list): List of target language (IL) n-grams corresponding to each tL n-gram in 'tl_struct'
        il_struct_count (list): List of the frequency counts of each IL n-gram in 'il_struct'
    
    Returns:
        list: List of translated sentences, where each sentence is a list of translated n-grams
    """

    trans_ngram_data = []
    for ngram_sen in ngram_data:
        trans_ngram_sen = []
        
        for ngram in ngram_sen:
            if ngram in tl_struct:
                temp_index = tl_struct.index(ngram)
                max_count = max(il_struct_count[temp_index])
                trans_index = il_struct_count[temp_index].index(max_count)
                trans_ngram = il_struct[temp_index][trans_index]
                trans_ngram_sen.append(trans_ngram)
            else:
                trans_ngram_sen.append(ngram)
        
        trans_ngram_data.append(trans_ngram_sen)
        
    return trans_ngram_data
# end of tl_trans_lm

def in_F_Phrases(word, word2, word3, word4, word5, word6, word7, lang_tar):
    """
    Check if a given set of words form a phrase in the phrase list.
    
    Parameters:
        word (str): The first word to check.
        word2 (str): The second word to check.
        word3 (str): The third word to check.
        word4 (str): The fourth word to check.
        word5 (str): The fifth word to check.
        word6 (str): The sixth word to check.
        word7 (str): The seventh word to check.
        lang_tar (list): List of phrases in Tagalog.
    
    Returns:
        tuple: A tuple containing three values:
            - inFPhrases (bool): Indicates if the words form a phrase.
            - tl_phrase (list): The phrase formed by the words, if any.
            - w_used (int): The number of words used to form the phrase.
    """
    inFPhrases = False
    tl_phrase = []
    w_used = 0

    for phrase in lang_tar:
        length = len(phrase)
        if length == 7:
            if word == phrase[0] and word2 == phrase[1] and word3 == phrase[2] and word4 == phrase[3] and word5 == phrase[4] and word6 == phrase[5] and word7 == phrase[6]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 7
                break
        if length == 6:
            if word == phrase[0] and word2 == phrase[1] and word3 == phrase[2] and word4 == phrase[3] and word5 == phrase[4] and word6 == phrase[5]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 6
                break
        if length == 5:
            if word == phrase[0] and word2 == phrase[1] and word3 == phrase[2] and word4 == phrase[3] and word5 == phrase[4]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 5
                break
        if length == 4:
            if word == phrase[0] and word2 == phrase[1] and word3 == phrase[2] and word4 == phrase[3]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 4
                break
        if length == 3:
            if word == phrase[0] and word2 == phrase[1] and word3 == phrase[2]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 3
                break
        if length == 2:
            if word == phrase[0] and word2 == phrase[1]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 2
                break
        if length == 1:
            if word == phrase[0]:
                inFPhrases = True
                tl_phrase = phrase
                w_used = 1
                break 
                
    return inFPhrases, tl_phrase, w_used
# end of in_F_Phrases


def tl_translate_smt(sen_poss_list, dict_src, vb_tl_tf_idf_list, nn_tl_tf_idf_list, jj_tl_tf_idf_list, rb_tl_tf_idf_list, cc_tl_tf_idf_list, pr_tl_tf_idf_list, dt_tl_tf_idf_list, tl_struct, il_struct, il_struct_count):
    """
    This function translates sentences from the source language (tl) to the target language (il) based on the part-of-speech information and the dictionaries of words and their translations.
    
    Parameters:
        sen_poss_list (list): List of lists of words and their corresponding part-of-speech information.
        dict_src (dict): Dictionary of words in the source language and their corresponding words in the target language.
        ''_tl_tf_idf_list (list): List of tf-idf scores of pos in the source language.
        tl_struct (list): List of structures of sentences in the source language.
        il_struct (list): List of structures of sentences in the target language.
        il_struct_count (int): Count of structures of sentences in the target language.

    Returns:
        sen_translation_list (list): List of sentences translated from the source language to the target language.
    """

    lang_src = [remove_punct(word) for word in dict_il.lang_src]
    lang_src = [tokenized(word) for word in lang_src]

    lang_tar = [remove_punct(word) for word in dict_tl.lang_tar]
    lang_tar = [tokenized(word) for word in lang_tar]
    
    not_in_sw = []
    not_in_vb = []
    not_in_nn = []
    not_in_jj = []
    not_in_rb = []
    not_in_cc = []
    not_in_pr = []
    not_in_dt = []
    not_tagged = []
    sum_tf_idf_tl_list = []

    sum_tf_idf_tl_list = get_sum_tl(sen_poss_list, dict_src, not_in_sw, not_in_vb, not_in_nn, not_in_jj, not_in_rb, not_in_cc, not_in_pr, not_in_dt, not_tagged, sum_tf_idf_tl_list, vb_tl_tf_idf_list, nn_tl_tf_idf_list, jj_tl_tf_idf_list, rb_tl_tf_idf_list, cc_tl_tf_idf_list, pr_tl_tf_idf_list, dt_tl_tf_idf_list)
    
    encapsulate(sen_poss_list, ngram_var.fourgram_list, ngram_var.trigram_list, ngram_var.bigram_list, ngram_var.unigram_list, ngram_var.ngram_list, ngram_var.notencap_list, ngram_var.fourgram_count_sen, ngram_var.trigram_count_sen, ngram_var.bigram_count_sen, ngram_var.unigram_count_sen, ngram_var.notencap_count_sen)
    
    ngram_data = ngram_var.ngram_list
    
    trans_ngram_data = tl_trans_lm(ngram_data, tl_struct, il_struct, il_struct_count)
    
    sp_index = 0
    sen_translation_list = []
    
    for pos_src in sen_poss_list:
        """
        pos_src is a list of POS of a sentence
        eg. ['VB', 'DT', 'NN', 'DT', 'NN']
        """
        sen_translation = []
        wp_index = 0
        cur_wp_index = 0
        
        for word_pos in pos_src:
            if wp_index == cur_wp_index:
                word = dict_src['Tokenized'][sp_index][wp_index]
                
                try: 
                    word2 = dict_src['Tokenized'][sp_index][wp_index+1]
                except:
                    word2 = None
                try:
                    word3 = dict_src['Tokenized'][sp_index][wp_index+2]
                except:
                    word3 = None
                try:
                    word4 = dict_src['Tokenized'][sp_index][wp_index+3]
                except:
                    word4 = None
                try:
                    word5 = dict_src['Tokenized'][sp_index][wp_index+4]
                except:
                    word5 = None
                try:
                    word6 = dict_src['Tokenized'][sp_index][wp_index+5]
                except:
                    word6 = None
                try:
                    word7 = dict_src['Tokenized'][sp_index][wp_index+6]
                except:
                    word7 = None
                    
                ans = in_F_Phrases(word, word2, word3, word4, word5, word6, word7,lang_tar)
                inFPDict = ans[0]
                tl_phrase = ans[1]
                w_used = ans[2]                
                
                if inFPDict:
                    """
                    if the word is in the list of Tagalog phrases
                    """
                    p_index = lang_tar.index(tl_phrase)
                    il_phrase = lang_src[p_index]
                    for il_word in il_phrase:
                        sen_translation.append(il_word)
                    cur_wp_index = wp_index + w_used
                    
                else:
                    cur_wp_index = wp_index + 1

                    # 1. SW
                    if word_pos == 'SW':
                        """
                        if the POS of the word is 'SW'
                        """
                        if word in dict_tl.sw_tl_list:
                            temp_index = dict_tl.sw_tl_list.index(word)
                            if dict_tl.sw_il_list[temp_index][0] == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(dict_tl.sw_il_list[temp_index][0])
                        else:
                            sen_translation.append(word)
                    
                    # 2. VB
                    elif word_pos == 'VB':
                        """
                        if the POS of the word is 'VB'
                        """
                        if word in dict_tl.vb_tl_list:
                            """
                            if the word is in the Tagalog list of verbs
                            """
                            tl_index = dict_tl.vb_tl_list.index(word)
                            max_tlidf = max(dict_tl.vb_tfidf_il_list[tl_index])
                            il_index = dict_tl.vb_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.vb_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                    
                    # 3. NN
                    elif word_pos == 'NN':
                        """
                        if the POS of the word is 'NN'
                        """
                        if word in dict_tl.nn_tl_list:
                            """
                            if the word is in the Tagalog list of noun
                            """
                            tl_index = dict_tl.nn_tl_list.index(word)
                            max_tlidf = max(dict_tl.nn_tfidf_il_list[tl_index])
                            il_index = dict_tl.nn_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.nn_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                    
                    # 4. JJ
                    elif word_pos == 'JJ':
                        """
                        if the POS of the word is 'JJ'
                        """
                        if word in dict_tl.jj_tl_list:
                            """
                            if the word is in the Tagalog list of adjectives
                            """
                            tl_index = dict_tl.jj_tl_list.index(word)
                            max_tlidf = max(dict_tl.jj_tfidf_il_list[tl_index])
                            il_index = dict_tl.jj_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.jj_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                            
                    # 5. RB
                    elif word_pos == 'RB':
                        """
                        if the POS of the word is 'RB'
                        """
                        if word in dict_tl.rb_tl_list:
                            """
                            if the word is in the Tagalog list of adverbs
                            """
                            tl_index = dict_tl.rb_tl_list.index(word)
                            max_tlidf = max(dict_tl.rb_tfidf_il_list[tl_index])
                            il_index = dict_tl.rb_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.rb_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                    
                    # 6. CC
                    elif word_pos == 'CC':
                        """
                        if the POS of the word is 'CC'
                        """
                        if word in dict_tl.cc_tl_list:
                            """
                            if the word is in the Tagalog list of conjunctions
                            """
                            tl_index = dict_tl.cc_tl_list.index(word)
                            max_tlidf = max(dict_tl.cc_tfidf_il_list[tl_index])
                            il_index = dict_tl.cc_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.cc_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                            
                    # 7. PR
                    elif word_pos == 'PR':
                        """
                        if the POS of the word is 'PR'
                        """
                        if word in dict_tl.pr_tl_list:
                            """
                            if the word is in the Tagalog list of prepositions
                            """
                            tl_index = dict_tl.pr_tl_list.index(word)
                            max_tlidf = max(dict_tl.pr_tfidf_il_list[tl_index])
                            il_index = dict_tl.pr_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.pr_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                            
                    # 8. DT
                    elif word_pos == 'DT':
                        """
                        if the POS of the word is 'DT'
                        """
                        if word in dict_tl.dt_tl_list:
                            """
                            if the word is in the Tagalog list of determiners
                            """
                            tl_index = dict_tl.dt_tl_list.index(word)
                            max_tlidf = max(dict_tl.dt_tfidf_il_list[tl_index])
                            il_index = dict_tl.dt_tfidf_il_list[tl_index].index(max_tlidf)
                            il_word = dict_tl.dt_il_list[tl_index][il_index]
                            
                            if il_word == 'None':
                                sen_translation.append(word)
                            else:
                                sen_translation.append(il_word)
                        else:
                            sen_translation.append(word)
                    
                    else:
                        sen_translation.append(word)

            wp_index += 1
        sp_index += 1
        sen_translation_list.append(sen_translation)
    
    return sen_translation_list
# end of tl_translate_smt

def tl_smt_trans(source):
    """
    This function takes in a source text in Tagalog language and returns a dataframe with the system output and expected output along with their scores.
    
    Parameters:
        source (str): The input text in Tagalog language.
    
    Returns:
        dict_tl_op_ex (DataFrame): A dataframe with two columns - 'System Output' and 'Expected Output' - which contain the system and expected outputs, respectively.
    """
    
    # Splitting the source text into sentences
    parsed_source = source.split("\r\n")

    # Removing punctuation from the sentences
    cleaned_source = [remove_punct(word) for word in parsed_source]
    
    # Tokenizing the sentences
    tok_src = [tokenized(word) for word in cleaned_source]

    # Creating a dataframe to store the tokenized sentences
    dict_src = pd.DataFrame({'Tokenized': tok_src}) 
    
    # Tagging the parts of speech for each word in the sentences
    pos_sen_list = pos(dict_src['Tokenized'])

    # Adding the POS tagged sentences to the dataframe
    dict_src['POS'] = pos_sen_list

    # Translating the sentences using the SMT method
    sen_translation_list = tl_translate_smt(dict_src['POS'], dict_src, dict_tl.vb_tl_tf_idf_list, dict_tl.nn_tl_tf_idf_list, dict_tl.jj_tl_tf_idf_list, dict_tl.rb_tl_tf_idf_list, dict_tl.cc_tl_tf_idf_list, dict_tl.pr_tl_tf_idf_list, dict_tl.dt_tl_tf_idf_list, dict_tl.tl_struct, dict_tl.il_struct, dict_tl.il_struct_count)
    
    # Combining the translated words to form complete sentences
    temp_sen_list = combine_tokens(sen_translation_list)

    # Creating a dataframe to store the system output and expected output along with their scores
    dict_tl_op_ex = pd.DataFrame({'System Output': temp_sen_list})

    return dict_tl_op_ex
# end of smt_trans