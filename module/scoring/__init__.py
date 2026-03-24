import pandas as pd
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import sacrebleu


def bleu_score(target_op, system_op):
    cc = SmoothingFunction() #smoothing is used for short sentences or sentences without 3/4-grams
    return sentence_bleu([target_op], system_op, smoothing_function=cc.method4)#sentenece_blue() requires sentences to be tokenized list
# end of function


def scoring_bleu(dict_tl_il_result):
    system_op_list = dict_tl_il_result['System Output'].tolist()
    target_op_list = dict_tl_il_result['Target Output'].tolist()
    

    temp_index = 0
    total_bleu_score = 0
    score_list = []
    for target_op in target_op_list:
        system_op = system_op_list[temp_index]
        
        score = bleu_score(target_op, system_op)
        print("Reference: ", target_op)
        print("Machine Translation: ", system_op)
        print("BLEU Score: ", score)
        print("\n")
        
        """
            Writing the result to a file
        """
        # df.write("Reference: " + target_op + "\n")
        # df.write("Machine Translation: " + system_op + "\n")
        # df.write("BLEU Score: " + str(score) + "\n")
        # df.write("\n")
        
        score_list.append(score)
        total_bleu_score += score
        temp_index += 1

    dict_tl_il_result['Blue Score'] = score_list
    bleu = total_bleu_score / len(target_op_list)
    print("Average BLEU Score: ", bleu)
    # df.write("Average BLEU Score: " + str(average_bleu_score))
        
    return bleu
# end of bleu


def scoring_ter(dict_tl_il_result):
    system_op_list = dict_tl_il_result['System Output'].tolist()
    target_op_list = dict_tl_il_result['Target Output'].tolist()
    
    temp_index = 0
    total_ter_score = 0
    
    for target_op in target_op_list:
        system_op = system_op_list[temp_index]
        
        score = sacrebleu.corpus_ter(system_op, [target_op])
        total_ter_score += score.score
        
        temp_index += 1
    
    ter = total_ter_score / len(target_op_list)
    return ter
# end of ter
