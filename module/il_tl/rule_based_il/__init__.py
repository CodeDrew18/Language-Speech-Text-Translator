import re
from module.il_tl.rule_based_il import lists_il

def tokenized(text):
    """
    This function takes in a text string as input and returns a list of tokens (words) extracted from the input text.

    Parameters:
        text (str): the text to be tokenized

    Returns:
        list: a list of tokens (words) extracted from the input text
    """
    # Convert the text to lowercase and split it into tokens based on non-word characters
    tokens = re.split('\W+', text.lower())
    
    # Remove any empty tokens from the list of tokens
    tokens = [token for token in tokens if token]
    
    # Check if the current token, next token, and next next token form the specific string 'naaramid a casta'
    # If so, merge the three tokens into one
    i = 0
    while i < len(tokens) - 2:
        if tokens[i] == 'naaramid' and tokens[i+1] == 'a' and tokens[i+2] == 'casta':
            tokens[i] = " ".join([tokens[i], tokens[i+1], tokens[i+2]])
            del tokens[i+1:i+3]
        i += 1
    
    return tokens
# end of tok_src

"""
Determiner Checker Function
"""
def isDtmn(word, noun_dtmn_list, adv_dtmn_list, prepo_dtmn_list, adv_time_list):
    """
    This function checks if the specific word in the sentence is a determiner, and extracts it.
    """
    if word in (noun_dtmn_list + adv_dtmn_list + prepo_dtmn_list + adv_time_list):
        ans = True
    else:
        ans = False

    return ans
# end of isDtmn


"""
Verb Affixer Checker Function
"""
def check_verb_affixes(word, isTagged, hasVerbAffixes, PREFIX_SET, INFIX_SET, SUFFIX_SET):
    """
    This function checks if the specific word in the sentence has a verb affix, and extracts it.
    """
    for prefix in PREFIX_SET:
        if word.startswith(prefix) and not isTagged:
            hasVerbAffixes = True
            isTagged = True
            
    for infix in INFIX_SET:
        if word.__contains__(infix) and not isTagged:
            """
            eg. kinunana = sinabi
            """
            hasVerbAffixes = True
            isTagged = True
    
    for suffix in SUFFIX_SET:
        """
        words ending with 'ang' are adverbs and after the adverbs are the nouns 
        """
        if word.endswith(suffix) and not isTagged:
            hasVerbAffixes = True
            isTagged = True
    
    return hasVerbAffixes
# end of check_verb_affixes

"""
Verb Checker Function
"""
def isVerb(word, prev_word, prev2_word, next_word, hasVerbAffixes, PREPO_SET, PER_PRONOUN, CONJ_SET, noun_dtmn_list, adv_dtmn_list, prepo_dtmn_list):
    """
    This function tags if the specific word in the sentence is a verb, and extracts it.
    """
    isDone = False
    isVerb = False
    
    if word not in PREPO_SET:    
        if word == 'espiritu' and not isDone:
            """
            if the word is 'espiritu' then it is not a verb
            eg. 'Esperitu' = 'spirit' (ti espiritu ti Dios)
            """
            isVerb = False
            isDone = True
           
        if word == 'naimbag' and not isDone:
            """
            naimbag = 'maganda', 'na maganda'
            """
            if next_word == 'iti':
                """
                if the next word is 'nga' then it means
                naimbag nga = "magandang", "maganda ang"
                """
            isVerb = False
            isDone = True
           
        if word == 'amin' and not isDone:
            isVerb = False
            isDone = True
    
        
        if (word.find("adda") != -1) and not isDone:
            isVerb = True
            isDone = True
            
        if word == 'nagtignay' and not isDone:
            if next_word == 'iti':
                """
                if the word is 'nagtignay' and next word is 'iti' then it is a verb
                then it is a propositional determiner
                eg. nagtignay iti = sumasa / ay sumasa
                """
                isVerb = False
                isDone = True
    
        if word == 'ninagananna' and not isDone:
            """
            ninagananna = "tinawag", "tinawag + niya"
            "pinangalan", "pinangalan + niya"
            ninaganna = "tinawag", "tinawag + ng"
            "pinangalan", "pinangalan + ng"
            """
            can2Viterbi = True
            isVerb = True
            isDone = True
        
        if word == 'naaramid a casta' and not isDone:
            """
            naaramid a casta = 'nagkagayon'
            """
            isVerb = True
            isDone = True
    
        if word not in (PREPO_SET + PER_PRONOUN + CONJ_SET) and not isDone:
            if prev_word not in (noun_dtmn_list + adv_dtmn_list + prepo_dtmn_list): # if the previous word is not a determiner
                if next_word in (noun_dtmn_list): 
                    """
                    if the previous word is not in the noun, adverb, and preposition determiner and 
                    the next word is a noun determiner
                    """
                    if hasVerbAffixes:
                        """
                        if the current word has a verb affix/es, then it is a verb
                        """
                        isVerb = True
                        isDone = True
            
                if next_word in PER_PRONOUN and not isDone:
                    """
                    if the next word is a personal pronoun
                    eg. (insert an example sentence)
                    issue: check if there's an issue
                    """
                    isVerb = True
                    isDone = True                
        
            if word.startswith('pa') and (word.endswith('en') or word.endswith('in')):
                """
                if word starts with pa and ends with en or in then it is verb
                eg. patuboen
                """
                isVerb = True
                isDone = True                
        
            if word.startswith('ag') and prev_word == 'nga' and next_word in ('nga', 'a'):
                isVerb = True
                isDone = True                
        
            if word.startswith('ag') and (word.endswith('kayo') or word.endswith('cayo')):
                isVerb = True
                isDone = True

            if prev_word == 'ti' and next_word in (noun_dtmn_list) and (not next_word in ('a','iti', 'ken')) and not isDone:
                """
                if the previous word is 'ti' and the next word is a noun determiner
                eg. ti aramid ti dios (Nilalang ng Dios)
                """
                if word == 'aramid' and next_word == 'ti':
                    """
                    aramid which means gawa that is a noun is being used as a verb translation of 'nilalang'
                    """
                    isVerb = True
                    isDone = True

                elif next_word != 'ti':
                    isVerb = True
                    isDone = True
            
            if prev_word in CONJ_SET and hasVerbAffixes and next_word in noun_dtmn_list and not isDone:
                isVerb = True
                isDone = True

            if word.startswith("ag") and word[2:5] == word[5:8] and not isDone:
                """
                if the word is an adjective it repeats the next 3 letters after 'ag'
                eg. 'agcarcaryam' = umuusad
                """
                isVerb = True
                isDone = True

            if prev_word == 'nga' and next_word =='a':
                isVerb = True
                isDone = True

            if word == 'aguy' and next_word == 'uyas':
                isVerb = True
                isDone = True

            if prev_word == 'aguy' and word == 'uyas':
                isVerb = True
                isDone = True

            if prev_word == 'iti' and next_word == 'ken' and word.endswith('da') and hasVerbAffixes:
                isVerb = True
                isDone = True

            if prev2_word == 'ti' and not isDone:
                if next_word in (noun_dtmn_list) and not next_word == 'a':
                    """
                    if the previous of previous word is 'ti' and the next word is a noun determiner
                    eg. ti Dios pinarsuana dagiti (ay nilikha ng Dios)
                    """
                    isVerb = True
                    isDone = True
                
                if hasVerbAffixes and not isDone:
                    """
                    if the current word has a verb affix/es, then it is a verb
                    """
                    isVerb = True
                    isDone = True
        
        if hasVerbAffixes and prev_word == None and not isDone:
            """
            if the current word has a verb affix/es and the previous word is None
            """
            isVerb = True
            isDone = True
    
    return isVerb
# end of isVerb

"""
Noun Checker Function
"""
def isNoun(word, prev_word, prev2_word, next_word, next2_word, noun_dtmn_list, PREPO_SET, CONJ_SET, PER_PRONOUN, hasVerbAffixes):
    """
    This function tags if the specific word in the sentence is a noun, and extracts it.
    """
    isDone = False
    isNoun = False
    
    if word in PER_PRONOUN and word not in PREPO_SET:
        """
        if the word is a personal pronoun, then it is a noun
        """
        isNoun = True
        isDone = True

    if word and not isDone:
        if prev_word in (noun_dtmn_list) and word not in (PREPO_SET + CONJ_SET + noun_dtmn_list) and not isDone:
            isNoun = True
            
            if not word.startswith("maica") and not isDone:
                """
                if previous word is a and the word does not start with maica, then it is a noun
                """
                isNoun = True
                isDone = True
                
            elif word.startswith("maica"):
                isNoun = False
                isDone = True

            if next2_word.startswith("maica") and next_word == "a" and not isDone:
                """
                if next next word starts with maic prefix and next word is a, then it is a noun
                """
                isNoun = True
                isDone = True

            if word[:2] == word[2:4]:
                if prev_word in (noun_dtmn_list) and next_word not in ("ti", "nga", "a"):
                    """
                    if the first two letters of a word is repeated and next_word is not ti/nga/a, then it is a noun
                    """
                    isNoun = True
                    isDone = True
                else:
                    isNoun = False
                    isDone = False
            
            if word[:3] == word[3:6]:
                if prev_word in (noun_dtmn_list) and next_word not in (noun_dtmn_list):
                    isNoun = False

                elif prev_word in (noun_dtmn_list) and next_word == None:
                    isNoun = True

            isDone = True

        if prev_word == 'idi' and  not hasVerbAffixes and not isDone:
            isNoun = True
            isDone = True           
        
        if (word.startswith('ka') or word.startswith('ca')) and word.endswith('tayo'):
            """
            if word starts with pa and ends with en or in then it is verb
            eg. caaspingtayo = sa ating wangis
            """
            isNoun = True
            isDone = True 

        if next_word in CONJ_SET and not hasVerbAffixes and not isDone:
            isNoun = True
            isDone = True
        
        if prev_word in noun_dtmn_list and (next_word.find("adda") != -1):
            isNoun = True
            isDone = True
        
        if next_word =='a' and prev2_word == 'nga':
            isNoun = True
            isDone = True

        if prev_word == word[:2]:
            isNoun = True
            isDone = True

        if prev_word == 'nga' and next_word == 'ti':
            isNoun = True
            isDone = True

        if prev2_word in noun_dtmn_list and not isDone:
            isNoun = True
            isDone = True

        if word.endswith('um') or word.endswith('en'):
            isNoun = True
            isDone = True

        if word in PER_PRONOUN:
            isNoun = True
            isDone = True
    return isNoun
# end of isNoun

"""
Adjective Checker Function
"""
def isAdj(word, prev_word, prev2_word, next_word, hasVerbAffixes, noun_dtmn_list, adv_dtmn_list, prepo_dtmn_list, PREPO_SET, PER_PRONOUN, CONJ_SET):
    """
    This function tags if the specific word in the sentence is an adjective, and extracts it.
    """
    isDone = False
    isAdj = False
        
    if word not in (noun_dtmn_list + adv_dtmn_list + prepo_dtmn_list + PREPO_SET + PER_PRONOUN + CONJ_SET):
            
        if word.startswith("na") and (next_word in noun_dtmn_list or next_word == 'a' or prev_word == 'ti') and  not hasVerbAffixes and not isDone:
            """
            if the word is an adjective it has an adjective prefix 'na' and the next word is noun determiner
            """
            isAdj = True
            isDone = True

        if word.startswith("na") and word[:3] != 'nag' and prev2_word in noun_dtmn_list and (next_word in noun_dtmn_list or next_word == 'ket') and not isDone:
            """
            if the word is sandwiched between two nouns
            """
            isAdj = True
            isDone = True

        if word.startswith("na") and not word.startswith("nag") and (prev_word in ("ti", "nga", "a")) and (word.find("biag") == -1) and not word.endswith('sua') and not isDone:
            """
            if the adjective is at the end
            """
            isAdj = True
            isDone = True 

        if word.startswith("ka") and word.endswith("an") and not isDone:
            """
            if the word is an adjective it has an adjective prefix 'ka' and adjective suffix 'an' and its a superlative adjective
            """
            isAdj = True
            isDone = True 
    
        if (word.find("una") != -1) and (next_word == 'a' or next_word == 'nga') and  not hasVerbAffixes and not isDone:
            """
            if the word is an adjective it has a word 'una' and next word is 'a' or 'nga'
            """
            isAdj = True
            isDone = True

        if word == 'awan' and next_word in noun_dtmn_list and not isDone:
            """
            if the word is an adjective it is awan followed by noun
            """
            isAdj = True
            isDone = True
        
        if word == 'awan' and prev_word in noun_dtmn_list and not isDone:
            isAdj = True
            isDone = True

        if word == 'amin' and prev_word in PER_PRONOUN:
            isAdj = True
            isDone = True
    
        if word == 'maysa' and (next_word == 'a' or next_word == 'nga') and  not hasVerbAffixes and not isDone:
            """
            if the word is an adjective it is maysa followed by nga or a and its an ordinal adjective
            """
            isAdj = True
            isDone = True 

        if word.startswith("maika") or word.startswith("maica"):
            """
            if the word is an adjective it has an adjective prefix 'maika' or 'maica' and its an ordinal adjective
            """
            isAdj = True
            isDone = True 

        if word[:3] == word[3:6] and not word.endswith('aw') and (next_word in noun_dtmn_list or prev_word == 'a') and  not hasVerbAffixes and not isDone:
            """
            if the word is an adjective it repeats the first 3 letters to make it comparative
            """
            isAdj = True
            isDone = True 

        if word[:2] == word[2:4] and (next_word in noun_dtmn_list or prev_word in ('a', 'dagiti')) and not hasVerbAffixes and not isDone:
            if word =='lalaki' or word == 'babai':
                isAdj = False
                isNoun = True 
                isDone= False
            else:
                """
                if the word is an adjective it repeats the first 2 letters
                """
                isAdj = True
                isDone = True

        if word.startswith("na") and word[2:5] == word[5:8] and not isDone:
            """
            if the word is an adjective it repeats the next 3 letters after 'na' to make it comparative
            """
            isAdj = True
            isDone = True
        
        if word.startswith("na") and word[2:6] == word[6:10] and not isDone:
            """
            if the word is an adjective it repeats the next 4 letters after 'na' to make it comparative
            """
            isAdj = True
            isDone = True

    return isAdj
# end of isAdj

"""
Adverb Checker Function
"""
def isAdv(word, prev_word, next_word, PER_PRONOUN, PREPO_SET, adv_time_list, adv_manner_list, adv_freq_list, adv_place_list, adv_dtmn_list, noun_dtmn_list):
   """
   This function tags if the specific word in the Ilokano sentences is an adverb, and extracts it.
   """
   isDone = False
   isAdv = False
   
   if word not in PER_PRONOUN and word not in PREPO_SET:
      if word.startswith('idi') or word.startswith('di') and not prev_word == 'nga' and not isDone:
         """
         If the word starts with idi and has nga as its next word it is an adverb describing an adjective 
         """
         isAdv = True
         isDone = True
           
      if word in adv_time_list and not isDone:
         """
         If the word is in the adverb of time list, then it is an adverb
         """ 
         isAdv = True
         isDone = True
         
      if word in adv_manner_list and not isDone:
         """
         If the word is in the adverb of time list, then it is an adverb
         """ 
         isAdv = True
         isDone = True
         
      if word in adv_freq_list and not isDone:
         """
         If the word is in the adverb of time list, then it is an adverb
         """ 
         isAdv = True
         isDone = True
         
      if word in adv_place_list and not isDone:
         """
         If the word is in the adverb of time list, then it is an adverb
         """ 
         isAdv = True
         isDone = True
         
      if prev_word in adv_dtmn_list and not isVerb and not isNoun and not isDone:
         """
         If the word's previous word is in the determiner's list and not a verb or a noun, then it is n adverb
         """
         isAdv = True
         isDone = True
            
      if next_word =='nga' or next_word == 'a' and word.startswith("na") and not isDone: 
         """
         If the word starts with na and has nga as its next word it is an adverb describing an adjective
         eg. napartak nga iyaadu = mabilis na pagdami, Napigsa a tudo = malakas na ulan
         """   
         isAdv = True
         isDone = True 
         
      if word.startswith('na') and not next_word in noun_dtmn_list and not isDone:
         """
         If the next word is not a noun dtrmr and the word starts with 'a'
         """
         isAdv = True
         isDone = True
         
      if word == "awan" and not next_word in noun_dtmn_list or isNoun and not isDone:
         """
         If the next word is not a noun or pronoun and if the word is Awan, then it is adverb
         """
         isAdv = True
         isDone = True
                  
   return isAdv
# end of isAdv

"""
Preposition Checker Function
"""
def isPrepo(word, prev_word, prepo_dtmn_list, PREPO_SET):
    """
    This function checks if the specific word in the sentence is a preposition, and extracts it.
    """
    isPrepo = False
    isDone = False
    prev_word = ""
    
    if prev_word in (prepo_dtmn_list) and word in (PREPO_SET) and not isDone:
        isPrepo = True
        isDone = True
        
    if word not in (PREPO_SET) and not isDone:
        isPrepo = True
        isDone = True
        
    if word in (PREPO_SET) and not isDone:
        isPrepo = True
        isDone = True
    if (word.find("ruar") != -1):
        isPrepo = True
        isDone = True

    return isPrepo
# end of isPrepo

"""
    Conjunction Checker Function
"""

def isConj(word, CONJ_SET):
    """
    This function checks if the specific word in the sentence is a conjunction
    """
    if word in CONJ_SET:
        return True
    else:
        return False
# end of isConj

def pos(sentence_list):
    """
    This function takes a list of sentences and returns a list of tagged parts of speech for each word in the sentence.

    Parameters:
        sentence_list: a list of sentences where each sentence is a string
    
    Returms:
        pos_sen_list: a list of lists where each list contains tagged parts of speech for each word in a sentence.
    """
    isTagged = None
    hasVerbAffixes = None
    pos_sen_list = []

    for sentence in sentence_list:
        pos_list = []
        prev_word = ""
        prev2_word = ""
        sen_len = len(sentence)
        
        for word in sentence:
            
            isTagged = False
            hasVerbAffixes = False
            
            try:
                next_word = sentence[sentence.index(word) + 1]
            except (ValueError, IndexError):
                next_word = ""
            
            try:
                next2_word = sentence[sentence.index(word) + 2]
            except (ValueError, IndexError):
                next2_word = ""
                
            try:
                hasVerbAffixes = check_verb_affixes(word, isTagged, hasVerbAffixes, lists_il.PREFIX_SET, lists_il.INFIX_SET, lists_il.SUFFIX_SET)
            except (ValueError, IndexError):
                hasVerbAffixes = False
            
            if sen_len == 1:
                pos_list.append('SW')
                isTagged = True

            elif isDtmn(word, lists_il.noun_dtmn_list, lists_il.adv_dtmn_list, lists_il.prepo_dtmn_list, lists_il.adv_time_list) and not isTagged:
                pos_list.append('DT')
                isTagged = True
                
            elif isConj(word, lists_il.CONJ_SET) and not isTagged:
                pos_list.append('CC')
                isTagged = True
                
            elif isVerb(word, prev_word, prev2_word, next_word, hasVerbAffixes, lists_il.PREPO_SET, lists_il.PER_PRONOUN, lists_il.CONJ_SET, lists_il.noun_dtmn_list, lists_il.adv_dtmn_list, lists_il.prepo_dtmn_list) and not isTagged:

                pos_list.append('VB')
                isTagged = True

            elif isNoun(word, prev_word, prev2_word, next_word, next2_word, lists_il.noun_dtmn_list, lists_il.PREPO_SET, lists_il.CONJ_SET, lists_il.PER_PRONOUN, hasVerbAffixes) and not isTagged:
                pos_list.append('NN')
                isTagged = True
            
            elif isAdj(word, prev_word, prev2_word, next_word, hasVerbAffixes, lists_il.noun_dtmn_list, lists_il.adv_dtmn_list, lists_il.prepo_dtmn_list, lists_il.PREPO_SET, lists_il.PER_PRONOUN, lists_il.CONJ_SET) and not isTagged:
                pos_list.append('JJ')
                isTagged = True
               
            elif isAdv(word, prev_word, next_word, lists_il.PER_PRONOUN, lists_il.PREPO_SET, lists_il.adv_time_list, lists_il.adv_manner_list, lists_il.adv_freq_list, lists_il.adv_place_list, lists_il.adv_dtmn_list, lists_il.noun_dtmn_list) and not isTagged:
                pos_list.append('RB')
                isTagged = True
                
            elif isPrepo(word, prev_word, lists_il.prepo_dtmn_list, lists_il.PREPO_SET) and not isTagged:
                pos_list.append('PR')
                isTagged = True
                        
            else:
                pos_list.append('UNK')
                isTagged = True
            
            prev_word = word

            try:
                prev2_word = sentence[sentence.index(word) - 1]
            except (ValueError, IndexError):
                prev2_word = None
            
        pos_sen_list.append(pos_list)
        
    return pos_sen_list
# end of pos_src