from args import args
from chessbook_parser import parse_book, extract_special_tokens, segment_numbered_items
from bert import test_bert

from nltk.tokenize import sent_tokenize
import pandas as pd
from tqdm import tqdm
import os





def context_parser(context):
	updated_paragraphs = []
	for paragraph in context:
		new_paragraph = paragraph.replace('\n',' ')
		diagrams, moves, text_moves, num_items = extract_special_tokens(new_paragraph, num_item=True)
		if num_items == None:
			updated_paragraphs.append(paragraph)
		else:
			updated_paragraphs.extend(segment_numbered_items(new_paragraph))

	for i in range(13):
		print("---------")
		print(updated_paragraphs[i])
	exit()

	for paragraph in context:
		new_paragraph = paragraph.replace('\n',' ')
		diagrams, moves, text_moves, num_items = extract_special_tokens(new_paragraph, num_item=True)
		if num_items == None:
			#paragraph = paragraph.replace('\n',' ')
			#sentences = sent_tokenize(paragraph)
			#for sentence in sentences:
				#diagrams, moves, text_moves, num_items = extract_special_tokens(sentence, diagram=True, move=True, text_move=True)
				#print(sentence)
			pass
		else:
			print("move sequence found")
			print("-------------------\n"+paragraph+"\n-------------------")
			for item in num_items:
				print(item[0].strip() + "\n")
			print("-------------------------------------------------------")			
			par = segment_numbered_items(new_paragraph, print_all=True)
			sentences = sent_tokenize(par[-1])
			for sentence in sentences:
				#diagrams, moves, text_moves, num_items = extract_special_tokens(sentence, diagram=True, move=True, text_move=True)
				print(sentence)
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
