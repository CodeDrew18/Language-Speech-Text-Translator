import string

def combine_tokens(sen_translation_list):
    """
    This function combines the translated tokens in a sentence into a single string.

    Parameters:
        sen_translation_list (list of lists): A list of sentence translations, where each sentence is a list of translated tokens.

    Returns:
        list: A list of sentence strings, where each sentence is a string formed by joining the translated tokens.
    """
    return [' '.join(sen_translation) for sen_translation in sen_translation_list]
# end of combine_tokens

def remove_punct(pText):
    """
    Remove all punctuation characters from a text string.

    Parameters:
        text (str): The input text string.

    Returns:
        str: The text string with all punctuation characters removed.
    """
    return "".join(char for char in pText if char not in string.punctuation)
# end of remove_punct

"""
Palindrome Checker Function
"""
def isPalindrome(word): 
    """
    This function checks if the word is a palindrome.
    """
    
    half_len = len(word)/2
    half_len = int(half_len)
    
    if word[:half_len] == word[half_len:] and half_len > 2:
        return True
    else:
        return False
# end of isPalindrome