from args import args
from chessbook_parser import parse_book, extract_special_tokens
from bert import test_bert

from nltk.tokenize import sent_tokenize
import pandas as pd
from tqdm import tqdm
import os





def context_parser(context):

	for paragraph in context:
		diagrams, moves, text_moves, num_items = extract_special_tokens(paragraph, num_item=True)
		if num_items == None:
			#paragraph = paragraph.replace('\n',' ')
			#sentences = sent_tokenize(paragraph)
			#for sentence in sentences:
				#diagrams, moves, text_moves, num_items = extract_special_tokens(paragraph, diagram=True, move=True, text_move=True)
				#print(sentence)
			pass
		else:
			print("move sequence found")
			print("-------------------\n"+paragraph+"\n-------------------")

	exit()
	




def main():

	#parse the contexts
	path = os.path.join(args.book_path, args.chapter_name)
	contexts = parse_book(path)

	context_parser(contexts[0])
	exit()

	predictions = []
	

	for paragraph in tqdm(paragraphs):
		paragraph = paragraph.replace('\n',' ')
		sentences = sent_tokenize(paragraph)
		for sentence in sentences:
			row = []
			pred = test_bert(sentence, args.model_path)
			row.append(sentence)
			row.append(pred[0])
			predictions.append(row)

	df_predictions = pd.DataFrame(predictions, columns=["sentence","label"])
	save_path = os.path.join(args.data_path, "sentence_predictions.csv")
	df_predictions.to_csv(save_path, sep='\t')


if __name__ == "__main__":
	main()
