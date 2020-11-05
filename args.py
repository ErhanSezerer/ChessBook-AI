import argparse

RANDOM_STATE = 42


# ref: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')




parser = argparse.ArgumentParser(description='Experiments for Plausible Detection Models')
#-----------------------------------------------------------------------------------------
#BERT ARGUMENTS
#-----------------------------------------------------------------------------------------
#path
parser.add_argument('--model_path', default='./model/bert_epochs_7_lr_5e-05')
#other
parser.add_argument('--MAX_LEN', type=int, default=512)
parser.add_argument('--num_label', type=int, default=5)
parser.add_argument('--target_class', type=int, default=1)
parser.add_argument('--use_gpu', type=str2bool, default=True)



#-----------------------------------------------------------------------------------------
#PARSER ARGUMENTS
#-----------------------------------------------------------------------------------------
#paths
parser.add_argument('--book_path', default='./data/book')
parser.add_argument('--diagram_path', default='./data/diagrams')
parser.add_argument('--moves_path', default='./data/moves')
#other
parser.add_argument('--chapter_name', default='CH6 - The Middle Game.txt')#CH4 - The Opening.txt
parser.add_argument('--out_diag', type=str2bool, default=False)



#-----------------------------------------------------------------------------------------
#OTHER ARGUMENTS
#-----------------------------------------------------------------------------------------
#paths
parser.add_argument('--data_path', default='./data')
#other
parser.add_argument('--print_preds', type=str2bool)



args = parser.parse_args()









